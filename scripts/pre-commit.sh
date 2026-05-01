#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root and activate venv if present
REPO_ROOT="$(git rev-parse --show-toplevel)"
VENV="$REPO_ROOT/.venv/bin/activate"
if [ -f "$VENV" ]; then
    # shellcheck source=/dev/null
    source "$VENV"
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}  ✓${NC} $1"; }
fail() { echo -e "${RED}  ✗${NC} $1"; FAILED=1; }
info() { echo -e "${YELLOW}  →${NC} $1"; }

FAILED=0

echo ""
echo "Running pre-commit checks..."
echo ""

# ── 1. Block secret files ──────────────────────────────────────────────────
info "Checking for secret files"
SECRET_PATTERNS=('\.env$' '\.env\.' 'secrets\.' '\.pem$' '\.key$' 'id_rsa' 'credentials\.json')
STAGED=$(git diff --cached --name-only)

for pattern in "${SECRET_PATTERNS[@]}"; do
    matches=$(echo "$STAGED" | grep -E "$pattern" | grep -v '\.example$' || true)
    if [ -n "$matches" ]; then
        fail "Secret file staged: $matches"
    fi
done

if [ "$FAILED" -eq 0 ]; then
    pass "No secret files staged"
fi
FAILED_AFTER_SECRETS=$FAILED

# ── 2. Ruff lint ───────────────────────────────────────────────────────────
# --diff-filter=d excludes deleted files so ruff isn't handed paths that no longer exist
STAGED_PY=$(git diff --cached --name-only --diff-filter=d | grep '\.py$' || true)

if [ -n "$STAGED_PY" ]; then
    info "Ruff lint"
    if ! echo "$STAGED_PY" | xargs ruff check --no-cache 2>&1; then
        fail "Ruff lint failed — run: ruff check --fix <files>"
    else
        pass "Ruff lint"
    fi

    info "Ruff format"
    if ! echo "$STAGED_PY" | xargs ruff format --check --no-cache 2>&1; then
        fail "Ruff format failed — run: ruff format <files>"
    else
        pass "Ruff format"
    fi
else
    pass "No Python files staged — skipping lint"
fi

# ── 3. Django system check ─────────────────────────────────────────────────
info "Django system check"
if DJANGO_SETTINGS_MODULE=config.settings.test python manage.py check --no-color 2>&1; then
    pass "Django system check"
else
    fail "Django system check failed"
fi

# ── 4. Migration check ─────────────────────────────────────────────────────
info "Migration check"
if DJANGO_SETTINGS_MODULE=config.settings.test python manage.py makemigrations --check --dry-run --no-color 2>&1; then
    pass "No missing migrations"
else
    fail "Missing migrations — run: python manage.py makemigrations"
fi

# ── 5. Test suite ──────────────────────────────────────────────────────────
if [ "${SKIP_TESTS:-0}" = "1" ]; then
    echo -e "${YELLOW}  ⚠${NC}  Tests skipped (SKIP_TESTS=1)"
else
    info "Test suite"
    if DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test apps.waitlist apps.core --no-color -v 0 2>&1; then
        pass "All tests passed"
    else
        fail "Tests failed — run: python manage.py test apps.waitlist apps.core"
    fi
fi

echo ""
if [ "$FAILED" -ne 0 ]; then
    echo -e "${RED}Pre-commit failed. Fix the above issues before committing.${NC}"
    echo -e "${YELLOW}To skip tests: SKIP_TESTS=1 git commit ...${NC}"
    exit 1
fi
echo -e "${GREEN}All checks passed.${NC}"
echo ""

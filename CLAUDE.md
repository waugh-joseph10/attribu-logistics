# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Local Development (Native Python)

```bash
uv venv && source .venv/bin/activate
uv sync
cp .env.example .env
createdb attribu_local
make install-hooks   # Install pre-commit hook (run once after clone)

make run          # Django dev server on port 8000
make migrate      # Apply migrations
make migrations   # Create new migrations
make shell        # Django interactive shell
make superuser    # Create admin user
make static       # Collect static files
```

### Linting

```bash
make lint         # ruff check + format --check
make lint-fix     # ruff check --fix + format (auto-fix)
```

Ruff is configured with `line-length = 100`, rules `E F W I UP`, and `F403`/`F405` suppressed in settings files.

### Docker Development

```bash
make docker-dev-up    # Start all services (docker-compose.dev.yml)
make docker-dev-down  # Teardown
make docker-logs      # Tail logs from all services
make docker-shell     # Django shell inside container
make docker-migrate   # Run migrations inside container
```

### Docker Production

```bash
make docker-build      # Build image
make docker-up         # Start services (background)
make docker-down       # Stop services
make docker-ps         # Show running containers
make docker-restart    # Restart all services
make docker-superuser  # Create admin user inside container
make deploy            # git pull + rebuild + migrate (production)
make backup            # Dump PostgreSQL database
```

### Settings Module Selection

Django settings are split by environment. Set via `DJANGO_SETTINGS_MODULE`:
- `config.settings.local` — development (DEBUG, console email, debug_toolbar)
- `config.settings.docker_local` — Docker dev (DEBUG, console email, no debug_toolbar)
- `config.settings.production` — production (HTTPS, Celery, Sentry)
- `config.settings.test` — minimal test config

Docker dev services use `.env.docker` (not `.env`) — `DB_HOST=db`, `REDIS_URL=redis://redis:6379/0`.

### Tests

Tests live in `apps/*/tests.py`. Always use `config.settings.test` settings module:

```bash
DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test apps.waitlist apps.core
```

Run a single test class or method:
```bash
DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test apps.waitlist.tests.WaitlistJoinViewTests
DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test apps.waitlist.tests.WaitlistJoinViewTests.test_valid_signup
```

### Pre-commit Hook

`make install-hooks` installs `scripts/pre-commit.sh`, which runs on every commit: secret file check → ruff lint → ruff format → Django system check → migration check → test suite. To skip the test suite only:

```bash
SKIP_TESTS=1 git commit ...
```

## Architecture

### Services

The production stack (`docker-compose.yml`) consists of six services:

| Service | Image | Role |
|---|---|---|
| `db` | postgres:16-alpine | Primary database |
| `redis` | redis:7-alpine | Celery broker + result backend |
| `web` | app (Gunicorn) | Django WSGI app |
| `celery` | app (worker) | Async task processor |
| `nginx` | nginx:alpine | Reverse proxy, SSL, static files |
| `certbot` | certbot | Let's Encrypt renewal |

Celery Beat (scheduled tasks) is present in the compose file but commented out.

### Django Apps

**`apps.core`** — Landing page and ops infrastructure. Serves `index.html` and a `/health/` endpoint that validates DB connectivity (used by load balancers/monitoring).

**`apps.waitlist`** — The only active user-facing feature. `WaitlistEntry` model captures email + source. The `POST /waitlist/join/` view is CSRF-exempt and rate-limited at nginx (5 req/min per IP). On signup, two Celery tasks fire: `send_confirmation_email` (to user) and `send_admin_notification` (to admin). Both tasks retry up to 3× with 60s delay on failure. Active endpoints are plain Django views — DRF is installed but not used here.

**`apps.dispatch`** — Placeholder app for the future ML-powered route optimization module (planned: OR-Tools). Models and views are empty.

### Admin

The admin uses `django-unfold` for a custom UI. Configuration lives in `config/settings/base.py` under the `UNFOLD` dict. The sidebar navigation and dashboard callback are defined there; the dashboard callback is implemented in `apps/core/admin_dashboard.py`. To add new models to the sidebar nav, update the `UNFOLD['SIDEBAR']['navigation']` list in `base.py`.

### Configuration

Settings inherit from `config/settings/base.py`. Key env vars (see `.env.example`):

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`, `ADMIN_EMAIL`
- `SENTRY_DSN` (optional)

### Nginx

`nginx/conf.d/app.conf` handles:
- HTTP → HTTPS redirect
- TLS 1.2+ with modern ciphers, HTTP/2
- Rate limiting on `/waitlist/join/` (zone defined in `nginx/nginx.conf`)
- Static and media file serving with cache headers
- Security headers: CSP, X-Content-Type-Options, X-XSS-Protection

### Celery

Configured in `config/celery.py`. Tasks are autodiscovered. The broker and result backend are both Redis. Workers run in the `celery` container using the same Docker image as `web`.

### Static Files

WhiteNoise serves compressed static files directly from Gunicorn in production — no separate CDN or nginx static pass-through needed for MVP.

## Business Context

This is an early-stage SaaS targeting field service companies (HVAC, plumbing, landscaping) that waste $150K–$300K/year on inefficient routing. The platform will provide ML-powered dispatch with time windows, skill matching, and dynamic rerouting. The current codebase is a pre-launch waitlist site; the `dispatch` app is the future core product. See `CONTEXT.md` for full go-to-market strategy, pricing model, and product roadmap.

# Attribu Logistics

AI-powered dispatch and route optimization for field service operations.

## Tech Stack

- **Backend:** Django 5.2, PostgreSQL 16, Django REST Framework
- **Task Queue:** Celery + Redis
- **Deployment:** Docker, Nginx, Gunicorn

## Local Development

### Docker (Recommended)

```bash
make docker-dev-up
make docker-migrate
make docker-superuser
```

Visit http://localhost:8000

### Native Python

```bash
uv venv && source .venv/bin/activate
uv sync
cp .env.example .env
createdb attribu_local
make install-hooks
make migrate && make superuser && make run
```

## Common Commands

```bash
# Setup
make install-hooks        # Install pre-commit hook (run once after cloning)

# Docker dev
make docker-dev-up        # Start all services
make docker-dev-down      # Tear down
make docker-migrate       # Run migrations in container
make docker-superuser     # Create admin user in container
make docker-logs          # Tail logs
make docker-shell         # Django shell in container

# Native
make run                  # Start dev server
make migrate              # Run migrations
make superuser            # Create admin user

# Linting
make lint                 # Check ruff lint + format
make lint-fix             # Auto-fix ruff lint + format issues

# Production
make deploy               # Pull, build, migrate
make backup               # Dump database
```

## Pre-commit Hook

`make install-hooks` symlinks `scripts/pre-commit.sh` into `.git/hooks/`. On every commit it runs:

1. Secret file detection (blocks `.env`, `*.pem`, `*.key`, etc.)
2. Ruff lint and format check on staged Python files
3. Django system check (`manage.py check`)
4. Migration completeness check (`makemigrations --check`)
5. Full test suite

To commit while skipping tests: `SKIP_TESTS=1 git commit ...`

## Project Structure

```
apps/
  core/         Landing page, health checks
  waitlist/     Email capture
  dispatch/     Route optimization (future)
config/         Django settings, Celery config
nginx/          Reverse proxy config
docs/           Deployment guides
```

## Production Deployment

See [docs/deployment.md](docs/deployment.md) for the full VPS deployment guide and [docs/docker-setup.md](docs/docker-setup.md) for Docker configuration reference.

## License

Proprietary - All rights reserved

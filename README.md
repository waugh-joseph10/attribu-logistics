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
make migrate && make superuser && make run
```

## Common Commands

```bash
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

# Production
make deploy               # Pull, build, migrate
make backup               # Dump database
```

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

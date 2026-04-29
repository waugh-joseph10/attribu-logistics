# Attribu Logistics

AI-powered dispatch and route optimization for field service operations.

## Tech Stack

- **Backend:** Django 5.2, PostgreSQL 16, Django REST Framework
- **Task Queue:** Celery + Redis
- **Deployment:** Docker, Nginx, Gunicorn
- **Future:** Google OR-Tools, React frontend

## Local Development

### Docker (Recommended)

```bash
cp .env.example .env
# Edit .env: set DB_HOST=db, REDIS_URL=redis://redis:6379/0
make docker-dev-up
```

Visit http://localhost:8000

### Native Python

```bash
uv venv && source .venv/bin/activate
uv sync
cp .env.example .env
createdb attribu_local
make migrate && make run
```

## Common Commands

```bash
# Development
make run                  # Start Django dev server
make migrate              # Run migrations
make superuser            # Create admin user

# Docker
make docker-dev-up        # Start dev environment
make docker-logs          # View logs
make docker-shell         # Django shell

# Production
make deploy               # Pull, build, migrate
make backup               # Backup database
```

## Production Deployment

See [docs/deployment.md](docs/deployment.md) for complete VPS deployment guide.

## Project Structure

```
apps/
  core/         Landing page, health checks
  waitlist/     Email capture
  dispatch/     Route optimization
config/         Django settings, Celery config
nginx/          Nginx reverse proxy config
docs/           Deployment guides
```

## Documentation

- [Deployment Guide](docs/deployment.md) - Full VPS deployment walkthrough
- [Docker Setup](docs/docker-setup.md) - Docker configuration reference

## License

Proprietary - All rights reserved

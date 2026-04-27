# attribu.io

AI dispatch & route intelligence for field service operators.

## Stack

- **Backend:** Django 5.2 + PostgreSQL
- **Optimization:** Google OR-Tools (V2)
- **Async:** Celery + Redis (V2)
- **Frontend:** Django templates → React (V2)
- **Hosting:** Hetzner/DigitalOcean VPS

## Local setup

```bash
uv venv && source .venv/bin/activate
uv sync
cp .env.example .env  # fill in values
createdb attribu_local
make migrate
make run
```

## Commands

```bash
make run          # dev server
make migrate      # apply migrations
make migrations   # make migrations
make shell        # Django shell
make superuser    # create admin user
make static       # collect static files
```

## Project layout

```
apps/core/      landing page
apps/waitlist/  email capture
apps/dispatch/  route optimization (V1)
config/         Django project settings
```

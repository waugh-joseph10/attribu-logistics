# Docker Setup - Quick Reference

Complete Docker setup for Attribu Logistics. Files created and configuration guide.

## Files Created

### Core Docker Files
- `Dockerfile` - Multi-stage production image
- `docker-compose.yml` - Production orchestration
- `docker-compose.dev.yml` - Development orchestration
- `.dockerignore` - Build optimization

### Configuration
- `gunicorn.conf.py` - Gunicorn settings
- `docker-entrypoint.sh` - Startup script
- `nginx/nginx.conf` - Main nginx config
- `nginx/conf.d/app.conf` - Application nginx config

### Environment Templates
- `.env.docker` - Docker development template
- `.env.production.example` - Production template
- `.env.example` - Updated with Docker support

### Additional
- `config/celery.py` - Celery configuration
- `config/__init__.py` - Updated with Celery import
- `scripts/setup-ssl.sh` - SSL certificate helper
- Health check endpoint at `/health/`

## Quick Commands

### First Time Setup (Development)

```bash
# 1. Copy Docker environment file
cp .env.docker .env

# 2. Start development environment
make docker-dev-up

# 3. Create superuser (in another terminal)
make docker-superuser
```

### First Time Setup (Production)

```bash
# 1. Copy and configure production environment
cp .env.production.example .env
nano .env  # Edit with production values

# 2. Setup SSL certificates
./scripts/setup-ssl.sh

# 3. Deploy
make docker-build
make docker-up

# 4. Create superuser
make docker-superuser
```

## Environment Variables

### Development (.env.docker)
```bash
DB_HOST=db                           # Docker service name
REDIS_URL=redis://redis:6379/0       # Docker service name
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (.env.production.example)
```bash
SECRET_KEY=<generate-new-key>        # CRITICAL: Change this!
DEBUG=False
ALLOWED_HOSTS=attribu.io,www.attribu.io
DB_PASSWORD=<strong-password>        # CRITICAL: Change this!
SECURE_SSL_REDIRECT=True             # After SSL is set up
```

## Service Architecture

```
┌─────────────────────────────────────────────┐
│  Internet (ports 80/443)                    │
└──────────────────┬──────────────────────────┘
                   │
            ┌──────▼──────┐
            │    Nginx    │  (SSL termination, static files)
            └──────┬──────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼────┐         ┌────▼──────┐
    │   Web   │         │  Certbot  │
    │(Django) │         │(SSL Certs)│
    └────┬────┘         └───────────┘
         │
    ┌────┴────────────────┐
    │                     │
┌───▼────┐           ┌────▼────┐
│   DB   │           │  Redis  │
│(Postgres)          │         │
└────────┘           └────┬────┘
                          │
                     ┌────┴──────┐
                     │           │
                ┌────▼───┐   ┌───▼─────┐
                │ Celery │   │ Celery  │
                │ Worker │   │  Beat   │
                └────────┘   └─────────┘
```

## Volumes & Persistence

| Volume | Purpose | Backup? |
|--------|---------|---------|
| `postgres_data` | Database | YES ✓ |
| `redis_data` | Redis cache | Optional |
| `static_volume` | Static files | No (rebuild) |
| `media_volume` | User uploads | YES ✓ |

## Port Mapping

### Production (docker-compose.yml)
- 80 → nginx (HTTP, redirects to HTTPS)
- 443 → nginx (HTTPS)
- Internal: web:8000, db:5432, redis:6379

### Development (docker-compose.dev.yml)
- 8000 → web (Django dev server)
- 5432 → db (PostgreSQL)
- 6379 → redis (Redis)

## Common Tasks

### View Logs
```bash
# All services
make docker-logs

# Specific service
docker compose logs -f web
docker compose logs -f celery_worker
```

### Database Operations
```bash
# Backup
make backup

# Restore
cat backup_20260428.sql | docker compose exec -T db psql -U postgres attribu

# Shell
docker compose exec db psql -U postgres attribu
```

### Django Management
```bash
# Shell
make docker-shell

# Migrations
make docker-migrate

# Custom command
docker compose exec web python manage.py <command>
```

### Service Management
```bash
# Restart all
make docker-restart

# Restart one service
docker compose restart web

# View resource usage
docker stats

# Check health
curl http://localhost:8000/health/  # Dev
curl https://attribu.io/health/     # Prod
```

## Troubleshooting

### "Port already in use"
```bash
# Find what's using the port
sudo lsof -i :8000
sudo lsof -i :80

# Stop Docker services
make docker-down
```

### "Cannot connect to database"
```bash
# Check if DB is running
docker compose ps db

# Check DB logs
docker compose logs db

# Wait for DB to be ready (automatic in entrypoint)
```

### "Static files not loading"
```bash
# Rebuild with static collection
docker compose up -d --build

# Manual collection
docker compose exec web python manage.py collectstatic --noinput
```

### "SSL certificate errors"
```bash
# Re-run SSL setup
./scripts/setup-ssl.sh

# Check certificate files
ls -la certbot/conf/live/attribu.io/

# View certbot logs
docker compose logs certbot
```

### Clean slate (DESTRUCTIVE)
```bash
# Remove everything including volumes
docker compose down -v

# Remove all images
docker system prune -a

# Rebuild from scratch
docker compose up -d --build
```

## Security Checklist

Before deploying to production:

- [ ] Generate new `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure strong `DB_PASSWORD`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Set up SSL certificates
- [ ] Enable `SECURE_SSL_REDIRECT=True`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Enable `CSRF_COOKIE_SECURE=True`
- [ ] Configure firewall (ports 22, 80, 443)
- [ ] Set up automated backups
- [ ] Configure monitoring

## Performance Tuning

### Gunicorn Workers
Edit `gunicorn.conf.py`:
```python
workers = multiprocessing.cpu_count() * 2 + 1  # Default
workers = 8  # Or set manually based on CPU/RAM
```

### Celery Workers
Edit `docker-compose.yml`:
```yaml
celery_worker:
  deploy:
    replicas: 3  # Scale workers
```

### Database Connections
Edit `config/settings/production.py`:
```python
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

## Monitoring

### Health Endpoint
```bash
curl https://attribu.io/health/
# Expected: {"status": "healthy", "database": "connected"}
```

### Resource Usage
```bash
docker stats
docker compose ps
docker system df  # Disk usage
```

### Logs Analysis
```bash
# Errors only
docker compose logs | grep ERROR

# Web requests
docker compose logs web | grep "HTTP"

# Database queries (if logging enabled)
docker compose logs web | grep "SELECT"
```

## Backup Strategy

### Automated Daily Backups
```bash
# Add to crontab
0 2 * * * cd /path/to/app && make backup

# Or in docker-compose.yml, add backup service:
backup:
  image: postgres:16-alpine
  command: >
    sh -c "while true; do
      pg_dump -U postgres -h db attribu > /backup/attribu_$(date +%Y%m%d).sql;
      sleep 86400;
    done"
  volumes:
    - ./backups:/backup
```

## Next Steps

1. Test locally with `make docker-dev-up`
2. Review DEPLOYMENT.md for production steps
3. Set up monitoring (optional: Sentry, Uptime monitoring)
4. Configure automated backups
5. Plan scaling strategy

## Support & Documentation

- Full deployment guide: [deployment.md](deployment.md)
- Project README: [../README.md](../README.md)
- Django docs: https://docs.djangoproject.com/
- Docker docs: https://docs.docker.com/
- Nginx docs: https://nginx.org/en/docs/

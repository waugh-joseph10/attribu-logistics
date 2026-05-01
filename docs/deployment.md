# Deployment Guide - Attribu Logistics

Complete production deployment guide for VPS hosting.

## Prerequisites

- VPS with Docker and Docker Compose installed (Ubuntu 22.04+ recommended)
- Domain name pointed to your VPS IP address
- SSH access to your VPS
- Git installed on VPS
- GitHub repository with Actions and GHCR packages enabled
- GitHub `production` Environment with required reviewer approval

## Quick Start

### 1. VPS Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Verify installation
docker --version
docker compose version
```

### 2. Clone Repository

```bash
# Clone your repository
git clone https://github.com/yourusername/attribu-logistics.git
cd attribu-logistics
```

### 3. Environment Configuration

```bash
# Create production .env file
cp .env.production.example .env

# Edit .env with your production values
nano .env
```

**Critical values to change:**

```bash
# Generate a new secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Update these in .env:
SECRET_KEY=<generated-key-from-above>
DEBUG=False
ALLOWED_HOSTS=attribu.io,www.attribu.io
DB_PASSWORD=<strong-database-password>
REDIS_PASSWORD=<strong-redis-password>
APP_IMAGE=ghcr.io/<owner>/attribu-logistics:main-latest
```

`APP_IMAGE` is overridden by GitHub Actions during production deployments with an immutable SHA tag. Keeping a default in `.env` is useful for manual pulls and emergency redeploys.

### 4. SSL Certificate Setup (Let's Encrypt)

```bash
# Create certbot directories
mkdir -p certbot/conf certbot/www

# Temporarily comment out SSL lines in nginx/conf.d/app.conf
# Run this initial setup without SSL first
nano nginx/conf.d/app.conf
# Comment out lines 26-35 (SSL certificate paths)

# Start nginx temporarily for certbot
docker compose up -d nginx

# Obtain SSL certificate
docker compose run --rm certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  -d attribu.io \
  -d www.attribu.io \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email

# Uncomment SSL lines in nginx/conf.d/app.conf
nano nginx/conf.d/app.conf

# Restart nginx
docker compose restart nginx
```

### 5. Deploy Application

```bash
# Log in to GHCR with a read-only package token
echo "$GHCR_READ_TOKEN" | docker login ghcr.io -u "$GHCR_USERNAME" --password-stdin

# Pull and start the application image
docker compose pull web celery_worker
docker compose up -d --no-build --remove-orphans

# Check logs
docker compose logs -f

# Verify services are running
docker compose ps
```

### 6. Database Setup

```bash
# Create superuser
docker compose exec web python manage.py createsuperuser

# Verify database
docker compose exec db psql -U postgres -d attribu -c "SELECT version();"
```

### 7. Post-Deployment Verification

```bash
# Test health endpoint
curl https://attribu.io/health/

# Expected response:
# {"status": "healthy", "database": "connected"}

# Visit your site
# https://attribu.io
# https://attribu.io/admin
```

## Local Development with Docker

```bash
# Copy example env
cp .env.example .env

# Edit for Docker (set DB_HOST=db, REDIS_URL=redis://redis:6379/0)
nano .env

# Start development environment
docker compose -f docker-compose.dev.yml up

# Run migrations
docker compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Access at http://localhost:8000
```

## GitHub Actions Production Deployments

Production deploys are handled by `.github/workflows/ci-cd.yml`.

### Pull Requests

Pull requests to `main` run:

- Ruff lint and format checks
- Django system check using `config.settings.test`
- Migration drift check
- Test suite for `apps.waitlist` and `apps.core`
- Docker image build without pushing

### Main Branch

Pushes to `main` run the same checks, build the Docker image, and push it to GHCR with:

- `ghcr.io/<owner>/<repo>:sha-<commit-sha>`
- `ghcr.io/<owner>/<repo>:main-latest`

After the image is published, the workflow waits for approval in the GitHub `production` Environment. Once approved, it SSHes to the VPS, logs in to GHCR with a read-only token, pulls the approved image, recreates `web` and `celery_worker`, and verifies `/health/`.

### Required GitHub Configuration

Create a GitHub Environment named `production` with required reviewers and a deployment branch restriction for `main`.

Add these Environment secrets:

```text
VPS_HOST
VPS_USER
VPS_PORT
VPS_SSH_KEY
VPS_APP_DIR
GHCR_USERNAME
GHCR_READ_TOKEN
```

Add `PRODUCTION_URL` as an Environment variable or secret, for example:

```text
https://attribu.io
```

The workflow uses GitHub's built-in `GITHUB_TOKEN` to publish images to GHCR. The VPS uses `GHCR_READ_TOKEN` only to pull images.

### VPS Deploy User

Create a dedicated deploy user when possible, then allow it to run Docker:

```bash
sudo adduser deploy
sudo usermod -aG docker deploy
sudo mkdir -p /home/deploy/.ssh
sudo nano /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

Set `VPS_APP_DIR` to the directory containing `docker-compose.yml`, `.env`, `nginx/`, and `certbot/`.

## Deployment Commands

### Update Application

```bash
# Pull the image configured by APP_IMAGE and restart app services
docker compose pull web celery_worker
docker compose up -d --no-build --remove-orphans

# Migrations and static collection run automatically when web starts
```

Prefer the GitHub Actions workflow for normal production deploys. Use these commands for manual recovery or first-time bootstrap only.

### Roll Back Application

Redeploy a previous immutable image tag from GitHub Actions with `workflow_dispatch`, or run the equivalent manually:

```bash
APP_IMAGE=ghcr.io/<owner>/<repo>:sha-<previous-commit-sha> docker compose pull web celery_worker
APP_IMAGE=ghcr.io/<owner>/<repo>:sha-<previous-commit-sha> docker compose up -d --no-build --remove-orphans
curl https://attribu.io/health/
```

When `workflow_dispatch` receives an existing `image_tag`, the workflow skips source checks and image builds so emergency rollback is not blocked by the current branch state. Review migrations before rolling back across database schema changes.

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f celery_worker
docker compose logs -f nginx
```

### Database Backup

```bash
# Create backup
docker compose exec db pg_dump -U postgres attribu > backup_$(date +%Y%m%d).sql

# Restore backup
docker compose exec -T db psql -U postgres attribu < backup_20260428.sql
```

### Service Management

```bash
# Stop all services
docker compose down

# Stop and remove volumes (DESTRUCTIVE)
docker compose down -v

# Restart specific service
docker compose restart web

# View resource usage
docker stats
```

## Monitoring

### Health Checks

The application includes a health check endpoint at `/health/` that:
- Verifies database connectivity
- Returns JSON status
- Used by Docker and load balancers

```bash
# Manual health check
curl https://attribu.io/health/
```

### Log Monitoring

```bash
# Watch web logs
docker compose logs -f web

# Watch all errors
docker compose logs -f | grep ERROR

# Check Gunicorn workers
docker compose exec web ps aux | grep gunicorn
```

## Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False in production
- [ ] Configure strong DB_PASSWORD
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] SSL certificates installed and working
- [ ] GitHub `production` Environment requires reviewer approval
- [ ] GitHub Actions secrets configured for SSH deploys
- [ ] GHCR read token has the minimum required package permissions
- [ ] Uncomment HSTS header after testing SSL
- [ ] Enable SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE after SSL
- [ ] Configure firewall (UFW):
  ```bash
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```
- [ ] Set up automated backups
- [ ] Configure monitoring/alerting (optional: Sentry)

## Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs web

# Check if ports are in use
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Pull and recreate app services
docker compose pull web celery_worker
docker compose up -d --no-build --remove-orphans
```

### Database connection errors

```bash
# Check database is running
docker compose ps db

# Check database logs
docker compose logs db

# Test connection manually
docker compose exec db psql -U postgres -d attribu
```

### SSL certificate issues

```bash
# Check certbot logs
docker compose logs certbot

# Manually renew certificate
docker compose run --rm certbot renew

# Verify certificate files exist
ls -la certbot/conf/live/attribu.io/
```

### Static files not loading

```bash
# Collect static files manually
docker compose exec web python manage.py collectstatic --noinput

# Check nginx logs
docker compose logs nginx

# Verify static volume is mounted
docker compose exec nginx ls -la /app/staticfiles/
```

## Architecture

### Services

- **web**: Django/Gunicorn (port 8000 internal)
- **db**: PostgreSQL 16
- **redis**: Redis 7 (for Celery)
- **celery_worker**: Background task processor
- **celery_beat**: Periodic task scheduler
- **nginx**: Reverse proxy (ports 80/443)
- **certbot**: SSL certificate management

### Volumes

- `postgres_data`: Database persistence
- `redis_data`: Redis persistence
- `static_volume`: Django static files
- `media_volume`: User-uploaded files

### Networks

All services communicate via Docker's internal network.
External access only through Nginx on ports 80/443.

## Scaling

### Horizontal Scaling

```yaml
# In docker-compose.yml, scale workers:
celery_worker:
  deploy:
    replicas: 3
```

### Vertical Scaling

Edit `gunicorn.conf.py`:
```python
# Increase workers (CPU-bound)
workers = multiprocessing.cpu_count() * 4 + 1
```

## Maintenance

### Regular Tasks

- Review logs weekly
- Update dependencies monthly
- Backup database daily
- Monitor disk usage
- Review security headers

### Updates

```bash
# Update Python dependencies
# Edit pyproject.toml and uv.lock, then merge through GitHub Actions.
# The workflow builds and publishes the production image.

# Update system packages
sudo apt update && sudo apt upgrade -y
docker compose pull
docker compose up -d --no-build --remove-orphans
```

## Support

For issues, check:
1. Docker logs: `docker compose logs -f`
2. Django admin: https://attribu.io/admin
3. Health check: https://attribu.io/health/
4. Server resources: `docker stats`

#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Attribu application...${NC}"

# Wait for postgres to be ready
if [ "$DB_HOST" ]; then
    echo -e "${YELLOW}Waiting for PostgreSQL at $DB_HOST:${DB_PORT:-5432}...${NC}"
    while ! pg_isready -h "$DB_HOST" -p "${DB_PORT:-5432}" -U "$DB_USER" > /dev/null 2>&1; do
        sleep 1
    done
    echo -e "${GREEN}PostgreSQL is ready!${NC}"
fi

# Wait for Redis to be ready (if configured)
if [ "$REDIS_URL" ] || [ "$CELERY_BROKER_URL" ]; then
    echo -e "${YELLOW}Waiting for Redis...${NC}"
    # Simple check - just wait a bit for Redis
    sleep 2
    echo -e "${GREEN}Redis should be ready!${NC}"
fi

# Run migrations (only for web and celery worker, not beat)
if [ "$1" = "gunicorn" ] || [ "$1" = "celery-worker" ]; then
    echo -e "${YELLOW}Running database migrations...${NC}"
    python manage.py migrate --noinput
    echo -e "${GREEN}Migrations complete!${NC}"
fi

# Collect static files (only for web)
if [ "$1" = "gunicorn" ]; then
    echo -e "${YELLOW}Collecting static files...${NC}"
    python manage.py collectstatic --noinput
    echo -e "${GREEN}Static files collected!${NC}"
fi

# Execute the command
case "$1" in
    gunicorn)
        echo -e "${GREEN}Starting Gunicorn server...${NC}"
        exec gunicorn -c gunicorn.conf.py config.wsgi:application
        ;;
    celery-worker)
        echo -e "${GREEN}Starting Celery worker...${NC}"
        exec celery -A config worker -l info
        ;;
    celery-beat)
        echo -e "${GREEN}Starting Celery beat scheduler...${NC}"
        exec celery -A config beat -l info
        ;;
    *)
        echo -e "${YELLOW}Running custom command: $@${NC}"
        exec "$@"
        ;;
esac

# Developer setup
install-hooks:
	chmod +x scripts/pre-commit.sh
	ln -sf ../../scripts/pre-commit.sh .git/hooks/pre-commit
	@echo "Pre-commit hook installed."

lint:
	ruff check apps config
	ruff format --check apps config

lint-fix:
	ruff check --fix apps config
	ruff format apps config

# Local development (without Docker)
run:
	python manage.py runserver

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

static:
	python manage.py collectstatic --noinput

# Docker commands
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-ps:
	docker compose ps

docker-shell:
	docker compose exec web python manage.py shell

docker-migrate:
	docker compose exec web python manage.py migrate

docker-superuser:
	docker compose exec web python manage.py createsuperuser

docker-restart:
	docker compose restart

# Docker development
docker-dev-up:
	docker compose -f docker-compose.dev.yml up --build

docker-dev-down:
	docker compose -f docker-compose.dev.yml down

# Production deployment
deploy:
	git pull origin main
	$(eval export SENTRY_RELEASE=$(shell git rev-parse HEAD))
	docker compose build
	docker compose run --rm web python manage.py migrate
	docker compose up -d --remove-orphans
	@echo "Deployed release: $(SENTRY_RELEASE)"

# Backup database
backup:
	docker compose exec db pg_dump -U postgres attribu > backup_$(shell date +%Y%m%d_%H%M%S).sql

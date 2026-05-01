# Multi-stage build for optimized production image
FROM python:3.14-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies from the lockfile into system Python
RUN uv export --frozen --no-dev -o /tmp/requirements.txt && \
    uv pip install --system --no-cache -r /tmp/requirements.txt


# Production stage
FROM python:3.14-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 django && \
    mkdir -p /app /app/staticfiles /app/media && \
    chown -R django:django /app

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=django:django . .

# Make entrypoint executable
RUN chmod +x /app/docker-entrypoint.sh

# Switch to non-root user
USER django

# Collect static files with build-only placeholders required by production settings imports.
RUN SECRET_KEY=build-placeholder-not-used-in-production \
    EMAIL_HOST_USER=build-placeholder \
    EMAIL_HOST_PASSWORD=build-placeholder \
    REDIS_PASSWORD=build-placeholder \
    RESEND_API_KEY=build-placeholder \
    python manage.py collectstatic --noinput --settings=config.settings.production

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn"]

from decouple import config
from django.core.exceptions import ImproperlyConfigured

from .base import *

if DEBUG:
    raise ImproperlyConfigured("DEBUG must be False in production")

# Security Settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# CSRF trusted origins (add your domain)
CSRF_TRUSTED_ORIGINS = [
    "https://attribu.io",
    "https://www.attribu.io",
]

# Media files configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Celery Configuration (V2)
_redis_password = config("REDIS_PASSWORD", default="")
_redis_auth = f":{_redis_password}@" if _redis_password else ""
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default=f"redis://{_redis_auth}redis:6379/0")
CELERY_RESULT_BACKEND = config(
    "CELERY_RESULT_BACKEND", default=f"redis://{_redis_auth}redis:6379/0"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/New_York"

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Email configuration — optional, Celery email tasks will fail gracefully if not set
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

# Optional: Sentry integration for error tracking and performance monitoring
SENTRY_DSN = config("SENTRY_DSN", default=None)
if SENTRY_DSN:
    import logging

    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    def _filter_sentry_event(event, hint):
        """Filter or modify events before sending to Sentry"""
        # Don't send 404 errors to reduce noise
        if event.get("level") == "error":
            exc_info = hint.get("exc_info")
            if exc_info and "404" in str(exc_info[1]):
                return None

        # Add custom tags for better organization
        event.setdefault("tags", {})["business_tier"] = "waitlist"

        return event

    def _filter_sentry_transaction(event, _hint):
        """Filter performance transactions"""
        # Ignore health check endpoints to reduce noise
        if event.get("transaction") == "/health/":
            return None
        return event

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Integrations
        integrations=[
            DjangoIntegration(
                transaction_style="url",  # Group by URL pattern, not specific path
                middleware_spans=True,  # Track middleware performance
                signals_spans=True,  # Track Django signals
            ),
            CeleryIntegration(
                monitor_beat_tasks=True,  # Track Celery Beat scheduled tasks
                exclude_beat_tasks=None,  # Or list tasks to exclude
            ),
            RedisIntegration(),  # Track Redis operations
            LoggingIntegration(
                level=logging.INFO,  # Breadcrumbs from INFO+
                event_level=logging.ERROR,  # Send ERROR+ as events
            ),
        ],
        # Performance Monitoring
        traces_sample_rate=0.1,  # 10% of transactions (increase for low traffic)
        # Profiling (CPU/memory)
        profiles_sample_rate=0.1,  # Profile 10% of transactions
        # Error Sampling
        sample_rate=1.0,  # Capture 100% of errors (reduce if too noisy)
        # Environment & Release Tracking
        environment=config("SENTRY_ENVIRONMENT", default="production"),
        release=config("SENTRY_RELEASE", default=None),  # Set to git commit SHA
        # Security
        send_default_pii=False,
        # Additional Options
        attach_stacktrace=True,  # Include stacktrace for messages
        max_breadcrumbs=50,  # Keep more context (default: 100)
        # Custom filters
        before_send=_filter_sentry_event,
        before_send_transaction=_filter_sentry_transaction,
        # Ignore specific errors
        ignore_errors=[
            KeyboardInterrupt,
            "BrokenPipeError",
        ],
    )

import logging

import resend
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_confirmation_email(self, email):
    try:
        resend.api_key = settings.RESEND_API_KEY
        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [email],
            "subject": "You're on the Attribu waitlist",
            "text": (
                "Thanks for signing up for early access to Attribu.\n\n"
                "We're building smarter dispatch and route optimization for field service teams. "
                "We'll be in touch when we're ready for you.\n\n"
                "— The Attribu Team"
            ),
        }
        resend.Emails.send(params)
        logger.info("Confirmation email sent to %s", email)
    except Exception as exc:
        logger.error("Failed to send confirmation email to %s: %s", email, exc)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_admin_notification(self, email):
    try:
        resend.api_key = settings.RESEND_API_KEY
        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.ADMIN_EMAIL],
            "subject": "New Attribu waitlist signup",
            "text": f"New signup: {email}",
        }
        resend.Emails.send(params)
        logger.info("Admin notification sent for signup: %s", email)
    except Exception as exc:
        logger.error("Failed to send admin notification for %s: %s", email, exc)
        raise self.retry(exc=exc)

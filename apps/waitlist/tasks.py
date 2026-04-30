import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_confirmation_email(self, email):
    try:
        send_mail(
            subject="You're on the Attribu waitlist",
            message=(
                "Thanks for signing up for early access to Attribu.\n\n"
                "We're building smarter dispatch and route optimization for field service teams. "
                "We'll be in touch when we're ready for you.\n\n"
                "— The Attribu Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info("Confirmation email sent to %s", email)
    except Exception as exc:
        logger.error("Failed to send confirmation email to %s: %s", email, exc)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_admin_notification(self, email):
    try:
        send_mail(
            subject="New Attribu waitlist signup",
            message=f"New signup: {email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        logger.info("Admin notification sent for signup: %s", email)
    except Exception as exc:
        logger.error("Failed to send admin notification for %s: %s", email, exc)
        raise self.retry(exc=exc)

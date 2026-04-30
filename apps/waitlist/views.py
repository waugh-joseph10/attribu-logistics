import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import WaitlistEntry
from .tasks import send_confirmation_email, send_admin_notification

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def join(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    email = data.get('email', '').strip().lower()

    if not email:
        return JsonResponse({'error': 'Email required.'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

    entry, created = WaitlistEntry.objects.get_or_create(email=email)
    if not created:
        return JsonResponse({'message': 'Already on the list.'}, status=200)

    logger.info("New waitlist signup: %s", email)
    send_confirmation_email.delay(email)
    send_admin_notification.delay(email)

    return JsonResponse({'message': "You're on the list."}, status=201)

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    context = {
        "mapbox_token": settings.MAPBOX_PUBLIC_TOKEN,
    }
    return render(request, "core/index.html", context)


def health_check(request):
    """Health check endpoint for monitoring and load balancers."""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({"status": "healthy", "database": "connected"})
    except Exception:
        return JsonResponse({"status": "unhealthy", "error": "Service unavailable"}, status=503)

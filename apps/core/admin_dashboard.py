from datetime import timedelta

from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.waitlist.models import WaitlistEntry


def dashboard_callback(request, context):
    now = timezone.now()
    last_7_days = now - timedelta(days=7)
    today = timezone.localdate()
    chart_start = today - timedelta(days=29)
    total_signups = WaitlistEntry.objects.count()

    signup_counts = {
        row["day"]: row["total"]
        for row in WaitlistEntry.objects.filter(created_at__date__gte=chart_start)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    }
    chart_days = [chart_start + timedelta(days=offset) for offset in range(30)]

    sources = []
    for source in (
        WaitlistEntry.objects.values("source")
        .annotate(total=Count("id"))
        .order_by("-total", "source")[:5]
    ):
        source_total = source["total"]
        sources.append(
            {
                **source,
                "percentage": round((source_total / total_signups) * 100) if total_signups else 0,
            }
        )

    context.update(
        {
            "waitlist_total": total_signups,
            "waitlist_recent_total": WaitlistEntry.objects.filter(
                created_at__gte=last_7_days
            ).count(),
            "waitlist_latest": WaitlistEntry.objects.order_by("-created_at")[:5],
            "waitlist_sources": sources,
            "signup_chart_labels": [day.strftime("%b %-d") for day in chart_days],
            "signup_chart_values": [signup_counts.get(day, 0) for day in chart_days],
            "signup_chart_has_data": any(signup_counts.values()),
        }
    )
    return context


def environment_callback(request):
    if settings.DEBUG:
        return ["Local", "info"]

    return ["Production", "danger"]

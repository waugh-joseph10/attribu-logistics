import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import action
from unfold.enums import ActionVariant

from .models import WaitlistEntry


@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(ModelAdmin):
    list_display = ["email_link", "source", "created_at", "signup_age"]
    list_filter = ["source", ("created_at", RangeDateTimeFilter)]
    search_fields = ["email"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    list_per_page = 50
    list_fullwidth = True
    list_filter_submit = True
    actions = ["export_as_csv"]

    @action(
        description=_("Export selected entries as CSV"),
        icon="download",
        variant=ActionVariant.PRIMARY,
    )
    def export_as_csv(self, request, queryset):
        timestamp = timezone.now().strftime("%Y%m%d-%H%M%S")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="waitlist-{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(["email", "source", "created_at"])

        for entry in queryset.order_by("-created_at"):
            writer.writerow([entry.email, entry.source, entry.created_at.isoformat()])

        return response

    @admin.display(description=_("Email"), ordering="email")
    def email_link(self, obj):
        return format_html('<a href="mailto:{0}">{0}</a>', obj.email)

    @admin.display(description=_("Age"), ordering="created_at")
    def signup_age(self, obj):
        return _("%(age)s ago") % {"age": timesince(obj.created_at)}

from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "doctor", "date", "time", "status", "created_at")
    list_filter = ("status", "date", "service", "doctor", "created_at")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "service__title",
        "doctor__name",
    )

from django.contrib import admin

from .models import Event, EventRegistration


@admin.register(Event, EventRegistration)
class ReservationAdmin(admin.ModelAdmin):
    """Admin interface for the boat, material, room, reservabletype and reservation."""

"""
Admin configuration for the events module.

This module defines the admin interfaces for managing events and event registrations.
"""
from typing import ClassVar

from django.contrib import admin

from .models import Event, EventOrganizer, EventRegistration
from .models.registration_form_field import RegistrationFormField


class RegistrationFormInline(admin.TabularInline):
    """Inline admin interface for registration form fields."""

    model = RegistrationFormField
    extra = 1

class EventOrganizerInline(admin.TabularInline):
    """Inline admin interface for event organizers."""

    model = EventOrganizer
    filter_horizontal = ("groups", "user")
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for the fields of the event class."""

    fields = ("title", "description", "start", "end", "registration_start",
              "registration_deadline", "cancelation_deadline", "price",
              "capacity", "location", "category")
    inlines: ClassVar[list[type]] = [RegistrationFormInline, EventOrganizerInline]

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for managing event registrations."""

@admin.register(RegistrationFormField)
class RegistrationFormAdmin(admin.ModelAdmin):
    """Admin interface for managing registration form fields."""


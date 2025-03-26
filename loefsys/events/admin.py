"""
Admin configuration for the events module.

This module defines the admin interfaces for managing events and event registrations.
"""

from django.contrib import admin

from .models import Event, EventRegistration
from .models.registration_form_field import RegistrationFormField


class RegistrationFormInline(admin.TabularInline):
    model = RegistrationFormField
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for the boat, material, room, reservabletype and reservation."""
    fields = ('title', 'description', 'start', 'end', 'registration_deadline', 'cancelation_deadline', 'price', 'location', 'category')
    inlines = [RegistrationFormInline]

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    pass

@admin.register(RegistrationFormField)
class RegistrationFormAdmin(admin.ModelAdmin):
    pass
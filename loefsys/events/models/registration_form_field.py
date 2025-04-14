"""
Defines the RegistrationForm model.

This model is used to handle registrations for events in the application.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from loefsys.events.models import event
from loefsys.events.models.registration import EventRegistration


class RegistrationFormField(models.Model):
    """
    Represents a registration form for events.

    This model stores the subject, response, and associated event for a registration.
    """

    BOOLEAN_FIELD = "boolean"
    INTERGER_FIELD = "integer"
    CHAR_FIELD = "text"
    DATETIME_FIELD = "datetime"

    FIELD_TYPES = [  # noqa: RUF012
    (BOOLEAN_FIELD, _("Boolean")),
    (INTERGER_FIELD, _("Integer")),
    (CHAR_FIELD, _("Text")),
    (DATETIME_FIELD, _("Datetime")),
]

    event = models.ForeignKey(event.Event, models.CASCADE, verbose_name=_("Event"))

    type = models.CharField(
        max_length=20, choices=FIELD_TYPES, default=CHAR_FIELD, verbose_name=_("Type")
    )

    subject = models.CharField(max_length=200, verbose_name=_("Subject"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    required = models.BooleanField(default=True, verbose_name=_("Required"))

    @property
    def default(self):
        return ""

    def __str__(self):
        return self.subject

    class Meta:
        order_with_respect_to = "event"


class RegistrationFormFieldResponse(models.Model):
    """
    Represents a response to a registration form field.

    This model stores the response value and associated registration form field.
    """

    BOOLEAN_FIELD = "boolean"
    INTERGER_FIELD = "integer"
    CHAR_FIELD = "text"
    DATETIME_FIELD = "datetime"

    FIELD_TYPES = [  # noqa: RUF012
    (BOOLEAN_FIELD, _("Boolean")),
    (INTERGER_FIELD, _("Integer")),
    (CHAR_FIELD, _("Text")),
    (DATETIME_FIELD, _("Datetime")),
]

    field = models.ForeignKey(RegistrationFormField, models.CASCADE)
    registration = models.ForeignKey(EventRegistration, models.CASCADE)

    response = models.CharField(
        max_length=20, choices=FIELD_TYPES, default=CHAR_FIELD, verbose_name=_("Type")
    )

    def __str__(self):
        return self.response

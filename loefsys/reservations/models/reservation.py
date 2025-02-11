"""Module defining the model for a reservation."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.utils.translation import gettext_lazy as _


class Reservation(models.Model):
    """Model describing a reservation of a reservable item.

    A reservation is a 'time-claim' anyone can put on a reservable item. It has a start
    time and end time which is after the start time. The start time may be in the past,
    but only an admin can create reservation that ends in the past. The start time and
    end time may be on different dates, as long as the start time is earlier than the
    end time. A reservation has a reference to a person (or possibly to a group). A
    reservation has a function which can calculate any costs related to that
    reservation. A reservation has a log, which the user must fill in after the
    reservation has ended. A reservation can be linked to a group, training or event.

    A boat reservation can be linked to a training (or event). If it is not then it must
    be reserved by a person with the required skipper's certificate. If the boat has an
    engine, then the user can set an amount of engine-hours used.

    Attributes
    ----------
    content_type : ~django.contrib.contenttypes.models.ContentType
        Part of the ForeignKey.
    item_id : int
        Part of the ForeignKey.
    item : ~loefsys.reservations.models.reservable.ReservableItem
        The item that is reserved.
    start : ~datetime.datetime
        The start timestamp of the reservation.
    end : ~datetime.datetime
        The end timestamp of the reservation.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "item_id")

    start = models.DateTimeField(verbose_name=_("Start time"))
    end = models.DateTimeField(verbose_name=_("End time"))

    class Meta:
        indexes = (models.Index(fields=["content_type", "item_id"]),)
        constraints = (
            # TODO Check for permissions of the reservator, depends on the implementation of permissions.  # noqa: E501
            # CheckConstraint(
            #     check=(),
            #     name="permission",
            #     violation_error_message="You are not permitted to make this reservation.",  # noqa: E501
            # ),
            CheckConstraint(
                condition=Q(end__gt=F("start")),
                name="end_gt_start",
                violation_error_message="End time cannot be before the start time.",
            ),
            CheckConstraint(
                condition=Q(start__gte=F("end")),
                name="start_gte_end",
                violation_error_message="This item has already been reserved during this timeslot.",  # noqa: E501
            ),
        )

    def __str__(self) -> str:
        return f"Reservation for {self.item}"

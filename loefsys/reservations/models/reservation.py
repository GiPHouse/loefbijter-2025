"""Module defining the model for a reservation."""

from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.forms import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from loefsys.reservations.models.boat import Boat
# from loefsys.reservations.models.choices import ReservableCategories
from loefsys.reservations.models.reservable import ReservableItem
from loefsys.users.models.user import User
from loefsys.users.models.user_skippership import UserSkippership


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
    reserved_item : ~loefsys.reservations.models.reservable.ReservableItem
        The ForeignKey.
    reservee_member : ~loefsys.users.models.member.MemberDetails
        The person reserving the item, is null if a group is reserving the item.
    reservee_group : ~loefsys.groups.models.group.LoefBijterGroup
        The group reserving the item, is null if a person is reserving the item.
    authorized_skipper : ~loefsys.users.models.user.User
        The person who is the authorized skipper for a boat.
    start : ~datetime.datetime
        The start timestamp of the reservation.
    end : ~datetime.datetime
        The end timestamp of the reservation.
    """

    reserved_item = models.ForeignKey(ReservableItem, on_delete=models.CASCADE)
    # reservee_member = models.ForeignKey(MemberDetails, on_delete=models.CASCADE)
    # reservee_group = models.ForeignKey(LoefbijterGroup, on_delete=models.CASCADE)
    reservee_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservee_user_reservation_set"
    )
    # TODO reservee_user is a temporary field which should be replaced
    # by the fields reservee_member and reservee_group once the WebCie
    # has added Member(ship) to the admin page.
    # TODO Add a constraint to check whether the skipper has the correct skipperships.
    authorized_skipper = models.ForeignKey(
        UserSkippership,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="authorized_skipper_reservation_set",
    )

    start = models.DateTimeField(verbose_name=_("Start time"))
    end = models.DateTimeField(verbose_name=_("End time"))
    date_of_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
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
            # CheckConstraint(
            #     condition=(
            #         Q(reservee_member__isnull=True) & Q(reservee_group__isnull=False)
            #     )
            #     | (Q(reservee_member__isnull=False) & Q(reservee_group__isnull=True)),
            #     name="member_or_group",
            #     violation_error_message="Only a group or a member can make reservation, not both.",  # noqa: E501
            # ),  # TODO create tests for this
        )

    def __str__(self) -> str:
        return f"Reservation for {self.reserved_item}"

    def get_absolute_url(self):
        """Return the detail page url for this reservation."""
        return reverse("reservation-detail", kwargs={"pk": self.pk})

    def clean(self):
        """Check whether any of the other reservations overlapand if the boat requires a skippership.

        Raises
        ------
            ValidationError: This item has already been reserved during this timeslot.
            ValidationError: This item is not reservable at the moment.
            ValidationError: The boat selected requires a skippership to be set.
            ValidationError: The skippership set is not valid for this boat.
        """  # noqa: E501
        try:
            Reservation.objects.get(
                ~Q(pk=self.pk)
                & Q(reserved_item=self.reserved_item)
                & (
                    Q(start__range=(self.start, self.end))
                    | Q(end__range=(self.start, self.end))
                    | Q(start__lt=self.start, end__gt=self.end)
                )
            )
            raise ValidationError(
                "This item has already been reserved during this timeslot."
            )
        except Reservation.DoesNotExist:
            if not self.reserved_item.is_reservable:
                raise ValidationError("This item is not reservable at the moment.")

            # TODO Add a field to the frontend in the ReservationCreateView to support skipperships.  # noqa: E501
            # if self.reserved_item.reservable_type.category == ReservableCategories.BOAT:  # noqa: E501
            #     requires_skippership = Boat.objects.get(
            #         pk=self.reserved_item.pk
            #     ).requires_skippership
            #     if requires_skippership:
            #         if not self.authorized_skipper:
            #             raise ValidationError(
            #                 "The boat selected requires a skippership to be set."
            #             )

            #         if requires_skippership != self.authorized_skipper.skippership:
            #             raise ValidationError(
            #                 "The skippership set is not valid for this boat."
            #             )
            return

"""Module defining the model for generic materials."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import ReservableCategories
from .reservable import ReservableItem, ReservableType


class Material(ReservableItem):
    """Describes a material item that can be reserved.

    A gear-piece is any wearable item used for sailing. It is of a type and has a size
    measure.

    Attributes
    ----------
    reservable_type : ~loefsys.reservations.models.reservable.ReservableType
        The type for which the pricing is set.
    size : str
        The size of the item (if applicable?).
    """

    size = models.CharField(max_length=10, verbose_name=_("Size"))



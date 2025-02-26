"""Module containing the model definitions for a fraternity."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import FraternityGenders
from .group import LoefbijterGroup


class Fraternity(LoefbijterGroup):
    """Model defining fraternities within the associations.

    Fraternities are groups of members that want to do more outside of the regular
    association activities. Fraternities can be male only, female only or mixed.

    Attributes
    ----------
    gender_requirement : FraternityGenders
        The type of fraternity.
    """

    class Meta:
        verbose_name_plural = _("Fraternities")

    gender_requirement = models.PositiveSmallIntegerField(
        choices=FraternityGenders, default=FraternityGenders.MIXED
    )

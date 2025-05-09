"""Module defining the Loefbijter user skippership model."""

from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from loefsys.users.models.skippership import Skippership

from . import User


class UserSkippership(models.Model):
    """Model connecting a user to a skippership they have obtained."""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    skippership = models.ForeignKey(to=Skippership, on_delete=models.CASCADE)
    since = models.DateField(
        verbose_name=_("Skippership since"),
        help_text=_("The date the user obtained the skippership."),
        default=date.today,
    )
    given_by = models.ManyToManyField(
        User,
        verbose_name=_("Skippers authorized"),
        help_text=_("The skippers that have authorized the skippership."),
        related_name="skipper_set",
        related_query_name="skipper",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["user", "skippership"], name="unique_skippership"
            ),
        )

    def __str__(self) -> str:
        return f"{self.skippership.name} {self.user.display_name}"

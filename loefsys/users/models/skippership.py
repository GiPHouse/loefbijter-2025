"""Module defining the Loefbijter skippership model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import User


class Skippership(models.Model):
    """Model defining skipperships."""

    name = models.CharField(max_length=40, verbose_name=_("Skippership"), unique=True)
    skippers = models.ManyToManyField(User, through="UserSkippership")

    def __str__(self) -> str:
        return self.name

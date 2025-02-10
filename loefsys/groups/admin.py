from django.contrib import admin  # noqa: D100

from .models import Board, Committee, Fraternity, Taskforce, YearClub


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin interface for the board model."""

    list_display = ("name", "year",)
    list_filter = ("active",)
    search_fields = ("name", "description", "year")	


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    """Admin interface for the committee model."""

    list_display = ("name", "description", "active")
    list_filter = ("mandatory", "active")
    search_fields = ("name", "description")

@admin.register(Fraternity)
class FraternityAdmin(admin.ModelAdmin):
    """Admin interface for the fraternity model."""

    list_display = ("name", "gender_requirement", "active")
    list_filter = ("active",)
    search_fields = ("name", "description")

@admin.register(Taskforce)
class TaskforceAdmin(admin.ModelAdmin):
    """Admin interface for the taskforce model."""

    list_display = ("name", "description", "active", "requires_nda")
    list_filter = ("active", "requires_nda")
    search_fields = ("name", "description")

@admin.register(YearClub)
class YearClubAdmin(admin.ModelAdmin):
    """Admin interface for the year club model."""

    list_display = ("name", "year", "active")
    list_filter = ("active",)
    search_fields = ("name", "description")


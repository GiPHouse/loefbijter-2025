from django.contrib import admin

from .models import Reservation, ReservableType, Boat, Material, Room


@admin.register(Reservation, ReservableType, Boat, Material, Room)
class ReservationsAdmin(admin.ModelAdmin):
    pass


# TODO Change `item id` such that an object can be selected.

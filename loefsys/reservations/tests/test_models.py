import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from django_dynamic_fixture import G

from loefsys.reservations.models import (
    Boat,
    Material,
    ReservableType,
    Reservation,
    Room,
)
from loefsys.reservations.models.choices import ReservableCategories


class BoatTestCase(TestCase):
    """Tests for Boat model creation and validation."""

    def test_create(self):
        """Test that Boat instance can be created."""
        boat = G(Boat)
        self.assertIsNotNone(boat)
        self.assertIsNotNone(boat.pk)


class MaterialTestCase(TestCase):
    """Tests for Material model creation and validation."""

    def test_create(self):
        """Test that Material instance can be created."""
        material = G(Material)
        self.assertIsNotNone(material)
        self.assertIsNotNone(material.pk)


class ReservableTypeTestCase(TestCase):
    """Tests for ReservableType model creation and validation."""

    def test_create(self):
        """Test that ReservableType instance can be created."""
        reservable_type = G(ReservableType)
        self.assertIsNotNone(reservable_type)
        self.assertIsNotNone(reservable_type.pk)


class ReservableTypePricingTestCase(TestCase):
    """Tests for ReservableTypePricing model creation and validation."""

    def test_create(self):
        """Test that ReservableTypePricing instance can be created."""
        pricing = G(ReservableType)
        self.assertIsNotNone(pricing)
        self.assertIsNotNone(pricing.pk)


class ReservationTestCase(TestCase):
    """Tests for Reservation model creation and validation."""

    def test_create(self):
        """Tests that Reservation instance can be created."""
        reservation = G(Reservation)
        self.assertIsNotNone(reservation)
        self.assertIsNotNone(reservation.pk)

    def test_same_start_end(self):
        """Tests that Reservation instance cannot be created with the same start and end time."""  # noqa: E501
        with self.assertRaises(IntegrityError):
            reservation = Reservation(
                content_type=ContentType.objects.get_for_model(Room),
                item_id=0,
                start=datetime.datetime(2025, 1, 1, hour=12, minute=0),
                end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
            )
            reservation.save()

    def test_start_after_end(self):
        """Tests that Reservation instance cannot be created with the start after the end time."""  # noqa: E501
        with self.assertRaises(IntegrityError):
            reservation = Reservation(
                content_type=ContentType.objects.get_for_model(Room),
                item_id=0,
                start=datetime.datetime(2025, 1, 1, hour=13, minute=0),
                end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
            )
            reservation.save()

    def test_reserved_twice(self):
        """Tests that two Reservation instances can be created for the same item on different timeslots."""  # noqa: E501
        reservation1 = Reservation(
            content_type=ContentType.objects.get_for_model(Room),
            item_id=0,
            start=datetime.datetime(2025, 1, 1, hour=11, minute=0),
            end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
        )
        reservation1.save()

        reservation2 = Reservation(
            content_type=ContentType.objects.get_for_model(Room),
            item_id=0,
            start=datetime.datetime(2025, 1, 1, hour=13, minute=0),
            end=datetime.datetime(2025, 1, 1, hour=14, minute=0),
        )
        reservation2.save()

        self.assertIsNotNone(reservation1)
        self.assertIsNotNone(reservation2)

    def test_reserved_twice_overlap(self):
        """Tests that two Reservation instances can be created for the same item on overlapping timeslots."""  # noqa: E501
        with self.assertRaises(ValidationError):
            reservation1 = Reservation(
                content_type=ContentType.objects.get_for_model(Room),
                item_id=0,
                start=datetime.datetime(2025, 1, 1, hour=11, minute=0),
                end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
            )
            reservation1.save()
            reservation1.clean()

            reservation2 = Reservation(
                content_type=ContentType.objects.get_for_model(Room),
                item_id=0,
                start=datetime.datetime(2025, 1, 1, hour=11, minute=30),
                end=datetime.datetime(2025, 1, 1, hour=13, minute=0),
            )
            reservation2.save()
            reservation2.clean()

    def test_duplicate(self):
        """Tests that two duplicate Reservation instances cannot be created."""
        with self.assertRaises(ValidationError):
            reservation1 = Reservation(
                content_type=ContentType.objects.get_for_model(Room),
                item_id=0,
                start=datetime.datetime(2025, 1, 1, hour=11, minute=0),
                end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
            )
            reservation1.save()

            reservation2 = Reservation(
                content_type=ContentType.objects.get_for_model(Room),
                item_id=0,
                start=datetime.datetime(2025, 1, 1, hour=11, minute=0),
                end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
            )
            reservation2.clean()
            reservation2.save()

    def test_reserved_two_overlap(self):
        """Tests that two Reservation instances can be created for two items on overlapping timeslots."""  # noqa: E501
        reservable_type = ReservableType(
            name="Room", category=ReservableCategories.ROOM, description="GiPHouse room"
        )
        reservable_type.save()

        room1 = Room(reservable_type=reservable_type, name="Vienna", capacity=9)
        room2 = Room(reservable_type=reservable_type, name="Copenhagen", capacity=9)
        room1.save()
        room2.save()

        reservation1 = Reservation(
            item=room1,
            start=datetime.datetime(2025, 1, 1, hour=11, minute=0),
            end=datetime.datetime(2025, 1, 1, hour=12, minute=0),
        )
        reservation1.save()

        reservation2 = Reservation(
            item=room2,
            start=datetime.datetime(2025, 1, 1, hour=11, minute=30),
            end=datetime.datetime(2025, 1, 1, hour=13, minute=0),
        )
        reservation2.clean()
        reservation2.save()

        self.assertIsNotNone(reservation1)
        self.assertIsNotNone(reservation2)

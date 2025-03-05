"""Module defining the class-based views for the reservations."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from loefsys.reservations.models.reservation import Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ["reserved_item", "start", "end"]


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    fields = ["reserved_item", "start", "end"]


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation

class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
"""Module defining the class-based views for the reservations."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from loefsys.reservations.forms import CreateReservationForm
from loefsys.reservations.models.reservation import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    """Reservation list view."""

    model = Reservation
    context_object_name = "reservations"

    def get_queryset(self):
        """Only show instances of Reservation made by the user."""
        return Reservation.objects.filter(reservee_user=self.request.user)


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """Reservation create view."""

    model = Reservation
    form_class = CreateReservationForm

    def form_valid(self, form):
        """Add the user who made the reservation to the Reservation instance."""
        form.instance.reservee_user = self.request.user
        return super().form_valid(form)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    """Reservation update view."""

    model = Reservation
    fields = ("reserved_item", "start", "end")

    def get_queryset(self):
        """Only show instances of Reservation made by the user."""
        return Reservation.objects.filter(reservee_user=self.request.user)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """Reservation delete view."""

    model = Reservation
    template_name = "reservations/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservations")


class ReservationDetailView(LoginRequiredMixin, DetailView):
    """Reservation detail view."""

    model = Reservation

    def get_queryset(self):
        """Only show instances of Reservation made by the user."""
        return Reservation.objects.filter(reservee_user=self.request.user)

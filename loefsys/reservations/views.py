"""Module defining the class-based views for the reservations."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from loefsys.reservations.forms import CreateReservationForm, FilterReservationForm
from loefsys.reservations.models.reservable import ReservableItem
from loefsys.reservations.models.reservation import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    """Reservation list view."""

    model = Reservation
    context_object_name = "reservations"

    def get_queryset(self):
        """Only show instances of Reservation made by the user, with the option to filter them."""  # noqa: E501
        form = FilterReservationForm(self.request.GET)
        filters = "start"

        if form.is_valid() and form.cleaned_data["filters"]:
            match form.cleaned_data["filters"]:
                case "location":
                    filters = "reserved_item__location"
                case "A-Z":
                    filters = Lower("reserved_item")
                case "type":
                    filters = "reserved_item__reservable_type"
                case _:
                    filters = form.cleaned_data["filters"]

        return Reservation.objects.filter(reservee_user=self.request.user).order_by(
            filters
        )

    def get_context_data(self, **kwargs):
        """Include the filter form in the context data."""
        context = super().get_context_data(**kwargs)
        context["form"] = FilterReservationForm(self.request.GET)
        return context


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """Reservation create view."""

    model = Reservation
    form_class = CreateReservationForm

    def get_form(self, *args, **kwargs):
        """Include the location in the form."""
        form = super().get_form(*args, **kwargs)
        form.fields["reserved_item"].queryset = ReservableItem.objects.filter(
            location=self.kwargs.get("location")
        )
        return form

    def form_valid(self, form):
        """Add the user who made the reservation to the Reservation instance."""
        form.instance.reservee_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Include the location in the context data."""
        context = super().get_context_data(**kwargs)
        context["location"] = self.kwargs.get("location")
        return context


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

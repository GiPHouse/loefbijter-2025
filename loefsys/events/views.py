"""Module defining the views for events."""

from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, FormView

from .exceptions import RegistrationError
from .forms import EventFieldsForm
from .models import Event, EventRegistration, RegistrationFormField


class EventView(DetailView):
    """View for viewing an event."""

    model = Event
    template_name = "events/event.html"
    event = None

    def get_object(self, queryset=None):  # noqa ARG002
        """Get event object based on url arguments."""
        if "pk" in self.kwargs:
            return get_object_or_404(Event, pk=self.kwargs["pk"])
        return get_object_or_404(Event, slug=self.kwargs["slug"])

    def post(self, request, *args, **kwargs):  # noqa ARG002
        """Handle the post request for the event view."""
        event = self.get_object()

        try:
            register = EventRegistration(
                event=event,
                contact=request.user,
                price_at_registration=event.price,
                fine_at_registration=event.fine,
                costs_paid=0.00,
            )
            register.save()
        except IntegrityError:
            # TODO handle the error
            print("Registration already exists")

        if event.has_form_fields:
            return redirect("events:registration", slug=event.slug)
        return redirect(event)


class RegistrationFormView(FormView):
    """View for the registration form."""

    template_name = "events/registration_form.html"
    form_class = EventFieldsForm
    event = None
    success_url = None

    def __get_registration(self, event, contact):
        """Get the registration for the event and contact."""
        try:
            registration = EventRegistration.objects.get(event=event, contact=contact)
        except EventRegistration.DoesNotExist as error:
            raise RegistrationError(
                _("You are not registered for this event.")
            ) from error
        except EventRegistration.MultipleObjectsReturned as error:
            raise RegistrationError(
                _("Unable to find the right registration.")
            ) from error

        return registration

    def get_form_kwargs(self):
        """Get form keyword arguments."""
        kwargs = super().get_form_kwargs()
        contact = self.request.user
        registration = self.__get_registration(self.event, contact)

        kwargs["form_fields"] = [
            (
                field.pk,
                {
                    "subject": field.subject,
                    "type": field.type,
                    "description": field.description,
                    "required": field.required,
                    "default": field.default,
                    "value": value,
                },
            )
            for field, value in registration.form_fields
        ]

        print("RegistrationFormView KWARGS:", kwargs["form_fields"])

        return kwargs

    def form_valid(self, form):
        """Check if form is valid."""
        values = form.field_values()
        registration = self.__get_registration(self.event, self.request.user)

        for field_id, field_value in values:
            print("field_id", field_id)
            print("field_value", field_value)
            field = RegistrationFormField.objects.get(id=field_id)
            field.set_value_for(registration, field_value)

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Return the proper response to a request."""
        self.event = get_object_or_404(Event, slug=self.kwargs["slug"])
        self.success_url = self.event.get_absolute_url()
        if self.event.has_form_fields:
            return super().dispatch(request, *args, **kwargs)

        return redirect(self.success_url)

class CalendarView(DetailView):

    def get(self, request):
        """Return the calendar view."""
        return render(request, "events/calendar.html")


class EventFillerView(View):
    """View for the event filler."""

    def get(self, request):
        """Get the events for the calendar."""
        events = Event.objects.all()
        data = []
        for event in events:
            if event.published:
                data.append(
                    {
                        "title": event.title,
                        "start": event.start,
                        "end": event.end,
                        "url": event.get_absolute_url()
                    }
                )
        return JsonResponse(data, safe=False)

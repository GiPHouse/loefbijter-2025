from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView


from .forms import EventFieldsForm
from .models import Event, RegistrationFormField, EventRegistration, RegistrationFormFieldResponse



class EventView(DetailView):
    model = Event
    template_name = "events/event.html"
    event = None

    def get_object(self, queryset=None):
        if "pk" in self.kwargs:
            return get_object_or_404(Event, pk=self.kwargs["pk"])
        return get_object_or_404(Event, slug=self.kwargs["slug"])

    def post(self, request, *args, **kwargs):
        """Handle the post request for the event view."""
        event = self.get_object()

        #TODO create registration object
        try:
            register = EventRegistration(event=event,
                                         contact=request.user,
                                         price_at_registration=event.price,
                                         fine_at_registration=event.fine,
                                         costs_paid=0.00)
            register.save()
        except IntegrityError:
            #TODO handle the error
            print("Registration already exists")

        if event.has_form_fields:
            return redirect("events:registration", pk=event.pk)
        return redirect(event)


class RegistrationFormView(FormView):
    template_name = "events/registration_form.html"
    form_class = EventFieldsForm
    event = None
    success_url = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        event = Event.objects.get(pk=self.kwargs["pk"])
        form_fields = RegistrationFormField.objects.filter(event=event)

        kwargs["form_fields"] = [
            (field.pk, {
                "subject": field.subject,
                "type": field.type,
                "description": field.description,
                "required": field.required,
                "default": field.default
            }) for field in form_fields
        ]

        return kwargs

    # def post(self, request, *args, **kwargs):
    #     _post = super().post(request, *args, **kwargs)
    #     return _post

    def form_valid(self, form):
        values = form.field_values()
        registration = EventRegistration.objects.get(event=self.event, contact=self.request.user)
        try:
            for value in values:
                response = RegistrationFormFieldResponse(
                    field=RegistrationFormField.objects.get(pk=value),
                    registration=registration,
                    response=value
                )
                response.save()
            # for field in values:
            #     response = RegistrationFormFieldResponse(
            #         field=field,
            #         registration=registration,
            #         response=values[field]
            #     )
        except IntegrityError:
            # TODO handle the error
            print("Response already exists")

        # validate values
        # update registration
        # success message
        # return redirect(self.event)
        # redirect back to event page
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs["pk"])
        self.success_url = self.event.get_absolute_url()
        print("i was executed")
        if self.event.has_form_fields:
            return super().dispatch(request, *args, **kwargs)

        return redirect(self.event)

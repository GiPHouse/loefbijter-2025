from .forms import EventFieldsForm
from .models import Event, RegistrationFormField
from django.views.generic import DetailView, FormView
from django.shortcuts import get_object_or_404, redirect


class EventView(DetailView):
    model = Event
    template_name = "events/event.html"

    def get_object(self, queryset=None):
        if "pk" in self.kwargs:
            return get_object_or_404(Event, pk=self.kwargs["pk"])
        return get_object_or_404(Event, slug=self.kwargs["slug"])

    # TODO: Register button should create registration before redirect!


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
        print("Form is valid")
        values = form.field_values()
        print(values)
        return super().form_valid(form)
        # validate values
        # update registration
        # success message
        # return redirect(self.event)
        # redirect back to event page

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs["pk"])
        self.success_url = f"/events/{self.event.pk}/"
        #TODO look into get_absolute_url

        if self.event.has_form_fields:
            return super().dispatch(request, *args, **kwargs)

        return redirect(self.event)
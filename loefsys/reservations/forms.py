"""Module defining the forms for the reservations."""

from django import forms

from .models import ReservableItem, Reservation


class CreateReservationForm(forms.ModelForm):
    """A form to create reservations."""

    reserved_item = forms.ModelChoiceField(queryset=ReservableItem.objects.all())
    start = forms.DateTimeField(
        input_formats=["%I:%M %p %d-%b-%Y"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%I:%M %p %d-%b-%Y"
        ),
    )
    end = forms.DateTimeField(
        input_formats=["%I:%M %p %d-%b-%Y"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%I:%M %p %d-%b-%Y"
        ),
    )

    class Meta:
        model = Reservation
        fields = ("reserved_item", "start", "end")


class FilterReservationForm(forms.Form):
    """A form to filter reservations."""

    CHOICES = (("start", "Option 1"), ("-end", "Option 2"))
    # CHOICES = (("start", "Option 1"), ("-end", "Option 2"), ("location", "Location"),
    # ("type", "Type of reservation"))
    filters = forms.ChoiceField(choices=CHOICES)
    # TODO Modify the Reservation class to include a location field, date of creation.

"""Module defining the forms for the reservations."""

from django import forms

from .models import ReservableItem, Reservation


class CreateReservationForm(forms.ModelForm):
    """A form to create reservations."""

    reserved_item = forms.ModelChoiceField(
        queryset=ReservableItem.objects.all(), widget=forms.RadioSelect
    )
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

    CHOICES = (
        ("start", "Starttijd"),
        ("-end", "Endtijd"),
        ("location", "Locatie"),
        ("-date_of_creation", "Nieuwste eerst"),
        ("A-Z", "A-Z"),
        ("type", "Type"),
    )
    filters = forms.ChoiceField(choices=CHOICES, required=False)

"""Module defining the forms for the reservations."""

from django import forms

from .models import ReservableItem, Reservation


class CreateReservationForm(forms.ModelForm):
    """A form to create reservations."""

    reserved_item = forms.ModelChoiceField(queryset=ReservableItem.objects.all())
    start = forms.DateField(
        widget=forms.widgets.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end = forms.DateField(
        widget=forms.widgets.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Reservation
        fields = ("reserved_item", "start", "end")

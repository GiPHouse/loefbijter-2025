"""Module defining the view for the index page."""

from datetime import datetime

from django.shortcuts import render

from loefsys.events.models import Event


def main(request):
    """View for loading the index page."""
    announcements = [
        {
            "header": "Vul je logboek in!",
            "text": "Je hebt je logboek voor Scylla van 11-11 nog niet ingevuld.",
        },
        {
            "header": "Zeilseizoen start weer!",
            "text": "Het zeilseizoen gaat weer van start",
        },
    ]
    events = Event.objects.all().filter(start__gte=datetime.now()).order_by("start")
    if request.user.is_active:
        events = events[:2]
    else:
        events = events.filter(published=True)[:2]
    return render(
        request, "main.html", {"announcements": announcements, "events": events}
    )

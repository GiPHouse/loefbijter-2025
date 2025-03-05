"""Module containing the views."""

from django.shortcuts import render


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
    return render(request, "main.html", {"announcements": announcements})

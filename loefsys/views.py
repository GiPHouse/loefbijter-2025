"""Module containing the views."""

from django.http import HttpResponse
from django.template import loader


def main(request):
    """View for loading the index page."""
    template = loader.get_template("main.html")
    return HttpResponse(template.render(request=request))

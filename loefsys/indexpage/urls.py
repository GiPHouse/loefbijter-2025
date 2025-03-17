"""Module containing the url definition of the index page."""

from django.urls import path

from . import views

urlpatterns = [path("", views.main, name="main")]

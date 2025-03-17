"""Module containing the url definition of the accountinformation page."""

from django.urls import path

from . import views

urlpatterns = [path("", views.accountinfo, name="accountinfo")]

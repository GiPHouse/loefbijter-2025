"""Module containing the url definition of the sign up page."""

from django.urls import path

from . import views

urlpatterns = [path("", views.signup, name="signup_page")]

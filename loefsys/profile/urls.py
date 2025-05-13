"""Module containing the url definition of the sign up page."""

from django.urls import path

from .views import SignupFormView

urlpatterns = [path("", SignupFormView.as_view(), name="signup_page")]

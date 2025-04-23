"""Module containing the url definition of the sign up page."""

from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.ProfileSignupView.as_view(), name="signup_page"),
    path("login/", views.ProfileLoginView.as_view(), name="profile-login"),
]

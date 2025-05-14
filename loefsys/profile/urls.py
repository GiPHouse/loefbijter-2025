"""Module containing the url definition of the sign up page."""

from django.urls import path

from .views import (
    ProfileLoginView,
    ProfilePasswordResetCompleteView,
    ProfilePasswordResetConfirmView,
    ProfilePasswordResetDoneView,
    ProfilePasswordResetView,
    ProfileSignupView,
)

urlpatterns = [
    path("signup/", ProfileSignupView.as_view(), name="signup"),
    path("login/", ProfileLoginView.as_view(), name="login"),
    path("password-reset/", ProfilePasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        ProfilePasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        ProfilePasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        ProfilePasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

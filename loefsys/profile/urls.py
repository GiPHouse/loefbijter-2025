"""Module containing the url definition of the sign up page."""

from django.urls import path

from .views import (
    ProfilePasswordResetView,
    ProfilePasswordResetDoneView,
    ProfilePasswordResetConfirmView,
    ProfilePasswordResetCompleteView,
)

urlpatterns = [
    path("signup/", views.ProfileSignupView.as_view(), name="signup"),
    path("login/", views.ProfileLoginView.as_view(), name="login"),
    path("password-reset/", ProfilePasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", ProfilePasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", ProfilePasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", ProfilePasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

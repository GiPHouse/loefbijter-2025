"""Module defining the view for the sign up page."""

from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.views.generic.edit import FormView

from .forms import SignupForm

import logging

logger = logging.getLogger("test_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


User = get_user_model()

class ProfileLoginView(LoginView):
    """View for logging in users."""

    next_page = "/account/"


class ProfileSignupView(FormView):
    """View for signing up users."""

    template_name = "signup.html"
    form_class = SignupForm
    success_url = "/profile/login/"

    def form_valid(self, form):
        """On valid credentials save the sign up data."""
        form.save()
        return super().form_valid(form)


# class ProfilePasswordResetView(PasswordResetView):
#     """View for requesting password change."""

#     template_name = "request_password_reset.html"
#     email_template_name = "reset_password_email.html"  # the email body
#     subject_template_name = "reset_password_subject.txt"  # the email subject line 
#     success_url = "/profile/password-reset/done/"


class ProfilePasswordResetView(PasswordResetView):
    """View for requesting password reset."""

    template_name = "request_password_reset.html"
    email_template_name = "reset_password_email.html"  # email body
    subject_template_name = "reset_password_subject.txt"  # email subject line 
    success_url = "/profile/password-reset/done/"


class ProfilePasswordResetDoneView(PasswordResetDoneView):
    """View for confirmation page after reseting password."""

    template_name = "password_reset_done.html"


class ProfilePasswordResetCompleteView(PasswordResetCompleteView):
    """View for when password reset has been completed."""

    template_name = "password_reset_complete.html"


class ProfilePasswordResetConfirmView(PasswordResetConfirmView):
    """View for entering a new password."""

    template_name = "password_reset_confirm.html"
    success_url = "/profile/password-reset/complete/"

    
class SignupFormView(FormView):
    """Sign up page view."""

    template_name = "signup.html"
    form_class = SignupForm
    success_url = "/"

    def form_valid(self, form):
        """Save the new user and log them in after a successful registration."""
        form.save()
        return super().form_valid(form)

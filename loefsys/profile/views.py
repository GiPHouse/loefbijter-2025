"""Module defining the view for the sign up page."""

from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView

from .forms import SignupForm


class ProfileLoginView(LoginView):
    """View for logging in users."""

    next_page = "/account/"


class ProfileSignupView(FormView):
    """View for signing up users."""

    template_name = "signup.html"
    form_class = SignupForm
    success_url = "/"

    def form_valid(self, form):
        """On valid credentials save the sign up data."""
        form.save()
        return super().form_valid(form)

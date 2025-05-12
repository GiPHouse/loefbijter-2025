"""Module defining the view for the sign up page."""

from django.views.generic import FormView

from .forms import SignupForm


class SignupFormView(FormView):
    """Sign up page view."""

    template_name = "signup.html"
    form_class = SignupForm
    success_url = "/"

    def form_valid(self, form):
        """Save the new user and log them in after a successful registration."""
        form.save()
        return super().form_valid(form)

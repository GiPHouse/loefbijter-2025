"""Module defining the view for the sign up page."""

from django.shortcuts import redirect, render

from .forms import SignupForm


def signup(request):
    """Sign up page view."""
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

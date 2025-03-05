"""Module containing the views."""

from django.shortcuts import redirect, render

from .profile.forms import SignupForm


def signup(request):
    """Sign up page view."""
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/admin/")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

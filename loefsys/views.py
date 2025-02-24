from django.http import HttpResponseRedirect  # noqa: D100
from django.shortcuts import render

from .profile.forms import SignupForm


def signup(request):
    """Sign up page view."""
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect("/admin/")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

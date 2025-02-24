"""A forms module to handle input for the sign up page."""

from django import forms


class SignupForm(forms.Form):
    """Sign up Form for email and password."""

    email = forms.CharField(label="email", max_length=100)
    password = forms.CharField(label="password", max_length=100)

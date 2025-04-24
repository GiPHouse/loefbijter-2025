"""Module containing the url definition of the accountinformation page."""

from django.urls import path

from .views import AccountinfoView, AccountinfoeditFormView

urlpatterns = [
    path("", AccountinfoView.as_view(), name="accountinfo"),
    path("edit", AccountinfoeditFormView.as_view(), name="accountinfoedit"),
]

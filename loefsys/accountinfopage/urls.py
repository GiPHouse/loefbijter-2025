"""Module containing the url definition of the accountinformation page."""

from django.urls import path

from .views import AccountinfoView, AccountinfoeditView

urlpatterns = [
    path("", AccountinfoView.as_view(), name="accountinfo"),
    path("edit", AccountinfoeditView.as_view(), name="accountinfoedit"),
]

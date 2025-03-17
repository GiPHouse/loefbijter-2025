"""Module containing the url definition of the loefsys web app."""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("loefsys.indexpage.urls")),
    path("admin/", admin.site.urls),
    path("signup/", include("loefsys.profile.urls")),
    path("account/", include("loefsys.accountinfopage.urls")),
    path("reservations/", include("loefsys.reservations.urls")),
    *debug_toolbar_urls(),
]

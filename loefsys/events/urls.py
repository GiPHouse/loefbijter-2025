from django.urls import path

from .views import EventView, RegistrationFormView

app_name = "events"

urlpatterns = [
    path("<int:pk>/", EventView.as_view(), name="event"),
    path("<slug:slug>/", EventView.as_view(), name="event"),
    # path("<int:pk>/register/", None, name="register"),
    # path("<slug:slug>/registration/cancel", None, name="cancel"),
    path("<slug:slug>/registration/", RegistrationFormView.as_view(), name="registration"),  # noqa: E501
]

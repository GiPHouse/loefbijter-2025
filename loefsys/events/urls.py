from django.urls import path

from .views import EventView, RegistrationFormView, CalendarView, EventFillerView   

app_name = "events"

urlpatterns = [
    path("<int:pk>/", EventView.as_view(), name="event"),
    path("<slug:slug>/", EventView.as_view(), name="event"),
    # path("<int:pk>/register/", None, name="register"),
    # path("<slug:slug>/registration/cancel", None, name="cancel"),
    path("<slug:slug>/registration/", RegistrationFormView.as_view(), name="registration"),  # noqa: E501
    path("", CalendarView.as_view(), name="events"),  # noqa: E501
    path("", EventFillerView.as_view(), name="event_filler"),  # noqa: E501 
]

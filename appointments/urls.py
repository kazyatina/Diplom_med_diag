from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("create/", views.create_appointment, name="create"),
    path(
        "<int:appointment_id>/cancel/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
]

from django.urls import path

from . import views

app_name = "accounts_api"

urlpatterns = [
    path("medical-history/", views.get_medical_history, name="medical_history_api"),
]

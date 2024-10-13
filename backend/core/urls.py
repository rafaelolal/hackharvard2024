from django.urls import path

from .views import (
    get_patient,
    get_suggestion,
    initialize_patient,
    start_recording,
    stop_recording,
    update_or_create_patient,
)

urlpatterns = [
    path("get_patient/<str:id>/", get_patient, name="get_patient"),
    path(
        "get_suggestion/<str:filename>/",
        get_suggestion,
        name="get_whisper_suggestions",
    ),
    path("initialize_patient/", initialize_patient, name="create_patient"),
    path("start_recording/", start_recording, name="start_recording"),
    path(
        "stop_recording/<str:recorder_id>/",
        stop_recording,
        name="stop_recording",
    ),
    path(
        "update_or_create_patient/",
        update_or_create_patient,
        name="update_or_create_patient",
    ),
]

from django.urls import path

from .views import (
    create_patient,
    get_patient,
    get_suggestion,
    initialize_patient,
    start_recording,
    stop_recording,
    update_patient,
)

urlpatterns = [
    path(
        "create_patient/<str:id>/",
        create_patient,
        name="create_patient",
    ),
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
    path("update_patient/<str:id>/", update_patient, name="update_patient"),
]

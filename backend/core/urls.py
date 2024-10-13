from django.urls import path

from .views import (
    create_patient,
    get_patient,
    get_whisper_suggestions,
    start_recording,
    stop_recording,
)

urlpatterns = [
    path("create_patient/", create_patient, name="create_patient"),
    path("get_patient/<str:patient_id>/", get_patient, name="get_patient"),
    path("start_recording/", start_recording, name="start_recording"),
    path(
        "stop_recording/<str:recorder_id>/",
        stop_recording,
        name="stop_recording",
    ),
    path(
        "get_whisper_suggestions/<str:filename>/",
        get_whisper_suggestions,
        name="get_whisper_suggestions",
    ),
]

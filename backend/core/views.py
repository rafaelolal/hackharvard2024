import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Patient
from .recorder import create_AR, process_AR, stop_AR, transcribe_AR

FHIR_SERVER_URL = settings.FHIR_SERVER_URL


@csrf_exempt
def create_patient(request, id):
    patient, created = Patient.objects.create(id=id)
    return JsonResponse({"success": True})


@csrf_exempt
# fetch(/update_patient/[id]/)
def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    data = request.POST.dict()
    transcription = data.get("transcription")
    data = data.get("data")
    patient.records.create(transcription=transcription, data=data)

    return JsonResponse({"success": True})


@csrf_exempt
def initialize_patient(request, id):
    patient, created = Patient.objects.get_or_create(id=id)
    data = {}

    # Fetch data from FHIR server
    data["mental_status"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={id}&code=72133-2"
    )
    data["hypotension"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={id}&code=85354-9"
    )
    data["kidney"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={id}&code=48642-3,48643-1"
    )
    data["hypoglycemia"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={id}&code=15074-8"
    )
    data["pressure_injury"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={id}&code=399912005"
    )
    data["skin_damage"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={id}&category=skin"
    )
    data["dehydration"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={id}&code=2951-2"
    )
    data["respirator_infection"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={id}&category=problem-list-item&code=50417007"
    )
    data["other_infection"] = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={id}&category=problem-list-item&clinical-status=active&verification-status=confirmed"
    )

    patient.records.create(transcription="", data=data)

    return JsonResponse({"success": True})


@csrf_exempt
def get_patient(request, id):
    patient = Patient.objects.get(id=id)
    latest_record = patient.records.latest("datetime")
    return JsonResponse({"data": latest_record.data})


@csrf_exempt
def start_recording(request):
    recorder_id = create_AR()
    return JsonResponse({"id": recorder_id})


@csrf_exempt
def stop_recording(request, recorder_id):
    filename = stop_AR(recorder_id)
    return JsonResponse({"filename": filename})


@csrf_exempt
def get_suggestion(request, filename):
    transcription = transcribe_AR(filename)
    suggestion = process_AR(transcription)
    return JsonResponse(
        {"suggestion": suggestion, "transcription": transcription}
    )


def fetch_fhir_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Process the FHIR response and extract relevant text
        # This is a simplified example; you may need to adjust based on the actual response structure
        return str(response.json())

    return ""

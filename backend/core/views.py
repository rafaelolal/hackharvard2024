import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Patient
from .recorder import create_AR, process_AR, stop_AR

FHIR_SERVER_URL = "http://localhost:8080/fhir"


@csrf_exempt
def create_patient(request, patient_id):
    patient, created = Patient.objects.get_or_create(id=patient_id)

    # Fetch data from FHIR server
    patient.mental_status = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={patient_id}&code=72133-2"
    )
    patient.hypotension = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={patient_id}&code=85354-9"
    )
    patient.kidney = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={patient_id}&code=48642-3,48643-1"
    )
    patient.hypoglycemia = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={patient_id}&code=15074-8"
    )
    patient.pressure_injury = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={patient_id}&code=399912005"
    )
    patient.skin_damage = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={patient_id}&category=skin"
    )
    patient.dehydration = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Observation?patient={patient_id}&code=2951-2"
    )
    patient.respirator_infection = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={patient_id}&category=problem-list-item&code=50417007"
    )
    patient.other_infection = fetch_fhir_data(
        f"{FHIR_SERVER_URL}/Condition?patient={patient_id}&category=problem-list-item&clinical-status=active&verification-status=confirmed"
    )

    patient.save()

    return JsonResponse(
        {
            "id": patient.id,
            "mental_status": patient.mental_status,
            "hypotension": patient.hypotension,
            "kidney": patient.kidney,
            "hypoglycemia": patient.hypoglycemia,
            "pressure_injury": patient.pressure_injury,
            "skin_damage": patient.skin_damage,
            "dehydration": patient.dehydration,
            "respirator_infection": patient.respirator_infection,
            "other_infection": patient.other_infection,
        }
    )


@csrf_exempt
def get_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    latest_record = patient.records.latest("datetime")
    return JsonResponse(latest_record.data)


@csrf_exempt
def start_recording(request):
    recorder_id = create_AR()
    return JsonResponse({"id": recorder_id})


@csrf_exempt
def stop_recording(request, recorder_id):
    filename = stop_AR(recorder_id)
    return JsonResponse({"filename": filename})


@csrf_exempt
def get_whisper_suggestions(request, filename):
    whisper_suggestion = process_AR(filename)
    return JsonResponse({"suggestion": whisper_suggestion})


def fetch_fhir_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Process the FHIR response and extract relevant text
        # This is a simplified example; you may need to adjust based on the actual response structure
        return str(response.json())

    return ""

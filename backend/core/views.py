import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Patient
from .recorder import create_AR, process_AR, stop_AR, transcribe_AR

FHIR_SERVER_URL = settings.FHIR_SERVER_URL


def process_fhir_searchset(response_data):
    result = ""
    total_items = response_data.get("total", 0)
    if total_items > 0 and "entry" in response_data:
        for entry in response_data["entry"]:
            resource = entry.get("resource", {})
            resource_type = resource.get("resourceType", "")

            if "effectiveDateTime" in resource:
                result += f"Date: {resource['effectiveDateTime']}\n"
            elif "onsetDateTime" in resource:
                result += f"Onset Date: {resource['onsetDateTime']}\n"

            if resource_type == "Observation":
                result += process_observation(resource)
            elif resource_type == "Condition":
                result += process_condition(resource)

            result += "\n"
    return result.strip()


def process_observation(resource):
    result = ""
    if "valueQuantity" in resource:
        value = resource["valueQuantity"]
        result += f"{resource.get('code', {}).get('text', 'Measurement')}: {value.get('value', 'Unknown')} {value.get('unit', '')}\n"
    elif "component" in resource:
        for component in resource["component"]:
            display = (
                component.get("code", {})
                .get("coding", [{}])[0]
                .get("display", "Unknown Measurement")
            )
            value = component.get("valueQuantity", {})
            result += f"{display}: {value.get('value', 'Unknown')} {value.get('unit', '')}\n"
    return result


def process_condition(resource):
    result = ""
    code = resource.get("code", {}).get("coding", [{}])[0]
    result += f"Condition: {code.get('display', 'Unknown Condition')}\n"
    if "clinicalStatus" in resource:
        result += f"Status: {resource['clinicalStatus'].get('coding', [{}])[0].get('display', 'Unknown')}\n"
    if "severity" in resource:
        result += f"Severity: {resource['severity'].get('coding', [{}])[0].get('display', 'Unknown')}\n"
    return result


def fetch_fhir_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Process the FHIR response and extract relevant text
        # This is a simplified example; you may need to adjust based on the actual response structure
        json = response.json()
        return process_fhir_searchset(json)

    return f"{response.status_code}"


def fetch_both_types(base_url, patient_id, obs_codes, cond_codes):
    obs_data = fetch_fhir_data(
        f"{base_url}/Observation?patient={patient_id}&code={','.join(obs_codes)}"
    )
    cond_data = fetch_fhir_data(
        f"{base_url}/Condition?patient={patient_id}&code={','.join(cond_codes)}"
    )
    return obs_data + "\n" + cond_data


@csrf_exempt
def initialize_patient(request, id):
    patient, created = Patient.objects.get_or_create(id=id)
    data = {}

    data["mental_status"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "72133-2",
            "72172-0",
            "9269-2",
            "74746-9",
            "75275-8",
            "80288-4",
            "11454-6",
        ],
        [],
    )

    data["hypotension"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "85354-9",
            "8462-4",
            "8480-6",
            # "8867-4",
            "8478-0",
            # "35094-2",
            # "55284-4",
            # "8310-5",
            # "8716-3",
        ],
        [],
    )

    data["kidney"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "48642-3",
            "48643-1",
            "2160-0",
            "3094-0",
            "9192-6",
            "14682-9",
            "32294-1",
            "51620-3",
            "33914-3",
        ],
        [],
    )

    data["hypoglycemia"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "15074-8",
            "4548-4",
            "1558-6",
            "8653-8",
            "2339-0",
            "2345-7",
            "41653-7",
            "55398-2",
        ],
        [],
    )

    data["pressure_injury"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        ["38228-3", "39105-6", "39125-4"],
        [
            "399912005",
            "225108008",
            "421038005",
            "421076003",
            "421893009",
            "421276004",
        ],
    )

    data["skin_damage"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [],  # ["39125-4", "39099-1", "39107-2"],
        ["271807003", "247441003", "225569009", "225573007", "225575000"],
    )

    data["dehydration"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "2951-2",
            "5811-5",
            "39099-1",
            "39095-9",
            "3141-9",
            "88660-6",
            "88661-4",
            "88662-2",
            "88663-0",
        ],
        [],
    )

    data["respiratory_infection"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "9279-1",
            # "2708-6",
            # "30954-2",
            # "8310-5",
            # "8867-4",
            # "19840-8",
            # "19835-8",
            # "19836-6",
        ],
        ["50417007"],
    )

    data["other_infection"] = fetch_both_types(
        FHIR_SERVER_URL,
        id,
        [
            "6690-2",
            "1988-5",
            "8310-5",
            "26464-8",
            "26465-5",
            "26466-3",
            "26467-1",
            "26468-9",
        ],
        [],
    )

    patient.records.create(transcription="", data=data)

    return JsonResponse({"success": True})


def check_patient_exists(patient_id):
    url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
    response = requests.get(url)
    return response.status_code == 200


@csrf_exempt
def create_patient(request, id):
    if check_patient_exists(id):
        return initialize_patient(request, id)

    Patient.objects.create(id=id)
    return JsonResponse({"success": True})


@csrf_exempt
def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    data = request.POST.dict()
    transcription = data.get("transcription")
    data = data.get("data")
    patient.records.create(transcription=transcription, data=data)

    return JsonResponse({"success": True})


@csrf_exempt
def get_patient(request, id):
    patient = Patient.objects.get(id=id)
    if not patient.records.exists():
        # create empty record
        # doesn't really make sense because records do not get updated
        patient.records.create(transcription="")

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

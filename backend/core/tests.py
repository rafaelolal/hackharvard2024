from django.test import Client, TestCase
from django.urls import reverse

from .models import Patient

# Create your tests here.


class InitializePatientTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.id = "18"
        self.url = reverse("initialize_patient", args=[self.id])

    def test_initialize_patient(self):
        # Make a POST request to the endpoint
        response = self.client.post(self.url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

        # Check that a Patient object was created
        patient = Patient.objects.get(id=self.id)
        self.assertIsNotNone(patient)

        # Check that a Record was created for the patient
        record = patient.records.first()
        self.assertIsNotNone(record)

        # Check that the Record has the expected data structure
        self.assertEqual(record.transcription, "")
        self.assertIn("mental_status", record.data)
        self.assertIn("hypotension", record.data)
        self.assertIn("kidney", record.data)
        self.assertIn("hypoglycemia", record.data)
        self.assertIn("pressure_injury", record.data)
        self.assertIn("skin_damage", record.data)
        self.assertIn("dehydration", record.data)
        self.assertIn("respiratory_infection", record.data)
        self.assertIn("other_infection", record.data)

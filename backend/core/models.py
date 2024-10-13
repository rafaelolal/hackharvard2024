from django.db import models

# Create your models here.


class Patient(models.Model):
    id = models.CharField(max_length=100, primary_key=True)


def get_default_data():
    return {
        "mental_status": "",
        "hypotension": "",
        "kidney": "",
        "hypoglycemia": "",
        "pressure_injury": "",
        "skin_damage": "",
        "dehydration": "",
        "respiratory_infection": "",
        "other_infection": "",
    }


class Record(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="records"
    )
    datetime = models.DateTimeField(auto_now_add=True)
    transcription = models.TextField()
    data = models.JSONField(default=get_default_data)

from django.db import models

# Create your models here.


class Patient(models.Model):
    id = models.CharField(max_length=100, primary_key=True)


class Record(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="records"
    )
    datetime = models.DateTimeField(auto_now_add=True)
    transcription = models.TextField()

    # format: {
    #     "mental_status": "",
    #     "hypotension": "",
    #     "kidney": ""
    #     "hypoglycemia": "",
    #     "pressure_injury": "",
    #     "skin_damage": "",
    #     "dehydration": "",
    #     "respirator_infection": "",
    #     "other_infection": "",
    # }
    data = models.JSONField()

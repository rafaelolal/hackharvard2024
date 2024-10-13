#!/bin/bash

for i in {1..10}
do
    echo "Generating and uploading patient $i of 10"

    # Run Synthea to generate patient data
    # Ensure the below file is executable by running  run_synthea
    ./run_synthea -p 1 --exporter.fhir.export=true

    # Find the most recently created files
    practitioner_file=$(ls -t output/fhir/practitionerInformation*.json | head -n1)
    hospital_file=$(ls -t output/fhir/hospitalInformation*.json | head -n1)
    patient_file=$(ls -t output/fhir/*.json | grep -v "practitionerInformation" | grep -v "hospitalInformation" | head -n1)

    # Upload practitioner information
    curl -X POST -H "Content-Type: application/fhir+json" -d @"$practitioner_file" http://localhost:8080/fhir

    # Upload hospital information
    curl -X POST -H "Content-Type: application/fhir+json" -d @"$hospital_file" http://localhost:8080/fhir

    # Upload patient information
    curl -X POST -H "Content-Type: application/fhir+json" -d @"$patient_file" http://localhost:8080/fhir

    echo "Patient $i data generated and uploaded successfully!"
    echo "---------------------------------------------------"
done

echo "All 10 patients have been generated and uploaded!"


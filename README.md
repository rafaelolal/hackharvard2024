# hackharvard2024

# Installation

* `brew install portaudio`
* `brew install ffmpeg`
* `python -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`
* .env variables needed
    * `OPENAI_API_KEY`
    * `RECORDING_FOLDER`
    * `WHISPER_MODEL`
    * `FHIR_SERVER_URL` (optional)
* `python manage.py runserver`

# API Endpoints

`/update_or_create_patient/[id]` -> `{success}`
`/initialize_patient/[id]` -> `{success}`
`/get_patient/[id]` -> `{data}`
`/start_recording` -> `{id}`
`/stop_recording/[id]` -> `{filename}`
`/get_suggestion/[filename]` -> `{suggestion, transcription}`
# hackharvard2024

# Installation

* `brew install portaudio`
* `brew install ffmpeg`
* `python[3] -m venv env`
* `source env/bin/activate` (MacOS)
* `pip install -r requirements.txt`
* Download a whisper model from `https://github.com/openai/whisper/blob/main/whisper/__init__.py`
* .env variables needed
    * `OPENAI_API_KEY`
    * `RECORDING_FOLDER`
    * `WHISPER_MODEL`
    * `FHIR_SERVER_URL` (optional)
* `python backend/manage.py migrate`
* `python backend/manage.py runserver`

# API Endpoints

`/update_or_create_patient/[id]` -> `{success}`
`/initialize_patient/[id]` -> `{success}`
`/get_patient/[id]` -> `{data}`
`/start_recording` -> `{id}`
`/stop_recording/[id]` -> `{filename}`
`/get_suggestion/[filename]` -> `{suggestion, transcription}`

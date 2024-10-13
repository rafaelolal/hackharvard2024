# hackharvard2024

# Installation

* `brew install portaudio`
* `brew install ffmpeg`
* `python -m venv env` (>=3.9 and <3.13)
* `source env/bin/activate` (Linux)
* `pip install -r requirements.txt`
* Download a whisper model from `https://github.com/openai/whisper/blob/main/whisper/__init__.py`
* .env variables needed
    * `OPENAI_API_KEY`
    * `RECORDING_FOLDER` (relative file location)
    * `WHISPER_MODEL` (relative file location)
    * `FHIR_SERVER_URL` (optional)
* `python backend/manage.py migrate`
* `python backend/manage.py runserver`

# API Endpoints

`/create_patient/[id]/` -> `{success}`
`/update_patient/[id]/` -> `{success}`
`/initialize_patient/[id]/` -> `{success}`
`/get_patient/[id]/` -> `{data}`
`/start_recording/` -> `{recorder_id}`
`/stop_recording/[id]/` -> `{filename}`
`/get_suggestion/[filename]/` -> `{suggestion, transcription}`

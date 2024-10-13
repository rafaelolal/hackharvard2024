const BASE = "http://127.0.0.1:8000/";
fetch(`${BASE}/start_recording`).then(response => {
    recorder_id = response.id
})

fetch(`${BASE}/stop_recording/${recorder_id}`).then(response => {
    filename = response.filename
})

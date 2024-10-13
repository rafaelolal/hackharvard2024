const BASE = "http://127.0.0.1:8000";
var recording = false;
var filename;
var recording_id;

function dummy_search(searchQuery) {
    console.log("User searched for: " + searchQuery)
    return [1, 2, 3, searchQuery]
}

searchInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the form from submitting
        searchButton.click(); // Trigger the button click action
    }
});

document.getElementById('searchButton').addEventListener('click', function () {
    event.preventDefault();
    let searchQuery = document.getElementById('searchInput').value;
    console.log(dummy_search(searchQuery));
    searchInput.value = "";
});

document.addEventListener('DOMContentLoaded', function () {
    rec_button = document.getElementById("rec_button");
    rec_icon = document.getElementById("rec_icon");
    rec_text = document.getElementById("rec_text");
    pull_button = document.getElementById("pull_button");
    audio_tscrpt = document.getElementById("audio_transcript");
    transcript_body = document.getElementById("transcript_body");
});

function record() {
    event.preventDefault();

    if (recording) {
        rec_button.className = "btn btn-success btn-icon-split";
        rec_icon.className = "far fa-play-circle";
        rec_text.innerHTML = "Start Recording";
        pull_button.className = "btn btn-primary btn-icon-split";
        stopRecording(recording_id);
    } else {
        rec_button.className = "btn btn-danger btn-icon-split";
        rec_icon.className = "far fa-pause-circle";
        rec_text.innerHTML = "Stop Recording";
        startRecording();
    }
    recording = !recording;
}

function pull() {
    event.preventDefault();
    if (pull_button.className == "btn btn-primary btn-icon-split") {
        var updates, transcript_log;
        pull_button.className = "btn btn-secondaryOff btn-icon-split disabled";
        fetch(`${BASE}/get_suggestion/${filename}/`,
            { method: "POST", headers: { "Content-Type": "application/json" }, })
            .then(response => response.json())
            .then(data => {
                updates = data.suggestion;
                transcript_log = data.transcription
                audio_tscrpt.style.display = "block";
                transcript_body.innerHTML = transcript_log;
            })
            .catch(error => { console.error('Error getting data:', error); });
    }
    return [updates, transcript_log];
}

function save() {
    event.preventDefault();
}

function newpt() {
    event.preventDefault();
}

function startRecording() {
    fetch(`${BASE}/start_recording/`, { method: 'POST', headers: { 'Content-Type': 'application/json', }, })
        .then(response => response.json())
        .then(data => { recording_id = data.id; })
        .catch(error => {
            console.error('Error starting recording:', error);
        });
}

function stopRecording(id) {
    fetch(`${BASE}/stop_recording/${id}/`,
        { method: 'POST', headers: { 'Content-Type': 'application/json' }, })
        .then(response => { console.log(response); return response.json() })
        .then(data => {
            filename = data.filename;
            console.log(filename)
        })
        .catch(error => {
            console.error('Error stopping recording:', error);
        });
    return filename;
}

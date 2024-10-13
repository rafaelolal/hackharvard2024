const BASE = "http://127.0.0.1:8000";
var recording = false;
var filename;
var recording_id;
var updates;
var transcript;


// function dummy_search(searchQuery) {
//     console.log("User searched for: " + searchQuery)
//     return [1,2,3,searchQuery]
// }

function set_data(data) {
    var card = document.getElementById("patientCard");
    if (data == "Not Found") {
        card.style.display = "block"; // Show Not Found Card
        return
    }
    card.style.display = "none"; // Hide Not Found Card
    console.log("got Data")


}

searchInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the page refresh
        searchButton.click(); // Trigger the button click action
    }
});

document.getElementById('searchButton').addEventListener('click', function () {
    event.preventDefault();
    let searchQuery = document.getElementById('searchInput').value;

    console.log("start")

    // fetch(`${BASE}/get_patient/${searchQuery}`).then(response => {
    //     if (response.status == 500){
    //         data = "Not Found";
    //     } else {
    //         data = response;
    //     }
    //     set_data(data)
    // });
    fetch(`http://127.0.0.1:8000/get_patient/${searchQuery}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log("mid")
            if (response.status == 500) {
                data = "Not Found";
            }
            set_data("Not Found");

            console.log("Patient Data");
            // You can store the recorder_id or use it as needed
        })
        .catch(error => {
            console.log("Patient Data Error Caught")
            set_data("Not Found");
        });
    searchInput.value = "";
    console.log("end")
});

// document.addEventListener('DOMContentLoaded', function () {
//     rec_button = document.getElementById("rec_button");
//     rec_icon = document.getElementById("rec_icon");
//     rec_text = document.getElementById("rec_text");
//     pull_button = document.getElementById("pull_button");
//     audio_tscrpt = document.getElementById("audio_transcript");
//     transcript_body = document.getElementById("transcript_body");
// });

async function record() {
    event.preventDefault();

    if (recording) {
        rec_button.className = "btn btn-success btn-icon-split";
        rec_icon.className = "far fa-play-circle";
        rec_text.innerHTML = "Start Recording";
        pull_button.className = "btn btn-primary btn-icon-split";
        const filename = await stopRecording(recording_id);
        [updates, transcript] = await processRecording(filename);
        audio_transcript.style.display = "block";
        transcript_body.innerHTML = transcript

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
                audio_transcript.style.display = "block";
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

async function stopRecording(id) {
    try {
        const response = await fetch(`${BASE}/stop_recording/${id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
        const data = await response.json();
        const filename = data.filename;  // Extract the filename
        return filename;  // Return the filename so it can be used in record()
    } catch (error) {
        console.error('Error stopping recording:', error);
        return null;  // Handle error and return null if something goes wrong
    }
}

async function processRecording(filename) {
    try {
        // Await the fetch call and response
        const response = await fetch(`${BASE}/get_suggestion/${filename}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });

        // Await parsing the response as JSON
        const data = await response.json();

        return [data.suggestion, data.transcription];

    } catch (error) {
        console.error('Error getting data:', error);
        return [null, null];  // Return nulls in case of error
    }
}

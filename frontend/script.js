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

    // Fill Text Boxes
    document.querySelector('#R1C1 textarea').value = data.mental_status ? data.mental_status : ""
    document.querySelector('#R1C2 textarea').value = data.hypotension ? data.hypotension : ""
    document.querySelector('#R1C3 textarea').value = data.kidney ? data.kidney : ""

    document.querySelector('#R2C1 textarea').value = data.hypoglycemia ? data.hypoglycemia : ""
    document.querySelector('#R2C2 textarea').value = data.pressure_injury ? data.pressure_injury : ""
    document.querySelector('#R2C3 textarea').value = data.skin_damage ? data.skin_damage : ""

    document.querySelector('#R3C1 textarea').value = data.dehydration ? data.dehydration : ""
    document.querySelector('#R3C2 textarea').value = data.respirator_infection ? data.respirator_infection : ""
    document.querySelector('#R3C3 textarea').value = data.other_infection ? data.other_infection : ""

}

document.addEventListener('DOMContentLoaded', function () {

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
        fetch(`http://127.0.0.1:8000/get_patient/${searchQuery}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log("mid")
                // if (response.status == 500) {
                //     data = "Not Found";
                // }
                set_data(data);

                console.log("Patient Data");
                // You can store the recorder_id or use it as needed
            })
            .catch(error => {
                console.log("Patient Data Error Caught", error)
                set_data("Not Found");
            });
        searchInput.value = "";
        console.log("end")
    });

    document.getElementById("newpt_id").addEventListener('keydown', function (e) {
        // Block 'e', 'E', '+', '-', '.' from being typed in
        if (e.key === 'e' || e.key === 'E' || e.key === '+' || e.key === '-' || e.key === '.') {
            e.preventDefault();  // Prevent the character from being entered
        }
    });

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
        audio_transcript.style.display = "none";

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

async function newpt(event) {
    event.preventDefault();

    try {
        const response = await fetch(`${BASE}/create_patient/${newpt_id.value}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
        const data = await response.json();
        console.log(data)
    } catch (error) {
        create_newpt.className = "btn btn-danger";
        setTimeout(() => { create_newpt.className = "btn btn-primary"; }, 2000); // 2000 milliseconds (2 seconds)
    }

    fetch(`http://127.0.0.1:8000/get_patient/${searchQuery}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log("mid")
            // if (response.status == 500) {
            //     data = "Not Found";
            // }
            set_data(data);

            console.log("Patient Data");
            // You can store the recorder_id or use it as needed
        })
        .catch(error => {
            console.log("Patient Data Error Caught", error)
            set_data("Not Found");
        });
    searchInput.value = "";

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

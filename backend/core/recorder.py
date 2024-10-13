import threading

import pyaudio
import whisper
from django.conf import settings
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key=settings.OPENAI_API_KEY)
RECORDINGS_FOLDER = "../../recordings"


class AudioRecorder:
    def __init__(self, channels=1, rate=44100, chunk=1024):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        if not self.is_recording:
            # Start the PyAudio stream
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
            )
            self.is_recording = True
            print("Recording started...")
            # Start recording in a separate thread to allow non-blocking behavior
            self.recording_thread = threading.Thread(target=self._record)
            self.recording_thread.start()

    def _record(self):
        # Continuously record audio chunks until stopped
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self, id):
        if self.is_recording:
            self.is_recording = False
            # Wait for the recording thread to finish
            self.recording_thread.join()

            # Stop and close the stream
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            print("Recording stopped.")

            # Save the recorded data as an MP3 file
            audio_segment = AudioSegment(
                data=b"".join(self.frames),
                sample_width=self.audio.get_sample_size(pyaudio.paInt16),
                frame_rate=self.rate,
                channels=self.channels,
            )

            filename = f"{id}.mp3"
            audio_segment.export(f"{RECORDINGS_FOLDER}/{filename}", format="mp3")
            print(f"Audio saved as {RECORDINGS_FOLDER}/{filename}")
            return filename


recordings = dict()


def create_AR():
    recorder = AudioRecorder()
    id = hash(recorder)
    recordings[id] = recorder
    recorder.start_recording()
    return id


def stop_AR(id):
    return recordings[id].stop_recording(id)


def transcribe_AR(filename):
    model = whisper.load_model("../../tiny.pt")
    result = model.transcribe(f"{RECORDINGS_FOLDER}/{filename}")
    transcription = result["text"]
    return transcription

def process_AR(transcription):
    # ChatGPT prompt
    prompt = (
        """Given the following text, provide any information that was stated regarding the
    categories of mental status, hypotension, kidney, hypoglycemia, pressure injury, skin damage,
    dehydration, respirator infection, other infection: \""""
        + transcription
        + """\" Return your
    answer in the form below, leaving unmentioned categories as empty strings:
        format: {
         "mental_status": "",
         "hypotension": "",
         "kidney": ""
         "hypoglycemia": "",
         "pressure_injury": "",
         "skin_damage": "",
         "dehydration": "",
         "respirator_infection": "",
         "other_infection": "",
     }"""
    )

    messages2 = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        messages=messages2, model="gpt-4", max_tokens=150, temperature=0.7
    )

    return response.choices[0].message.content

# ar = AudioRecorder()
# id = ar.start_recording()
# import time
# time.sleep(7)
# filename = ar.stop_recording(id)
# transcription = transcribe_AR(filename)
# print(transcription)
# print(process_AR(transcription))

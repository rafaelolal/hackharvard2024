import whisper
import pyaudio
from pydub import AudioSegment
import threading



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
            self.stream = self.audio.open(format=pyaudio.paInt16, channels=self.channels,
                                          rate=self.rate, input=True,
                                          frames_per_buffer=self.chunk)
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
                data=b''.join(self.frames),
                sample_width=self.audio.get_sample_size(pyaudio.paInt16),
                frame_rate=self.rate,
                channels=self.channels
            )

            filename = f"{id}.mp3"
            audio_segment.export(f"./{filename}", format="mp3")
            print(f"Audio saved as {filename}")
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

def process_AR(filename):
    model = whisper.load_model("base")  # Change the model size if needed
    result = model.transcribe(f"./{filename}")  # Replace with your file path
    print(result["text"]) # Output the transcribed text


ar = AudioRecorder()
id = ar.start_recording()
import time
time.sleep(6)
ar.stop_recording(id)

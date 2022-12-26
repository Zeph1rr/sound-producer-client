import json

import pyaudio
import wave
import requests

from requests_toolbelt import MultipartEncoder
from vosk import Model, KaldiRecognizer, SpkModel
from time import time
from os import makedirs
from os.path import join, exists, dirname, abspath

from ui import ClientUI


class App:
    def __init__(self):
        self.ui = ClientUI()
        self.frames = []
        self.is_recording = False
        self.current_record_time = 0
        self.stream_opened_time = 0
        self.message = ''
        self.prepared_data = {}
        self.file = ''
        self.is_creating_speaker = False
        self.recognizing_result = {}

        self.audio = None
        self.stream = None

        self.recognizer = self.__init_recognizer()

    def __init_recognizer(self):
        model = Model(join(dirname(abspath(__file__)), "assets", "models", "recognizing_model"))
        spk_model = SpkModel(join(dirname(abspath(__file__)), "assets", "models", "speaker_model"))
        recognizer = KaldiRecognizer(model, 44100)
        recognizer.SetSpkModel(spk_model)
        return recognizer

    def open_audio_stream(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )
        self.stream_opened_time = time()
        self.frames = []

    def close_audio_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_speaker_data(self):
        if not exists("speakers"):
            makedirs("speakers")
        if not self.recognizing_result['spk']:
            return False
        save_data = {"spk": self.recognizing_result["spk"], "speaker": self.ui.nickname.get()}
        with open(join("speakers", self.ui.nickname.get() + ".json"), 'w') as file:
            json.dump(save_data, file, indent=4, ensure_ascii=False)
        return True

    def record(self):
        if self.is_recording:
            frame = self.stream.read(1024, exception_on_overflow=False)
            self.frames.append(frame)
            self.ui.root.after(1, self.record)
            passed = time() - self.stream_opened_time
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
        else:
            self.close_audio_stream()
            if self.recognize():
                self.prepare_data()
            if self.is_creating_speaker:
                print(self.save_speaker_data())
                return
            self.save_file()
            secs, mins, hours = 0, 0, 0
        self.ui.current_time_label.config(
            text=f"Current record length: {int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
        )

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        self.ui.record_button['text'] = "Stop recording" if self.is_recording else "Start recording"
        if self.is_recording:
            self.open_audio_stream()
            self.record()

    def prepare_data(self):
        self.prepared_data = {
            'nickname': (None, self.ui.nickname.get())
        }

    def send_data(self):
        url = "http://" + self.ui.url.get() + ":65525"
        response = requests.post(url, data=self.recognizing_result, files=self.prepared_data)
        if not response.ok:
            self.ui.status_label.config(text=response.text, foreground="#FF0000")
        else:
            self.ui.status_label.config(text="Successfully sent!", foreground="#006400")

    def create_speaker(self):
        self.is_creating_speaker = True
        self.toggle_recording()

    def save_file(self, path: str = None, file_name: str = None):
        if not path:
            path = "records"
        if not file_name:
            file_name = f'{self.ui.nickname.get()}_{time()}.wav'
        file_name = join(path, file_name)
        if not exists(path):
            makedirs(path)
        sound_file = wave.open(file_name, 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(self.frames))
        sound_file.close()
        self.ui.current_file_label['text'] = "Last file: " + file_name
        self.file = file_name

    def recognize(self):
        self.recognizing_result = {}
        data = b''.join(self.frames)
        if len(data) == 0:
            print("len")
            return False
        if not self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.PartialResult())
            text = result.get('partial')
        else:
            result = json.loads(self.recognizer.Result())
            text = result.get('text')
        spk = result.get('spk', [])
        spk_frames = result.get('spk_frames', 0)

        self.recognizing_result = {"spk": spk, "spk_frames": spk_frames, 'message': text}
        return True

    def start_app(self):
        self.ui.record_button["command"] = self.toggle_recording
        self.ui.send_data_button["command"] = self.send_data
        self.ui.create_speaker_button["command"] = self.create_speaker
        self.ui.mainloop()

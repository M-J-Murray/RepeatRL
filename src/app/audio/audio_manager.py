import math
import os
import wave
import pyaudio
from collections import deque, OrderedDict


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


class AudioManager(object):

    def __init__(self, save_dir, rate=44100, chunk=1024):
        self.save_dir = save_dir
        self.py_audio = pyaudio.PyAudio()
        self.rate = rate
        self.chunk = chunk
        self.format_bytes = 2
        self.mic = None
        self.speaker = None

        self.is_recording = False
        self.recording_chunks = []

        self.is_playing = False
        self.playback_chunks = None
        self.on_complete = None

        self.audio_files = []
        self.unsaved_audio = OrderedDict()

        self.check_for_saved_audio()

    def check_for_saved_audio(self):
        for f in os.listdir(self.save_dir):
            path = os.path.join(self.save_dir, f)
            if os.path.isfile(path):
                self.audio_files.append(f[:-4])

    def create_speaker_stream(self, callback=None):
        return self.py_audio.open(rate=self.rate, format=pyaudio.paInt16, channels=1, output=True,
                                  frames_per_buffer=self.chunk, stream_callback=callback)

    def create_microphone_stream(self, callback=None):
        return self.py_audio.open(rate=self.rate, format=pyaudio.paInt16, channels=1, input=True, input_device_index=1,
                                  frames_per_buffer=self.chunk, stream_callback=callback)

    def record_callback(self, in_data, frame_count, time_info, status):
        self.recording_chunks.append(in_data)
        return in_data, pyaudio.paContinue

    def playback_callback(self, in_data, frame_count, time_info, status):
        if len(self.playback_chunks) == 0:
            if self.on_complete is not None:
                self.on_complete()
            self.is_playing = False
            self.on_complete = None
            return b'', pyaudio.paComplete
        else:
            chunk_data = self.playback_chunks.popleft()
            return chunk_data, pyaudio.paContinue

    def start_recording(self):
        if self.is_recording:
            raise Exception("Attempted to start recording that is already running")
        self.recording_chunks = []
        self.mic = self.create_microphone_stream(callback=self.record_callback)
        self.mic.start_stream()
        self.is_recording = True

    def all_audio_ids(self):
        return list(self.unsaved_audio.keys()) + self.audio_files

    def generate_next_name(self):
        greatest = 0
        for audio_id in self.all_audio_ids():
            if audio_id[:10] == "Recording " and is_int(audio_id[10:len(audio_id)]):
                value = int(audio_id[10:len(audio_id)])
                if value > greatest:
                    greatest = value

        return "Recording " + str(greatest + 1)

    def stop_recording(self):
        if not self.is_recording:
            raise Exception("Attempted to stop recording when none recording")
        self.mic.stop_stream()
        self.mic.close()
        del self.mic
        final_audio = b''.join(self.recording_chunks)
        del self.recording_chunks
        self.unsaved_audio[self.generate_next_name()] = final_audio
        self.is_recording = False

    def rename_audio(self, audio_id, new_id):
        if audio_id in self.unsaved_audio:
            if new_id in self.all_audio_ids():
                raise Exception("New audio name is already taken")
            else:
                self.unsaved_audio[new_id] = self.unsaved_audio[audio_id]
                del self.unsaved_audio[audio_id]
        else:
            if new_id in self.all_audio_ids():
                raise Exception("New audio name is already taken")
            else:
                os.rename(self.save_dir + "/" + audio_id + ".wav",
                          self.save_dir + "/" + new_id + ".wav")
                self.audio_files[self.audio_files.index(audio_id)] = new_id

    def play_audio(self, audio_id, on_complete=None):
        if self.is_playing:
            self.stop_audio()
        self.is_playing = True
        if audio_id in self.unsaved_audio:
            audio_data = self.unsaved_audio[audio_id]
        else:
            audio_data = self.load_audio(audio_id)
        n_chunks = math.ceil(len(audio_data) / (self.format_bytes * self.chunk))
        self.playback_chunks = deque(maxlen=n_chunks)
        for i in range(n_chunks):
            if i < n_chunks - 1:
                self.playback_chunks.append(audio_data[i * self.format_bytes * self.chunk:(i + 1) * self.format_bytes * self.chunk])
            else:
                remaining = audio_data[i * self.format_bytes * self.chunk:len(audio_data)]
                if len(remaining) < self.format_bytes * self.chunk:
                    remaining += b'0' * ((self.format_bytes * self.chunk) - len(remaining))
                self.playback_chunks.append(remaining)
        self.on_complete = on_complete
        self.speaker = self.create_speaker_stream(callback=self.playback_callback)
        self.speaker.start_stream()

    def stop_audio(self):
        if not self.is_playing:
            raise Exception("Attempted to stop audio when no audio playing")
        self.speaker.stop_stream()
        self.speaker.close()
        del self.speaker
        del self.playback_chunks
        if self.on_complete is not None:
            self.on_complete()
        self.is_playing = False
        self.on_complete = None

    def save_all(self):
        for audio_id in set(self.unsaved_audio):
            self.save_audio(audio_id)

    def is_saved(self, audio_id):
        return os.path.isfile(self.save_dir + "/" + audio_id + ".wav")

    def save_audio(self, audio_id):
        audio_file = wave.open(self.save_dir + "/" + audio_id + ".wav", 'wb')
        audio_file.setnchannels(1)
        audio_file.setsampwidth(self.py_audio.get_sample_size(pyaudio.paInt16))
        audio_file.setframerate(self.rate)
        audio_file.writeframes(self.unsaved_audio[audio_id])
        audio_file.close()
        del self.unsaved_audio[audio_id]
        self.audio_files.append(audio_id)

    def load_audio(self, audio_id):
        audio_file = wave.open(self.save_dir + "/" + audio_id + ".wav", 'rb')
        audio_data = audio_file.readframes(audio_file.getnframes())
        audio_file.close()
        return audio_data

    def shutdown(self):
        self.py_audio.terminate()

    def delete_audio(self, audio_id):
        if audio_id in self.unsaved_audio:
            del self.unsaved_audio[audio_id]
        else:
            os.remove(self.save_dir + "/" + audio_id + ".wav")
            del self.audio_files[self.audio_files.index(audio_id)]

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

RATE = 8000
CHUNK = 800
T = 5

volume = 0.5


def speaker_stream():
    return p.open(rate=RATE, format=pyaudio.paInt16, channels=1, output=True, frames_per_buffer=CHUNK)


def microphone_stream():
    return p.open(rate=RATE, format=pyaudio.paInt16, channels=1, input=True, input_device_index=1,
                  frames_per_buffer=CHUNK)


def main():
    speaker = speaker_stream()
    mic = microphone_stream()

    print("mic latency: %.2fs, speaker latency: %.2fs, total: %.2fs" % (
        mic.get_input_latency(), speaker.get_output_latency(), mic.get_input_latency() + speaker.get_output_latency()))
    mic.get_input_latency()

    for i in range(0, int(RATE / CHUNK * T)):
        audio_bytes = mic.read(CHUNK)
        data = np.frombuffer(audio_bytes, dtype=np.int16)
        speaker.write(audio_bytes)

    mic.stop_stream()
    mic.close()
    speaker.stop_stream()
    speaker.close()

    p.terminate()


if __name__ == '__main__':
    main()

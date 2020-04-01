import numpy as np
import pyaudio

p = pyaudio.PyAudio()

RATE = 2000
CHUNK = 200
T = 2

hz = 490
volume = 0.5


def main():
    print(p.get_default_host_api_info())
    speaker = p.open(rate=RATE, format=pyaudio.paInt16, channels=1, output=True, frames_per_buffer=CHUNK)

    t = np.arange(0, T, 1 / RATE)
    x = volume * np.sin(2 * np.pi * hz * t)
    x = (x * 32768).astype(np.int16)  # Normalises to frame range
    speaker.write(x.tobytes())

    speaker.stop_stream()
    speaker.close()

    p.terminate()


if __name__ == '__main__':
    main()

import simpleaudio as sa
import numpy as np
from scipy.io import wavfile


def play_wav(file_path):
    sample_rate, audio_data = wavfile.read("src/audio/Brent-240930110056.wav")

    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

    # Create a WaveObject from the PCM data
    wave_obj = sa.WaveObject(
        audio_data.tobytes(),
        num_channels=1,
        bytes_per_sample=2,
        sample_rate=sample_rate,
    )

    # Play the audio
    play_obj = wave_obj.play()
    play_obj.wait_done()

    play_obj.stop()

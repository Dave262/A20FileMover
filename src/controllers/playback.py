import sounddevice as sd
import soundfile as sf
import subprocess
import numpy as np
from threading import Event

# ----------------------------------
# Working, but overy complicated
# ----------------------------------


# Global variables to hold the subprocess and stop event
current_song_process = None
stop_event = Event()


def play_audio(file_path):
    global current_song_process
    stop_event.clear()  # Clear the stop event at the start of playback

    CHUNK = 1024  # Define the chunk size for reading the audio file
    try:
        # Set up ffmpeg subprocess to convert audio format and stream data
        current_song_process = subprocess.Popen(
            [
                "ffmpeg",
                "-i",
                file_path,
                "-loglevel",
                "panic",
                "-vn",
                "-f",
                "s16le",
                "pipe:1",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # Capture stderr for error messages
        )

        # Check if the subprocess was created successfully
        if current_song_process.stdout is None:
            error_message = current_song_process.stderr.read().decode()
            print(f"FFmpeg error: {error_message}")
            return

        # Use soundfile to read the file properties (sample rate, channels, etc.)
        with sf.SoundFile(file_path) as f:
            samplerate = f.samplerate
            channels = f.channels

        # Create a stream with sounddevice using the specified format
        with sd.OutputStream(
            samplerate=samplerate, channels=channels, dtype="int16"
        ) as stream:
            # Read and play the audio data in chunks
            while not stop_event.is_set():
                data = current_song_process.stdout.read(CHUNK)
                if not data:
                    break
                # Convert bytes data to numpy array for sounddevice
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                stream.write(audio_chunk)
    except Exception as e:
        print(f"Error during audio playback: {e}")
    finally:
        if current_song_process is not None:
            current_song_process.terminate()
            current_song_process = None
        print("Playback finished or stopped.")


def stop_audio():
    stop_event.set()  # Signal the playback loop to stop
    if current_song_process is not None:
        current_song_process.terminate()  # Terminate the ffmpeg process
        print("Audio playback stopped.")

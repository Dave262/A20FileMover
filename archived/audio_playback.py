import pyaudio
import soundfile as sf
import signal
import sys
import threading


class AudioPlay:
    chunk = 512  # Number of frames per chunk

    def __init__(self, file, update_slider_callback=None):
        self.lock = threading.Lock()
        """ Init audio stream """
        self.data, self.samplerate = sf.read(file, dtype="float32")
        print("Sample rate:", self.samplerate)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=self.data.shape[1] if len(self.data.shape) > 1 else 1,
            rate=self.samplerate,
            output=True,
        )
        self.position = 0  # To keep track of playback position
        self.is_playing = False  # Flag to control playback
        self.update_slider_callback = update_slider_callback

    def play(self):
        """Play entire file in chunks"""
        self.is_playing = True
        try:
            while self.position < len(self.data) and self.is_playing:
                with self.lock:  # Ensure thread-safe access to the stream
                    if not self.is_playing:
                        break
                    # Calculate the next chunk
                    end_position = self.position + self.chunk
                    data_chunk = self.data[self.position : end_position].tobytes()

                    # Write chunk to stream
                    self.stream.write(data_chunk)

                    # Update position
                    self.position = end_position

                    # Update slider
                    if self.update_slider_callback:
                        self.update_slider_callback(
                            self.position / len(self.data) * 100
                        )

            with self.lock:
                if self.stream.is_active():
                    self.stream.stop_stream()

        except KeyboardInterrupt:
            print("Playback interrupted by user.")
        finally:
            print("Playback finished or stopped.")

    def stop(self):
        """Stop playback"""
        print("stopping playback")
        with self.lock:
            self.is_playing = False
            if self.stream.is_active():
                self.stream.stop_stream()

    def close(self):
        """Graceful shutdown"""
        with self.lock:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

    def signal_handler(sig, frame):
        print("Signal received, stopping playback.")
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

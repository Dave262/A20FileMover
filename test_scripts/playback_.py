import subprocess
import time


class AudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.process = None

    def start(self):
        if self.process is None:
            # Start playback using ffplay
            self.process = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", self.file_path]
            )
            print("Playback started.")
        else:
            print("Playback already in progress.")

    def stop(self):
        if self.process:
            # Stop playback by terminating the ffplay process
            self.process.terminate()
            self.process = None
            print("Playback stopped.")
        else:
            print("No playback to stop.")

    def rewind(self, seconds):
        # Rewinds by restarting playback from an earlier time
        self._seek(-seconds)

    def fast_forward(self, seconds):
        # Fast-forwards by restarting playback from a later time
        self._seek(seconds)

    def _seek(self, offset_seconds):
        # To achieve seeking, stop playback, calculate the new starting time, and restart from there
        if self.process:
            self.stop()  # Stop current playback

        # Calculate the new start time
        seek_time = max(0, offset_seconds)
        # Start playback from the specified seek time
        self.process = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-ss",
                str(seek_time),
                "-loglevel",
                "error",
                self.file_path,
            ]
        )
        print(f"Playback started from {seek_time} seconds.")


# Example usage
if __name__ == "__main__":
    player = AudioPlayer("src/audio/Labour Day_July 2024.wav")

    # Start playback
    player.start()
    time.sleep(5)  # Playback for 5 seconds

    # Fast-forward by 10 seconds
    player.fast_forward(10)
    time.sleep(5)  # Playback for another 5 seconds

    # Stop playback
    player.stop()

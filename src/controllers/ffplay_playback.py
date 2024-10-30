import customtkinter as ctk
import subprocess
import threading
import time
from datetime import datetime, timedelta


class AudioPlayer:
    def __init__(self, file_path, playhead_slider, playtime_label, timecode_label):
        self.file_path = file_path
        self.process = None
        self.duration = self._get_duration()  # Total duration of the file
        self.timecode = self._get_timecode()
        self.playhead_slider = playhead_slider
        self.playtime_label = playtime_label
        self.timecode_label = timecode_label
        self.current_seek = 0  # Track the current playback position

        # Bind slider movement to a callback
        self.playhead_slider.configure(command=self.seek_from_slider)

    def _get_timecode(self):
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format_tags=creation_time",
                "-of",
                "csv=p=0",
                self.file_path,
            ],
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():  # Only print if creation_time data is found
            result = result.stdout.strip()
            print("Start Timecode (Creation Time):", result)
            return result
        else:
            print("No start timecode found in file.")
            return None

    def _get_duration(self):
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                self.file_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        return float(result.stdout) if result.stdout else 0

    def get_duration_as_hms(self):
        duration_in_seconds = self._get_duration()
        hours, remainder = divmod(duration_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return int(hours), int(minutes), seconds

    def print_duration(self):
        hours, minutes, seconds = self.get_duration_as_hms()
        print(f"Duration: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    def start(self):
        # Start playback from the current seek time
        self._play_from(self.current_seek)
        print("Playback started.")
        threading.Thread(target=self._update_playtime, daemon=True).start()
        threading.Thread(
            target=self._update_timecode, args=(self.timecode,), daemon=True
        ).start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            print("Playback stopped.")

    def seek_from_slider(self, slider_value):
        """Adjust current seek based on slider (0-100 scale) and restart playback."""
        if self.process:
            self.stop()  # Stop current playback
        self.current_seek = (slider_value / 100) * self.duration
        self._play_from(self.current_seek)  # Start playback from new position
        print("resumed")

    def _play_from(self, start_time):
        """Start ffplay from a specific timestamp."""
        print("_play_from")
        self.process = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-ss",
                str(start_time),
                "-loglevel",
                "error",
                self.file_path,
            ]
        )
        self.start_time = time.time() - start_time  # Set start time for tracking
        threading.Thread(target=self._update_slider, daemon=True).start()

    def _update_slider(self):
        while self.process and self.process.poll() is None:
            elapsed = time.time() - self.start_time
            slider_position = (elapsed / self.duration) * 100
            self.playhead_slider.set(min(slider_position, 100))
            time.sleep(0.5)

    def _update_playtime(self):
        while self.process and self.process.poll() is None:
            elapsed = time.time() - self.start_time
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.playtime_label.configure(
                text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            )
            time.sleep(1)

    def _update_timecode(self, creation_time_str):
        if creation_time_str is None:
            start_timecode = datetime.strptime("00:00:00", "%H:%M:%S")
        else:
            start_timecode = datetime.strptime(creation_time_str, "%H:%M:%S")

        while self.process and self.process.poll() is None:
            elapsed = time.time() - self.start_time
            current_timecode = start_timecode + timedelta(seconds=elapsed)

            self.timecode_label.configure(text=current_timecode.strftime("%H:%M:%S"))
            time.sleep(1)


# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    playhead_slider = ctk.CTkSlider(root, from_=0, to=100)
    playhead_slider.pack(fill="x", expand=True, pady=20, padx=20)
    playhead_slider.set(0)

    playtime_label = ctk.CTkLabel(root, text="00:00:00")
    playtime_label.pack(pady=10)

    timecode_label = ctk.CTkLabel(root, text="00:00:00")
    timecode_label.pack(pady=10)

    player = AudioPlayer(
        "src/audio/Brent-240708234433.wav",
        playhead_slider,
        playtime_label,
        timecode_label,
    )
    player.print_duration()

    play_button = ctk.CTkButton(root, text="Play", command=player.start)
    play_button.pack(pady=10)

    stop_button = ctk.CTkButton(root, text="Stop", command=player.stop)
    stop_button.pack(pady=10)

    root.mainloop()

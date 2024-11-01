import customtkinter as ctk
import subprocess
import threading
import time
from datetime import datetime, timedelta

class AudioPlayer:
    def __init__(self, file_path, playhead_slider, playtime_label, timecode_label):
        self.file_path = file_path
        self.process = None
        self.duration = self._get_duration()
        self.timecode = self._get_timecode()
        self.playhead_slider = playhead_slider
        self.playtime_label = playtime_label
        self.timecode_label = timecode_label
        self.current_seek = 0
        self.stop_event = threading.Event()
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

        if result.stdout.strip():
            return result.stdout.strip()
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
            text=True
        )
        try:
            return float(result.stdout.strip())
        except ValueError:
            print("Could not determine duration.")
            return 0

    def start(self):
        time.sleep(0.01) # delaying start a tiny bit stops breakages??
        self.stop()  # Stop any ongoing playback before starting
        self._play_from(self.current_seek)
        self.stop_event.clear()
        self._restart_update_threads()

    def stop(self):
        self.stop_event.set()  # Signal threads to stop
        if self.process:
            self.process.terminate()
            self.process = None
            print("Playback stopped.")

    def seek_from_slider(self, slider_value):
        print("seeking")
        self.current_seek = (slider_value / 100) * self.duration
        self.start()  # Restart playback from new position

    def _play_from(self, start_time):
        print("playing from")
        self.process = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-ss", str(start_time), "-loglevel", "error", self.file_path]
        )
        self.start_time = time.time() - start_time

    def _restart_update_threads(self):
        threading.Thread(target=self._update_slider, daemon=True).start()
        threading.Thread(target=self._update_playtime, daemon=True).start()
        threading.Thread(target=self._update_timecode, args=(self.timecode,), daemon=True).start()

    def _update_slider(self):
        while self.process and not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            slider_position = (elapsed / self.duration) * 100
            self.playhead_slider.set(min(slider_position, 100))
            time.sleep(0.1)

    def _update_playtime(self):
        print("updating playtime")
        while self.process and not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.playtime_label.configure(
                text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            )
            time.sleep(0.1)

    def _update_timecode(self, creation_time_str):
        start_timecode = datetime.strptime(creation_time_str or "00:00:00", "%H:%M:%S")
        while self.process and not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            current_timecode = start_timecode + timedelta(seconds=elapsed)
            self.timecode_label.configure(text=current_timecode.strftime("%H:%M:%S"))
            time.sleep(0.1)

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

    play_button = ctk.CTkButton(root, text="Play", command=player.start)
    play_button.pack(pady=10)

    stop_button = ctk.CTkButton(root, text="Stop", command=player.stop)
    stop_button.pack(pady=10)

    root.mainloop()

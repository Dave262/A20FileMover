import customtkinter as ctk
import subprocess
import threading
import time


class AudioPlayer:
    def __init__(self, file_path, playhead_slider, time_label):
        self.file_path = file_path
        self.process = None
        self.duration = self._get_duration()
        self.playhead_slider = playhead_slider
        self.time_label = time_label
        self.current_seek = 0

        self.playhead_slider.configure(command=self.seek_from_slider)

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

    def _format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def start(self):
        self._play_from(self.current_seek)
        print("Playback started.")

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            print("Playback stopped.")

    def seek_from_slider(self, slider_value):
        if self.process:
            self.stop()
        self.current_seek = (slider_value / 100) * self.duration
        self._play_from(self.current_seek)

    def _play_from(self, start_time):
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
        self.start_time = time.time() - start_time
        threading.Thread(target=self._update_ui, daemon=True).start()

    def _update_ui(self):
        while self.process and self.process.poll() is None:
            elapsed = time.time() - self.start_time
            slider_position = (elapsed / self.duration) * 100
            self.playhead_slider.set(min(slider_position, 100))
            self.time_label.configure(text=self._format_time(elapsed))
            time.sleep(0.5)


# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    time_label = ctk.CTkLabel(root, text="00:00:00")
    time_label.pack(pady=10)

    playhead_slider = ctk.CTkSlider(root, from_=0, to=100)
    playhead_slider.pack(fill="x", expand=True, pady=20, padx=20)

    player = AudioPlayer(
        "src/audio/Labour Day_Aug11_V1.wav", playhead_slider, time_label
    )
    player.print_duration()

    play_button = ctk.CTkButton(root, text="Play", command=player.start)
    play_button.pack(pady=10)
    stop_button = ctk.CTkButton(root, text="Stop", command=player.stop)
    stop_button.pack(pady=10)

    root.mainloop()

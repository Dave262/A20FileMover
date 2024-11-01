import subprocess
import threading
import time

# Path to your audio file
file_path = "src/audio/Labour Day_Aug11_V1.wav"


def play_audio(file_path):
    # Start ffplay in a background process to play the audio
    subprocess.run(
        ["ffplay", "-nodisp", "-autoexit", file_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def display_timestamp(duration):
    start_time = time.time()
    while True:
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        # Check if we've reached the end of the audio file
        if elapsed_time >= duration:
            break
        # Format elapsed time to hh:mm:ss
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(
            f"Playback Time: {formatted_time}", end="\r"
        )  # Overwrite the previous line
        time.sleep(1)  # Update every second
    print("\nPlayback finished.")


def get_audio_duration(file_path):
    # Use ffprobe to get the duration of the audio file in seconds
    ffprobe_command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]
    result = subprocess.run(
        ffprobe_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return float(result.stdout.strip())


# Get the duration of the audio file
duration = get_audio_duration(file_path)

# Start playback and timestamp display in separate threads
play_thread = threading.Thread(target=play_audio, args=(file_path,))
timestamp_thread = threading.Thread(target=display_timestamp, args=(duration,))

play_thread.start()
timestamp_thread.start()

play_thread.join()
timestamp_thread.join()

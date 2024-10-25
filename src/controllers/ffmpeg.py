import subprocess





def play_audio(file_path: str) -> None:
    """Play audio using FFmpeg."""
    try:
        subprocess.run(['ffmpeg', '-i', file_path, '-f', 'alsa', 'default'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to play the audio: {e}")
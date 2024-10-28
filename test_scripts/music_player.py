import pyaudio
import subprocess

CHUNK = 1024

def play_audio(file_path):
    song = subprocess.Popen(
        ["ffmpeg", "-i", file_path, "-loglevel", "panic", "-vn", "-f", "s16le", "pipe:1"],
        stdout=subprocess.PIPE
    )

    # instantiate PyAudio
    p = pyaudio.PyAudio()

    # open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,    # use ffprobe to determine channels
                    rate=48000,    # use ffprobe to determine sample rate
                    output=True)

    # read and play data
    data = song.stdout.read(CHUNK)
    
    while len(data) > 0:
        stream.write(data)
        data = song.stdout.read(CHUNK)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

# Example usage for testing
if __name__ == "__main__":
    play_audio("src/audio/Brent-241005113108.wav")
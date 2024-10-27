import subprocess
import sounddevice as sd
import pydub
import io
import numpy as np


class PlayBack:
    def __init__(self, source_file):
      super().__init__()

      # Path to the source file
      source_file = ""

      # Set chunk duration
      chunk_duration = 1  # Duration in seconds

      # Define the ffmpeg command to read the file as a stream
      ffmpeg_cmd = [
          "ffmpeg",
          "-i", source_file,
          "-f", "wav",          # Output as WAV format
          "-acodec", "pcm_s16le",  # Sample format for compatibility
          "-ar", "44100",       # Set the sample rate (match your needs)
          "-ac", "1",           # Set to mono for simplicity
          "pipe:1"              # Output to pipe
      ]

      # Open the ffmpeg subprocess
      with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as process:
          print("Streaming audio...")

          # Stream audio in chunks
          while True:
              # Read bytes equal to chunk size
              chunk_data = process.stdout.read(int(48000 * chunk_duration * 2))  # 2 bytes per sample for pcm_s16le

              # Break if end of stream
              if not chunk_data:
                  break

              # Use pydub to create an AudioSegment from raw audio data
              audio_segment = pydub.AudioSegment.from_raw(
                  io.BytesIO(chunk_data),
                  sample_width=2,       # 2 bytes for pcm_s16le
                  frame_rate=44100,     # Match your ffmpeg sample rate
                  channels=1            # Mono audio
              )

              # Convert AudioSegment to numpy array for playback
              audio_data = np.array(audio_segment.get_array_of_samples(), dtype=np.float32) / 32768.0  # Normalize
              
              sd.play(audio_data, samplerate=48000)
              sd.wait()  # Wait until the chunk finishes playing
            #   sd.stop()

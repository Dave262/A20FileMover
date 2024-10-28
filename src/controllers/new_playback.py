from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import subprocess
from io import BytesIO

class AudioPlayer:
  def __init__(self, file_path):
      self.file_path = file_path
      self.audio_segment = None
      self.is_playing = False
      self.process = None
      self.play_obj = None

  def stream_audio(self):
      # Set up the ffmpeg command to stream the file as raw audio data
      ffmpeg_cmd = [
          'ffmpeg', '-i', self.file_path, 
          '-f', 'wav',  # Output format as WAV
          '-acodec', 'pcm_s16le',  # Codec for 16-bit PCM
          '-ar', '44100',  # Sample rate (adjust if needed)
          '-ac', '2',  # Number of audio channels (1 for mono, 2 for stereo)
          '-'
      ]

      # Use subprocess to start the ffmpeg process and pipe stdout
      self.process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      # Read the stdout output from ffmpeg
      raw_audio_data, _ = self.process.communicate()

      # Load audio data into pydub AudioSegment
      self.audio_segment = AudioSegment.from_file(BytesIO(raw_audio_data), format="wav")

  def play_audio_segment(self):
      if self.audio_segment is None:
          self.stream_audio()  # Stream the audio if not already done
      self.is_playing = True
      self._play()

  def _play(self):
      # Convert AudioSegment to raw audio data
      raw_data = self.audio_segment.raw_data
      sample_rate = self.audio_segment.frame_rate
      num_channels = self.audio_segment.channels
      bytes_per_sample = self.audio_segment.sample_width

      # Play audio using simpleaudio
      self.play_obj = sa.play_buffer(raw_data, num_channels, bytes_per_sample, sample_rate)
      self.play_obj.wait_done()  # Wait for playback to finish
      self.is_playing = False

  def stop(self):
      if self.is_playing and self.play_obj:
          self.play_obj.stop()  # Stop playback
          self.is_playing = False
          print("Playback stopped.")

  def reset(self):
      # Reset the player state
      self.audio_segment = None
      self.process = None
      print("Player reset. Ready to play again.")
        
        
if __name__ == '__main__':
  audio_path = 'src/audio/Labour Day_Aug11_V1.wav'  # Replace with your PolyWAV file
  player = AudioPlayer(audio_path)

  # To play the audio
  player.play_audio_segment()

  # To stop playback
  # player.stop()

  # To reset the player for another playback
  # player.reset()
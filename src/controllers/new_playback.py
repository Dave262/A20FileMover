from pydub import AudioSegment
import os
import subprocess


ffplay_process = None

def play_wav(file_path):
  global ffplay_process
  # audio = AudioSegment.from_wav(file_path)

  # audio.export(file_path, format="wav")
  # subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path])
  # os.remove(file_path)
  
  # ffplay_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", file_path])
  ffplay_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", file_path])
  
  
def stop_wav():
  
  global ffplay_process

  if ffplay_process and ffplay_process.poll() is None:  # Check if the process is running
    ffplay_process.terminate()  # Terminate the process
    ffplay_process = None  # Reset the process variable
  else:
    print("No audio is currently playing.")

  
  
  
if __name__ == "__main__":
  wav_file_path = "src/audio/Brent-240930150405.wav" # Replace with your WAV file path
  if os.path.exists(wav_file_path): 
      play_wav(wav_file_path)
  else:
      print(f"File {wav_file_path} does not exist.")
import os
from controllers.wav_info_get import WavInfoGet


class File:
    def __init__(self, name, size, type, length, file_path, talent):
        super().__init__()
        self.name = name
        self.size = size
        self.type = type
        self.length = length
        self.file_path = file_path
        self.talent = talent
        

def load_files(audio_folder):
    files = []
    file_report = WavInfoGet()
    try:
        for file_name in os.listdir(audio_folder):      
            if file_name.lower().endswith('.wav'):
                file_path = os.path.join(audio_folder, file_name)
                
                info_getter = file_report.info_getter(file_path)
                
                name, type = os.path.splitext(file_name)
                # size = os.path.getsize(file_path)
           
                if info_getter: # dictionary passed in from wav info getter
                    talent = info_getter["talent_name"]
                    length = info_getter["length"]
                    size = info_getter["size"]
                    # bext_info = info_getter["bext_info"]
                    
                else:
                    print("Cant access info_getter")

                file_instance = File(name=name, size=size, type=type, length=length, file_path=file_path, talent=talent)
                files.append(file_instance)
    except FileNotFoundError:
        print(f"Directory {audio_folder} not found.")
    return files


# Correct function call
audio_folder = "src/audio/"
file_instances = load_files(audio_folder)


for file in file_instances:
    print(f"File Name: {file.name}  Size: {file.size}  Type: {file.type}  length {file.length}  Path: {file.file_path}, {file.talent}")

import os
from controllers.wav_info_get import WavInfoGet

#-------------------------------------------------
# Loads files as instances of a class with atributes 
#---------------------------------------------------

class File:
    def __init__(self, name, size, type, length, file_path, talent, sample_rate, bit_depth):
        super().__init__()
        self.name = name
        self.size = size
        self.type = type
        self.length = length
        self.file_path = file_path
        self.talent = talent
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth 



    # def __repr__(self):
    #         return (f"File: name={self.name}, talent={self.talent}, type={self.type}, "
    #                 f"sample_rate={self.sample_rate}, bit_depth={self.bit_depth}, "
    #                 f"size={self.size}, length={self.length}, file_path={self.file_path})")



    # audio_folder = "src/audio/"
    @classmethod
    def load_files(self, audio_folder):
        files = []
        file_report = WavInfoGet()
        try:
            for file_name in os.listdir(audio_folder):      
                if file_name.lower().endswith('.wav'):
                    file_path = os.path.join(audio_folder, file_name)
                    
                    info_getter = file_report.info_getter(file_path)
                    
                    name, type = os.path.splitext(file_name)
    #----------------------
    # Pass file_path to info_getter and return values from dict
    #----------------------          
                    if info_getter: # dictionary passed in from wav info getter
                        talent = info_getter["talent_name"]
                        length = info_getter["length"]
                        size = info_getter["size"]
                        sample_rate = info_getter["sample_rate"]
                        bit_depth = info_getter["bit_depth"]
                        
                        # bext_info = info_getter["bext_info"]
                        
                    else:
                        print("Cant access info_getter")

                    file_instance = File( 
                        name=name, 
                        size=size, 
                        type=type, 
                        length=length, 
                        file_path=file_path, 
                        talent=talent, 
                        sample_rate=sample_rate, 
                        bit_depth=bit_depth
                        )
            
                    files.append(file_instance)
                    
        except FileNotFoundError:
            print(f"Directory {audio_folder} not found.")
    
        return files


# file_instances = File.load_files(audio_folder)


#-------------------------------
# To access the output you have to loop through file_instances
#-------------------------------
# for file in file_instances:
#      print(f"{file.name}, {file.talent}, {file.type}, {file.sample_rate}, {file.bit_depth}, {file.size}, {file.length}, {file.file_path}")
   
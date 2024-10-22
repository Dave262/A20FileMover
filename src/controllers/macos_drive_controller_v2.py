import psutil
from wavinfo import WavInfoReader
import wavinfo
import os
import datetime
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FileReport:
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.wav_list = []
        self.file_list = [] # each transmitters list of files
        self.send_label_list = []
        self.send_path_list =[]

     
    def mount_drives(self):
        exfat_present = False
        system_drives = psutil.disk_partitions(all=False)
        
        for drive in system_drives: # loop through all system drives checking for exfat type
            if drive.fstype=="exfat": 
                self.file_path = drive.mountpoint  
                exfat_present = True                
                
                tx_label = self.file_path.strip("/Volumes/") 
                print("------------")
                logging.info(f"found external drive: {self.file_path}")
                self.send_path_list.append(self.file_path)   

                print(f"TX: {tx_label}")
                print("------------")
                
                self.send_label_list.append(tx_label)                 
        
        if not exfat_present: # defaults to an predefined 
            print("------------")
            logging.warning("No exFAT device found.")
            print("------------")
            # print("------summary-------")
            # print (f"selected path = {self.file_path}")
            # print(f"tx labels : {self.send_label_list}")
            # print(f"tx paths : {self.send_path_list}")
        return self.file_path          


    def info_getter(self, selected_files=None):
        counter = 1
        
        if selected_files:
            path_list = selected_files
        else: 
            path_list = self.send_path_list # list of drive mount points




                
        for tx in path_list:       
            self.file_list = os.listdir(tx)       
            for wav_file in self.file_list:
                if wav_file.lower().endswith('.wav'):             
# Every File
                    try:
                        info = wavinfo.WavInfoReader(os.path.join(tx, wav_file))
                    except Exception as e:   
                        logging.error(f"Failed to read {wav_file}: {e}") 
                        continue
                    time.sleep(.05)
                    bext_metadata = info.bext
                    info_metadata = info.info # doesn't seem to return anything
                    general_metadata = info.fmt # sample rate, bit depth etc. 
                    chunk_metadata = info.data			

            # useful options for wav data to pull
                    file_name = bext_metadata.originator
                    device_serial = bext_metadata.originator_ref
                    file_rec_date = bext_metadata.originator_date
                    start_tc = bext_metadata.originator_time 
                    file_time_ref = bext_metadata.time_reference # number of samples - referenced after midnight 
                    file_description = bext_metadata.description 
                    file_coding_history = bext_metadata.coding_history ## returned nothing on A20 mini
                                # The coding_history is designed to contain a record of every conversion performed on the audio file.
                    sample_rate = general_metadata.sample_rate
                    bit_depth = general_metadata.bits_per_sample
                    audio_format = general_metadata.audio_format # returns 3 for some reason 
                    samples = chunk_metadata.frame_count # total samples
                    bytes = chunk_metadata.byte_count

                    
                    file_megabytes = int(bytes) / 1048576	
                    file_run_time_float = samples / sample_rate # seconds with decimal places 
                    file_run_time_int = round(file_run_time_float)
                    time_delta = datetime.timedelta(seconds=file_run_time_int) # hours minutes seconds
                    
                    file_info = {
                        "count" : counter,
                        "file_name" : file_name,
                        "mb" : round(file_megabytes, 2),
                        "start_tc" : start_tc  
                    }  
                    
                    self.timeref = file_time_ref
                    self.sample_rate = sample_rate 
                    

                    
                    # add anything yu want to see here
                    print(f"{counter}-{wav_file} : {file_name} : {round(file_megabytes, 2)} MB : {time_delta} : start tc-{start_tc}")
                    
                    counter += 1
                    self.wav_list.append(file_info)
            return self.wav_list
        else:
            print("whatever")
                
                
if __name__=="__main__":
    file_reporter = FileReport()
    file_reporter.mount_drives()
    file_reporter.info_getter()




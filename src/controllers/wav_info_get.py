from wavinfo import WavInfoReader
import os
import logging
import wavinfo
import datetime


class WavInfoGet:
    def __init__(self):
        super().__init__()

    def info_getter(self, passed_file):
        # self.wav_list = []  # Clear the list at the beginning
        if passed_file:
            info = wavinfo.WavInfoReader(passed_file)  
            # time.sleep(0.01)
            bext_metadata = info.bext
            general_metadata = info.fmt  # Sample rate, bit depth, etc.
            chunk_metadata = info.data

            # Useful options for wav data to pull
            talent_name = bext_metadata.originator
            
            start_tc = bext_metadata.originator_time
            file_time_ref = bext_metadata.time_reference  # Number of samples - referenced after midnight
            sample_rate = general_metadata.sample_rate
            samples = chunk_metadata.frame_count  # Total samples
            bytes = chunk_metadata.byte_count
            # path = os.path.join(self.file_list)

            file_megabytes = int(bytes) / 1048576
            file_run_time_float = samples / sample_rate  # Seconds with decimal places
            file_run_time_int = round(file_run_time_float)
            time_delta = datetime.timedelta(seconds=file_run_time_int)  # Hours, minutes, seconds

            file_info = {
                "talent_name": talent_name,
                "size": round(file_megabytes, 2),
                "length": time_delta,
                "start_tc": start_tc,
                "bit depth": general_metadata,
                "sample_rate": sample_rate,

            
            }

            self.timeref = file_time_ref
            self.sample_rate = sample_rate
            
         
            # Add anything you want to see here
            # print(f"{counter}-{wav_file} : {file_name} : {round(file_megabytes, 2)} MB : {time_delta} : start tc-{start_tc}")

            # counter += 1
            # self.wav_list.append(file_info)
            
            return file_info 
# return self.wav_list

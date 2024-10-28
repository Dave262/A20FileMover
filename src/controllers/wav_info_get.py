from wavinfo import WavInfoReader
import wavinfo
import datetime
import os
import re


class WavInfoGet:
    def __init__(self):
        super().__init__()

    def info_getter(self, passed_file) -> dict:
        # self.wav_list = []  # Clear the list at the beginning
       

        if passed_file:
        
            info = WavInfoReader(passed_file)

            file_name = os.path.basename(passed_file)
            
            # time.sleep(0.01)
            bext_metadata = info.bext
            general_metadata = info.fmt  # Sample rate, bit depth, etc.
            chunk_metadata = info.data
            bullet_metadata = info.info
            # Useful options for wav data to pull
            talent_name = bext_metadata.originator
            
            start_tc = bext_metadata.originator_time
            file_time_ref = bext_metadata.time_reference  # Number of samples - referenced after midnight
            sample_rate = general_metadata.sample_rate
            samples = chunk_metadata.frame_count  # Total samples
            bytes = chunk_metadata.byte_count
            bit_depth = general_metadata.bits_per_sample
            orig_date = bext_metadata.originator_date
            description = bext_metadata.description
            product_id = bext_metadata.originator_ref

            file_megabytes = int(bytes) / 1048576
            file_run_time_float = samples / sample_rate  # Seconds with decimal places
            file_run_time_int = round(file_run_time_float)
            time_delta = datetime.timedelta(seconds=file_run_time_int)  # Hours, minutes, seconds


        # Add more patterns here if needed

            match = re.search(r"sSPEED=([\d.]+-ND)", description)
            frame_rate = match.group(1).replace("0", "") if match else None # only strips from begining


            file_info = {
        
                "file_name": file_name, 
                "talent_name": talent_name,
                "size": round(file_megabytes, 2),
                "length": time_delta,
                "start_tc": start_tc,
                "bit_depth": bit_depth,
                "sample_rate": sample_rate,
                "info": orig_date,
                "frame_rate": frame_rate,
                "product_id": product_id,
                "rec_date": orig_date
            }

            self.timeref = file_time_ref
            self.sample_rate = sample_rate
        # except Exception as e:
        #     print("Error getting info for files")
        
    

            # print(file_info)
        return file_info # dict
# return self.wav_list
if __name__=="__main__":
    wav_info = WavInfoGet()
    wav_info.info_getter("src/audio/Brent-240930110056.wav")
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
        self.send_label_list = [] # list of drive labels for button creation
        self.send_path_list =[]


    def mount_drives(self):# -> dict[str, list]:# -> dict[str, list]:
        exfat_present = False
        system_drives = psutil.disk_partitions(all=False)

        logging.info("Checking system drives...")

        for drive in system_drives:  # loop through all system drives checking for exfat type
            logging.info(f"Found drive: {drive.device}, Type: {drive.fstype}")
            if drive.fstype == "exfat":
                self.file_path = drive.mountpoint
                exfat_present = True

                tx_label = os.path.basename(self.file_path)  # only return the drive label
                print("------------")
                logging.info(f"Found external drive: {self.file_path}")
                self.send_path_list.append(self.file_path)
                print(f"TX: {tx_label}")
                print("------------")
                self.send_label_list.append(tx_label)

        if not exfat_present:  # defaults to a predefined
            print("------------")
            logging.warning("No exFAT device found.")
            print("------------")

        return {
            "labels" : self.send_label_list,  # Return the list of drive labels after checking all drives
            "paths" : self.send_path_list
        }

    def info_getter(self, selected_files=None):
        counter = 1
        self.wav_list = []  # Clear the list at the beginning

        if selected_files:
            path_list = [selected_files]
        else:
            path_list = self.send_path_list  # List of drive mount points

        for tx in path_list:
            try:
                self.file_list = os.listdir(tx)  # Get the list of files in the directory
                print(f"HELLO {self.file_list}")
            except Exception as e:
                logging.error(f"Failed to list directory {tx}: {e}")
                continue

            for wav_file in self.file_list:
                if wav_file.lower().endswith('.wav'):
                    # Every File
                    try:
                        info = wavinfo.WavInfoReader(os.path.join(tx, wav_file))
                    except Exception as e:
                        logging.error(f"Failed to read {wav_file}: {e}")
                        continue

                    time.sleep(0.05)
                    bext_metadata = info.bext
                    general_metadata = info.fmt  # Sample rate, bit depth, etc.
                    chunk_metadata = info.data

                    # Useful options for wav data to pull
                    file_name = bext_metadata.originator
                    start_tc = bext_metadata.originator_time
                    file_time_ref = bext_metadata.time_reference  # Number of samples - referenced after midnight
                    sample_rate = general_metadata.sample_rate
                    samples = chunk_metadata.frame_count  # Total samples
                    bytes = chunk_metadata.byte_count

                    file_megabytes = int(bytes) / 1048576
                    file_run_time_float = samples / sample_rate  # Seconds with decimal places
                    file_run_time_int = round(file_run_time_float)
                    time_delta = datetime.timedelta(seconds=file_run_time_int)  # Hours, minutes, seconds

                    file_info = {
                        "count": counter,
                        "file_name": file_name,
                        "mb": round(file_megabytes, 2),
                        "length": time_delta,
                        "start_tc": start_tc,
                    }

                    self.timeref = file_time_ref
                    self.sample_rate = sample_rate

                    # Add anything you want to see here
                    print(f"{counter}-{wav_file} : {file_name} : {round(file_megabytes, 2)} MB : {time_delta} : start tc-{start_tc}")

                    counter += 1
                    self.wav_list.append(file_info)

        return self.wav_list



if __name__=="__main__":
    file_reporter = FileReport()
    file_reporter.mount_drives()
    file_reporter.info_getter()

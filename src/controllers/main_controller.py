import os
import shutil
import re
from tkinter import filedialog
import time
from datetime import datetime
from typing import Union, Callable
import wavinfo
from wavinfo import WavInfoReader
from controllers.mac_usb_controller_v1 import MacUsbControlerV1
# from ..app import App
from tqdm import tqdm

class MainController:
    def __init__(self):
        super().__init__()
    
        # self._app = App
    
        
    def global_time(self):
        """
        Uses the date time and time modules to set the local date and time

        :return: local_time
        """
        time_object = time.localtime()
    
        local_time = time.strftime("%B %d %Y - %H:%M:%S", time_object)
        # print(local_time)
        return local_time




    def select_folder_path(self):
        folder_path: str = filedialog.askdirectory(initialdir="/home/david/Python_Projects/Fake_Folders/", title="please select your bodypack folder path")
        print(f"The Folder path is: {folder_path}")
        return folder_path 
    




    def select_A20_path(self, ):
        
        A20_path: str = filedialog.askdirectory(initialdir="/home/david/Python_Projects/", title="please select your A20 pack")
        print(A20_path)
        return A20_path




    def A20_convert_name(self, path) -> list[str]:
            """
            Converts the default 12 digit date and time that the A20 transmitters use into a readable date and time. 
            Prefixed by the transmitter name. 

            Args:
                path (str): Path to the A20 mount either the manually selected path or the path from a clicked button

            Returns:
                list[str]:  a list of the formatted names including date and starting timecode
            """
            new_names = []
            for file in os.listdir(path):
                names = re.findall(r'\D+', file.removesuffix(".wav"))
                names_results = "".join(names)
                numbers = re.findall(r'\d+', file)
                numbers_result = "".join(numbers)
                if len(numbers_result) ==12:
                    try:
                        date_time = datetime.strptime(numbers_result, "%y%m%d%H%M%S")
                        formatted_date = date_time.strftime("%d/%m/%Y")
                        formatted_time = date_time.strftime("%H:%M:%S")
                        new_name = (f"{names_results} Date: {formatted_date}, TC: {formatted_time}")
                        new_names.append(new_name)
                    except ValueError:
                        print(f"Unexpected date format in {numbers_result}")        
                else:
                    print(f"Unexpected number format in {numbers_result}")
            return new_names



    # def move_files(self, A20_path, folder_path, update_progress_callback=None):
    #     if A20_path and folder_path:
    #         print(f"def - move_files in main controller can see {A20_path} : {folder_path}")
    #         files = os.listdir(A20_path)
    #         total_files = len(files)
    #         moved_files = 0
    # # Create a progress bar using tqdm        
    #         with tqdm(total=total_files, desc="Moving Files") as progress_bar:
    #             for file in files:
    #                 name_only = re.findall(r'[a-zA-Z]+', file.removesuffix(".wav"))
    #                 if name_only:
    #                     name_only = name_only[0]
    #                     print(name_only)
    #                 for folder in os.listdir(folder_path):
    #                     if name_only == folder:
    #                         print("there's a match!")
                            
    #                         src_path = os.path.join(A20_path, file)
    #                         dst_path = os.path.join(folder_path, folder, file)
                            
    #                         progress_bar.set_postfix(file=file)
                            
    #                         shutil.move(src_path, dst_path)
    #                         moved_files += 1
                            
    #                         print(f"moved file: {file} to folder: {folder}")
                            
    #                         progress_bar.update(1)
                            
    #                         if update_progress_callback:
    #                             update_progress_callback(moved_files / total_files)
    #                         break

   
    def move_files(self, A20_path, folder_path, ctk_progress_bar):

        if A20_path and folder_path:
            print(f"def - move_files in main controller can see {A20_path} : {folder_path}")
            # self.start_progress_bar()
            files = os.listdir(A20_path)
            
            for file in files:
                name_only = re.findall(r'[a-zA-Z]+', file.removesuffix(".wav"))
                if name_only:
                    name_only = name_only[0]
                    print(name_only)
                for folder in os.listdir(folder_path):
                    if name_only == folder:
                        print("there's a match!")
                        
                        src_path = os.path.join(A20_path, file)
                        dst_path = os.path.join(folder_path, folder, file)
                        
                        # Get the size of the file for tracking progress
                        file_size = os.path.getsize(src_path)
                        
                        # Open the source and destination files and copy in chunks while updating the progress bar
                        with open(src_path, 'rb') as src_file, open(dst_path, 'wb') as dst_file:
                            with tqdm(total=file_size, desc=f"Copying {file}", unit='B', unit_scale=True) as progress_bar:
                                for chunk in iter(lambda: src_file.read(1024 * 1024), b''):
                                    dst_file.write(chunk)
                                    progress_bar.update(len(chunk))
                        
                        # Optionally, remove the source file after copying to simulate move
                        os.remove(src_path)
                        print(f"Moved file: {file} to folder: {folder}")
                        # self.stop_progress_bar()
            print("ALL FILES MOVED!")

      

    def give_list_of_attributes_for_tx_files(self):
        self._usb_controller = MacUsbControlerV1()
        
        tx_path = self._usb_controller.list_drives()
        print(tx_path)
        
        for mount_pount in tx_path:    
            a20_mount_point = mount_pount.get('mountpoint')
            print(f"mount = {a20_mount_point}")  
            
 
        for index, file in enumerate(os.listdir(a20_mount_point), start=1):
            file_path = os.path.join(a20_mount_point, file)
            
            if not file_path.endswith(".wav"):
                print(f"Skipping non-WAV file: {file}")
                continue
            try:
                info = WavInfoReader(file_path)
                fmt_info = info.fmt
                if fmt_info:
                    print(f"{index}_{file} - bit depth: {fmt_info.bits_per_sample} - sample rate: {fmt_info.sample_rate}")    
            except wavinfo.riff_parser.WavInfoEOFError:
                print(f"EOF error encountered while reading {file_path}. The file may be corrupted or incomplete.")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

  
if __name__ == "__main__":
    controller = MainController()
    current_time = controller.global_time()
    # wav_info = controller.give_list_of_attributes_for_tx_files()
    print(f"The time is: {current_time}")

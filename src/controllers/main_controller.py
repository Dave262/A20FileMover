import os
import shutil
import re
from tkinter import filedialog
import time
from datetime import datetime
from typing import Union, Callable

class MainController:
    def __init__(self):
        super().__init__()
        

    def global_time(self):
        """
        Uses the date time and time modules to set the local date and time

        :return: local_time
        """
        time_object = time.localtime()
    
        local_time = time.strftime("%B %d %Y - %H:%M:%S", time_object)
        print(local_time)
        return local_time

    def select_folder_path(self):
        folder_path: str = filedialog.askdirectory(initialdir="home", title="please select your bodypack folder path")
        print(folder_path)
        return folder_path 



    def select_A20_path(self):
        A20_path: str = filedialog.askdirectory(initialdir="home", title="please select your A20 pack")
        print(A20_path)
        return A20_path



    def move_files(self, A20_path, folder_path, update_progress_callback=None):
        if A20_path and folder_path:
            files = os.listdir(A20_path)
            total_files = len(files)
            moved_files = 0
            for file in os.listdir(A20_path):
                name_only = re.findall(r'[a-zA-Z]+', file.removesuffix(".wav"))
                if name_only:
                    name_only = name_only[0]
                    print(name_only)
                for folder in os.listdir(folder_path):
                    if name_only == folder:
                        print("there's a match!")
                        src_path = os.path.join(A20_path, file)
                        dst_path = os.path.join(folder_path, folder, file)
                        shutil.move(src_path, dst_path)
                        print(f"moved file: {file} to folder: {folder}")
                        if update_progress_callback:
                            update_progress_callback(moved_files / total_files)



# Function that strips all characters form the file string and returns a readable date from the number suffix

    def extract_numbers_convert(self, path):
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
                    print(f"{names_results} Rec Date: {formatted_date}, Start TC: {formatted_time}")
                except ValueError:
                    print(f"Unexpected date format in {numbers_result}")        
            else:
                print(f"Unexpected number format in {numbers_result}")
        return formatted_date

# if __name__ == "__main__":
#     controller = MainController()
#     controller.global_time()
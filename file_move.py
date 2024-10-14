import os
import shutil
import re
from tkinter import messagebox, filedialog
from typing import List



# select folder
def select_folder_path():
    folder_path: str = filedialog.askdirectory(initialdir="home", title="please select your bodypack folder path")
    print(folder_path)
    return folder_path 


def select_A20_path():
    A20_path: str = filedialog.askdirectory(initialdir="home", title="please select your A20 pack")
    print(A20_path)
    return A20_path



def move_files(A20_path, folder_path, update_progress_callback=None):
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



    





# selectPaths()
# move_files()
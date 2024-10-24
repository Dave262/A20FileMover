import os
import shutil
import re
from tkinter import filedialog
import time
from datetime import datetime
from typing import Union, Callable
import wavinfo
from wavinfo import WavInfoReader
from controllers.macos_drive_controller_v2 import FileReport
# from ..app import App
from tqdm import tqdm



class MainController:

    def __init__(self):
        super().__init__()

        # self._app = App
        self._usb_controller = FileReport()

    def global_time(self):
        time_object = time.localtime()
        local_time = time.strftime("%B %d %Y - %H:%M:%S", time_object)
        # print(local_time)
        return local_time



    def select_folder_path(self):
        folder_path: str = filedialog.askdirectory(initialdir="/home/david/Python_Projects/Fake_Folders/", title="please select your bodypack folder path")
        print(f"The Folder path is: {folder_path}")
        return folder_path



    def select_A20_path(self,):
        A20_path: str = filedialog.askdirectory(initialdir="/home/david/Python_Projects/", title="please select your A20 pack")
        # print(A20_path)
        return A20_path



    def move_files(self, A20_path, folder_path, textbox=None, progress_callback=None):
        if A20_path and folder_path:
            print(f"def - move_files in main controller can see {A20_path} : {folder_path}")
            files: list = os.listdir(A20_path)

            for file in files:
                name_only: list = re.findall(r'[a-zA-Z]+', file.removesuffix(".wav"))
                if name_only:
                    name_only = name_only[0]
                    match_found = False

                    for folder in os.listdir(folder_path):
                        if name_only == folder:
                            print(f"there's a match! : {file} corresponds to the folder {folder}")
                            match_found = True
                            src_path = os.path.join(A20_path, file)
                            dst_path = os.path.join(folder_path, folder, file)
                            break

                    if not match_found:
                        print(f"No match found for {name_only}, moving on.")
                        continue

                    try:
                        file_size = os.path.getsize(src_path)
                        print(f"Starting copy of {file} with size {file_size} bytes")
                        with open(src_path, 'rb') as src_file, open(dst_path, 'wb') as dst_file:
                            with tqdm(total=file_size, desc=f"Copying {file}", unit='B', unit_scale=True) as progress_bar:
                                for chunk in iter(lambda: src_file.read(1024 * 1024), b''):
                                    dst_file.write(chunk)
                                    progress_bar.update(len(chunk))

                                    if progress_callback:
                                        progress_callback(len(chunk), file_size)


                        os.remove(src_path)
                        print(f"Moved file: {file} to folder: {folder}")
                    except Exception as e:
                        print(f"Error moving file {file}: {e}")

            print("ALL FILES MOVED!")


    def give_list_of_attributes_for_tx_files(self):

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
    wav_info = controller.give_list_of_attributes_for_tx_files()
    print(f"The time is: {current_time}")

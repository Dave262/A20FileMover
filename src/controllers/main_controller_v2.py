import os
import shutil
import re
from tkinter import filedialog
import time
from datetime import datetime
from typing import Union, Callable
import wavinfo
from wavinfo import WavInfoReader
# from controllers.macos_drive_controller_v2 import FileReport

from tqdm import tqdm


class MainController:
    def __init__(self):
        super().__init__()


    def global_time(self) -> str: 
      """
      summary_
    Uses time module to get the current date based on users system. 
      Returns:
          str: month day year eg. (October 25 2024)
      """
      time_object = time.localtime()
      local_date:str = time.strftime("%B %d %Y") # date but no time
      print(local_date)
      return local_date


    def folder_select_path(self) -> str:
      folder_path: str = filedialog.askdirectory(initialdir="/home/david/Python_Projects/Fake_Folders/", title="Select destination folder")
      print(f"Destination path : {folder_path}")
      return folder_path
    
    
    def select_A20_path(self,) -> str:
      tx_path: str = filedialog.askdirectory(initialdir="/home/david/Python_Projects/", title="please select your A20 pack")
      return tx_path
    
    def match_files_to_folder(self, folder_path: str, tx_path: str) -> None:
      """
      Makes a dictionary of the tx_path and folder_path names : paths and then matches them based on names
      it then creates a new dictionary 'move_dict' which is each file and the path to the folder it matches.

      Args:
          folder_path (str): can be user selected
          tx_path (str): can be user selected or taken from tx button 
      """
      if folder_path and tx_path:
        print(f"The folder path is: {folder_path}")
# Folder dictionary creation
        folder_list: list = [folder for folder in os.listdir(folder_path) if re.match(r'^[^.]+$', folder)]
        folder_dict: dict = {folder: os.path.join(folder_path, folder) for folder in folder_list}
        for folder, path in folder_dict.items():
          print(f"{folder} : {path}")
      
# Transmitter dictionary        
        tx_files: list = os.listdir(tx_path) # this will include hidden files and non-wav files
        move_dict = {}
        
        for file in tx_files:
          if file.endswith (".wav"):
            for folder in folder_dict:
              if folder.lower() in file.lower():# only return wav files
                move_dict[os.path.join(tx_path, file)] = os.path.join(folder_path, folder)
           
            
        
        for key, value in move_dict.items():
          print(f"YO YO {key} : {value}")
          
      print(move_dict)
      return move_dict
        
    def move_files(self, move_dict):
      if move_dict:
        print("Moving files...")
        try:
          print(move_dict)
          for file_path, folder_path in move_dict.items():
            print(f"Attempting to move {file_path} to {folder_path}") 
            shutil.move(file_path, folder_path)
            print(f"Moved {file_path} to {folder_path}")
          

  
        
        except Exception as e:
          print(f"Error moving files: {str(e)}")
      else:
        print("no files to move")
          
          
      
      
      
        

if __name__ == "__main__":
    controller = MainController()
    # dict = controller.match_files_to_folder
    date = controller.global_time()
    file_match = controller.match_files_to_folder(
      "/Users/davidross/Documents/A20_Test_Folders/Bodypack_Folders", 
      "/Users/davidross/Documents/A20_Test_Folders/A20 mount"
      )
    controller.move_files(file_match)
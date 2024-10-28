
from tkinter.constants import COMMAND
import customtkinter as ctk
from typing import LiteralString, Union, Callable
from utils.enums import Colour
from controllers.main_controller_v2 import MainController
from controllers.macos_drive_controller_v2 import FileReport

from controllers.class_based_files import File
from controllers.wav_info_get import WavInfoGet
from controllers.new_playback import AudioPlayer

# from controllers.playback import play_audio, stop_audio

import logging
import time
from threading import Thread, Event
import CTkListbox as lb
import os

# when calling a function from any of the controller modules the syntax wis
# "self.[_reference to controller as listed in script].function


class App(ctk.CTk):
    def __init__(self):
        
        

        super().__init__()
        
        # self.playback_thread = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

# configure the window
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0,1), weight=0)
        self.grid_columnconfigure((2),weight=1)

        self.geometry("900x550")
        self.title("A20 TX File Mover")

# Controllers
        self._usb_controller = FileReport()

        self._controller = MainController(self.print_progress) # print progress callback

        # self._file_store = FileInfo()
        self._class_based_files = File(None,None, None, None, None, None, None, None)
        self._wav_info_get = WavInfoGet()

        self.current_files: list = [] # the files from tx or manualc
        self.audio_player = AudioPlayer
       
 
   

        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=2)
        self.grid_rowconfigure((2), weight=0)
        self.grid_columnconfigure((1,2), weight=1)
        self.grid_columnconfigure((0), weight=0)

        self.A20_path = ""
        self.folder_path = ""
        self.create_layout()
        self.create_tx_buttons()

# Heading
    def create_layout(self):

# HEADER
        self.frame_header = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_header.grid(row=0, columnspan=3, padx=3, pady=1, sticky="nswe")

        self.label_heading =ctk.CTkLabel(self.frame_header)
        self.label_heading.pack(side="left", padx=10, pady=10)
        self.label_heading.configure(text="TRANSMITTER - FILE MOVER", font=("Inclusive Sans", 25))

        self.time_heading =ctk.CTkLabel(self.frame_header)
        self.time_heading.pack(side="right", padx=10)
        self.time_heading.configure(text=f"{self._controller.global_time()}", font=("Inclusive Sans", 15))

        self.frame_left = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_left.grid(row=1, column=0, rowspan=1, padx=3, pady=3, sticky="nswe")
        self.frame_left.configure()

        self.frame_middle = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_middle.grid(row=1, column=1, rowspan=1, padx=3, pady=3, sticky="nswe")
        self.frame_middle.configure()

        self.frame_right = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_right.grid(row=1, column=2, rowspan=1, padx=3, pady=3, sticky="nswe")
        self.frame_right.configure()

        self.frame_footer = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_footer.grid(row=2, columnspan=3, padx=3, pady=1, sticky="nswe")



# Folder Stuff
        self.A20_instance_frame = ctk.CTkFrame(self.frame_left)
        self.A20_instance_frame.pack(side="top", pady=1, padx=1)
        self.A20_instance_frame.configure(fg_color="transparent")

        self.tx_list_frame = ctk.CTkFrame(self.A20_instance_frame)
        self.tx_list_frame.pack(pady=1, padx=1)
        self.tx_list_frame.configure(fg_color="transparent")


        self.tx_refresh_button = ctk.CTkButton(self.tx_list_frame, text="R", width=30, height=30, command=self.create_tx_buttons)
        self.tx_refresh_button.pack(side="left", pady=5, padx=5)
        self.tx_refresh_button.configure(fg_color="transparent", font=("Inclusive Sans", 15))

        self.A20_instance_label = ctk.CTkLabel(self.tx_list_frame)
        self.A20_instance_label.pack(side="left", padx=5, pady=5)
        self.A20_instance_label.configure(text="Transmitters", font=("Inclusive Sans", 20))

        self.options_frame = ctk.CTkFrame(self.frame_left)
        self.options_frame.pack(side="bottom", fill='both', pady=1, padx=1)
        self.options_frame.configure(fg_color="transparent")

        self.options_label = ctk.CTkLabel(self.options_frame)
        self.options_label.pack(padx=5, pady=5)
        self.options_label.configure(text="Options", font=("Inclusive Sans", 15))

        self.A20_path_button = ctk.CTkButton(self.options_frame, text="Manually Choose TX", command=self.manual_select)
        self.A20_path_button.pack(pady=10)
        self.A20_path_button.configure(fg_color=Colour.BUTTON.value, font=("Inclusive Sans", 15))

        self.folder_path_button = ctk.CTkButton(self.options_frame, text="Choose Destination", command=self.update_label_with_folder_path)
        self.folder_path_button.pack(pady=10)
        self.folder_path_button.configure(fg_color=Colour.BUTTON.value, font=("Inclusive Sans", 15))


        self.options_label_frame = ctk.CTkFrame(self.frame_middle)
        self.options_label_frame.pack(padx=5, pady=10, fill="both")
        self.options_label_frame.configure(fg_color="transparent")



        self.options_label = ctk.CTkLabel(self.options_label_frame)
        self.options_label.pack(side="left", padx=10, pady=0)
        self.options_label.configure(text="File list", font=("Inclusive Sans", 15))





        self.a20_listbox = lb.CTkListbox(self.frame_middle,
                                         height=300,
                                         width=300,
                                         command=self.add_to_details)

        self.a20_listbox.pack(fill="both", pady=0, padx=10)
        self.a20_listbox.insert(0, "Files will show here...")
        self.a20_listbox.configure(border_width=1,
                                   corner_radius=10,
                                   border_color=Colour.OFF_WHITE.value,
                                   fg_color=Colour.BACKGROUND_DARK.value,
                                   hover_color=Colour.GREY.value,
                                   highlight_color=Colour.BLUE.value,
                                   scrollbar_button_color=Colour.OFF_WHITE.value,
                                   font=("Reddit Mono", 15)
                                   )
        



        self.copy_info_frame = ctk.CTkFrame(self.frame_right)
        self.copy_info_frame.pack(padx=5, pady=5, fill="both")
        self.copy_info_frame.configure(fg_color="transparent")

        self.copy_info_label = ctk.CTkLabel(self.copy_info_frame)
        self.copy_info_label.pack(side="left", padx=10, pady=0)
        self.copy_info_label.configure(text="Copy window", font=("Inclusive Sans", 15))


        self.terminal_textbox = ctk.CTkTextbox(self.frame_right, height=80)
        self.terminal_textbox.pack(fill="both", pady=0, padx=10)
        self.terminal_textbox.insert("2.0", "No folder selected...") # placeholder text
        self.terminal_textbox.configure(fg_color=Colour.BACKGROUND_DARK.value,
                                        border_width=1,
                                        border_color=Colour.OFF_WHITE.value,
                                        font=("Reddit Mono", 13)
                                        )


        self.file_info_frame = ctk.CTkFrame(self.frame_right)
        self.file_info_frame.pack(padx=5, pady=5, fill="both")
        self.file_info_frame.configure(fg_color="transparent")
        

        self.file_info_label = ctk.CTkLabel(self.file_info_frame)
        self.file_info_label.pack(side="left", padx=10, pady=0)
        self.file_info_label.configure(text="File info", font=("Inclusive Sans", 15))


        self.file_info_textbox = ctk.CTkTextbox(self.frame_right, height=150)
        self.file_info_textbox.pack(fill="both", pady=0, padx=10)
        self.file_info_textbox.insert("2.0", "File details...") # placeholder text
        self.file_info_textbox.configure(fg_color=Colour.BACKGROUND_DARK.value,
                                        border_width=1,
                                        border_color=Colour.OFF_WHITE.value,
                                        font=("Reddit Mono", 13)
                                        )


        self.options_frame_mid = ctk.CTkFrame(self.frame_middle)
        self.options_frame_mid.pack(side="bottom", fill="x", expand="true", pady=10, padx=1)
        self.options_frame_mid.configure(fg_color="transparent")

        self.extra_button = ctk.CTkButton(self.options_frame_mid, text="Show today", command=None)
        self.extra_button.pack(side="left", fill="x", expand="true", padx=5, pady=0)
        self.extra_button.configure(fg_color=Colour.BUTTON.value, font=("Inclusive Sans", 15))

        self.extra_button_two = ctk.CTkButton(self.options_frame_mid, text="Clear Files")
        self.extra_button_two.pack(side="left", fill="x", expand="true", padx=5, pady=0)
        self.extra_button_two.configure(fg_color=Colour.BUTTON.value, command=self.clear_textbox, font=("Inclusive Sans", 15))


        self.copy_files_button = ctk.CTkButton(self.frame_right, text="Copy Files to Folders", command=self.call_move_files)
        self.copy_files_button.pack(fill="x", padx=5, pady=10)
        self.copy_files_button.configure(fg_color=Colour.GREEN.value, font=("Inclusive Sans", 15))
    

        self.move_files_button = ctk.CTkButton(self.frame_right, text="Move Files to Folders", command=self.call_move_files)
        self.move_files_button.pack(side="bottom", fill="x", padx=5, pady=10)
        self.move_files_button.configure(fg_color=Colour.PINK.value, font=("Inclusive Sans", 15))
        self.drive_buttons = {}

        # self.playback_label = ctk.CTkLabel(self.frame_footer)
        # self.playback_label.pack(side="left", padx=10, pady=5)
        # self.playback_label.configure(text="Playback", 
        #                               font=("Inclusive Sans", 20)
        #                               )

        self.play_button = ctk.CTkButton(self.frame_footer, text="Play", width=50, height=40, command=self.play_selected_audio)
        self.play_button.pack(side="left", padx=(20, 10), pady=10)
        self.play_button.configure(fg_color=Colour.NORD.value, border_width=1, border_color=Colour.OFF_WHITE.value, hover_color=Colour.BACKGROUND_DARK.value, font=("Inclusive Sans", 15))

        self.stop_button = ctk.CTkButton(self.frame_footer, text="Stop", width=50, height=40, command=self.stop_playback)
        self.stop_button.pack(side="left", padx=(10, 10), pady=10)
        self.stop_button.configure(fg_color=Colour.NORD.value, border_width=1, border_color=Colour.OFF_WHITE.value, hover_color=Colour.BACKGROUND_DARK.value, font=("Inclusive Sans", 15))



        self.playhead_slider = ctk.CTkSlider(self.frame_footer)
        self.playhead_slider.pack(side="left", fill="x", expand ='true', pady=20, padx=20)
        self.playhead_slider.configure(
            
            button_color=Colour.RED.value,
            button_hover_color=Colour.RED.value,
            progress_color=Colour.RED.value,
            from_=1,
            to=100
        )
        self.playhead_slider.set(0)
#------------------------------------
# Folder selection 
#--------------------------------
    def update_label_with_folder_path(self) -> None:
        self.folder_path: str = self._controller.folder_select_path()

        if self.folder_path:
            self.terminal_textbox.delete("1.0", "end")
            self.terminal_textbox.insert("end", text=f"Destination:\n{self.folder_path}")
        else:
            print("No folder path selected.")
#-----------------------------------------
# Handle manual selection of transmitter
#------------------------------------------

    def manual_select(self):
        counter = 1
        self.file_paths = []
        path = self._controller.select_A20_path()
        self.A20_path = ""
        self.current_files: list = [] # empties existing list 
        if path:
            file_label_item = os.path.basename(path)
            self.current_files: list = self._class_based_files.load_files(path) # list of files for moving etc
            self.A20_path = path
            
            self.a20_listbox.delete(0, "end")
              # List to store file paths
            if not self.current_files:
                self.a20_listbox.insert("end", "No files in selected path")
            else:
                for file_instance in self.current_files:
                    file_dict: dict = self._wav_info_get.info_getter(file_instance.file_path)
                    display_text: str = f"{counter} | {file_dict['talent_name']} | {file_dict['length']} | {file_dict['size']} | {file_dict["rec_date"]}"
                    self.a20_listbox.insert("end", display_text)
                    self.file_paths.append(file_instance.file_path)  # Store the file path
                    self.options_label.configure(text=f"Directory: {file_label_item}")
                    print(f"success! loaded {file_instance}")
                    counter = counter + 1
              
        else:
            print("No path selected.")

#------------------------------------------
# Add to details: 
#------------------------------------------

    def add_to_details(self, index):
        index: tuple = self.a20_listbox.curselection()  # gets the selected item index in the listbox

        selected_index: tuple = index

        # Ensure selected_index is an integer
        if isinstance(selected_index, int):
            selected_file_path: str = self.file_paths[selected_index]  # Retrieve the file path
            self._wav_info_get.info_getter(selected_file_path)  # Use the file path

            print(f"File number {selected_index}, Path: {selected_file_path}")

            file_dict: dict = self._wav_info_get.info_getter(selected_file_path)
            display_text: str = (
                    f"File name: {file_dict['file_name']}\n"
                    f"Talent: {file_dict['talent_name']}\n"
                    f"Runtime: {file_dict['length']}\n"
                    f"Size: {file_dict['size']} mb\n"
                    f"Rec date: {file_dict["rec_date"]}\n"
                    f"Frame rate: {file_dict["frame_rate"]}\n"
                    f"Sample rate: {file_dict["sample_rate"]} hz\n"
                    f"Bit depth: {file_dict["bit_depth"]}"
            )

            self.file_info_textbox.delete("1.0", "end")
            self.file_info_textbox.insert("2.0", display_text)
            return selected_file_path
        else:
            print("Error: selected_index is not an integer.")
            return None
            
#------------------------------------------
# Automatic transmitter stuff
#----------------------------------------------

    def create_tx_buttons(self) -> None:

        drive_info: dict = self._usb_controller.mount_drives()

        labels: list = drive_info["labels"]
        paths: list = drive_info["paths"]

        # logging.info(f"Creating TX buttons for: {labels}")

        for button in self.drive_buttons.values():
            button.destroy()
        self.drive_buttons.clear()


        if labels:
            for index, label in enumerate(iterable=labels):
                full_path: list = paths[index] # turn it into a list
                logging.info(f"Creating button for: {label} with path {full_path}")

                button = ctk.CTkButton(self.A20_instance_frame, text=f"TX: {label}", command=lambda tx_button=full_path: self.select_tx_button(tx_button))
                button.pack(pady=10)  # Adjust layout as needed
                button.configure(fg_color=Colour.NORD.value, border_width=1, border_color=Colour.OFF_WHITE.value, hover_color=Colour.BACKGROUND_DARK.value, font=("Inclusive Sans", 15))
                self.drive_buttons[label] = button
                logging.info(f"Button for {label} packed successfully.")

        else:
            logging.info("No transmitters connected, soz.")



    def select_tx_button(self, a20_mount_point):
        counter = 1
        self.file_paths = []
        self.A20_path = ""
        self.current_files: list = []
        if a20_mount_point:
            file_label_item = os.path.basename(a20_mount_point)

            self.current_files = self._class_based_files.load_files(a20_mount_point)
            self.A20_path = a20_mount_point
            
            self.a20_listbox.delete(0, "end")
              # List to store file paths
            if not self.current_files:
                self.a20_listbox.insert("end", "No files in selected path")
            else:
                for file_instance in self.current_files:
                    file_dict: dict = self._wav_info_get.info_getter(file_instance.file_path)
                    display_text: str = f"{counter}   {file_dict['talent_name']}   {file_dict['length']}   {file_dict['size']}     {file_dict["rec_date"]}"
                    self.a20_listbox.insert("end", display_text)
                    self.file_paths.append(file_instance.file_path)  # Store the file path
                    self.options_label.configure(text=f"Transmitter: {file_label_item}", font=("Inclusive Sans", 20))
                    print(f"success! loaded {file_instance}")
                    counter = counter + 1
        
        else:
            print("Transmitter not loading for some reason")
    



    def clear_textbox(self) -> None:
        self.a20_listbox.delete(0, "end") 
        self.a20_listbox.insert(0, "Files will show here...")
        self.file_info_textbox.delete("1.0", "end")
        self.file_info_textbox.insert("2.0", "File details...")
        self.current_files: list = [] # empty the list 
        print("current files cleared")
        print(f"{self.current_files}")

#-------------------------------------------------
# Move the files to the folder
#-----------------------------------------------

    def call_move_files(self) -> None:
        if self.A20_path and self.folder_path:
            print("i see both paths")

            file_match = self._controller.match_files_to_folder(folder_path=self.folder_path, tx_path=self.A20_path)
            self._controller.move_files(file_match)
        else:
            print("Please select both paths before moving files.")


    def print_progress(self, copied, total, file_name) -> None:
        progress_bar = self._controller.update_custom_progress_bar(copied, total, file_name)
        self.terminal_textbox.delete("1.0", "end")
        self.terminal_textbox.configure(font=("Reddit Mono", 10))
        self.terminal_textbox.insert("end", progress_bar + '\n')
        
        # self.terminal_textbox.see("end")
        self.update()

#-----------------------------------
# Playback
#----------------------------------
    def play_selected_audio(self) -> None:

        
        index: tuple = self.a20_listbox.curselection() 
        selected_index: tuple = index
        if isinstance(selected_index, int):
            selected_file_path = self.file_paths[selected_index]

            if selected_file_path:
                
                print(f"playing: -> {selected_file_path}")
                print(f"Type of selected_file_path: {type(selected_file_path)}")
                print(f"Value of selected_file_path: {selected_file_path}")
                
                self.audio_player = AudioPlayer(selected_file_path)

                t1 = Thread(target=self.audio_player.play_audio_segment)
                t1.start()
                print("Started T1 thread")
        else:
            print("No file selected")



    def stop_playback(self):
        self.audio_player.stop()
        self.audio_player.reset()
  





app = App()
app.mainloop()

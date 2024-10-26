
from tkinter.constants import COMMAND
import customtkinter as ctk
from typing import LiteralString, Union, Callable
from utils.enums import Colour
from controllers.main_controller_v2 import MainController
from controllers.macos_drive_controller_v2 import FileReport
from controllers.file_storage import FileInfo
import logging
import time
import threading
import CTkListbox as lb
import subprocess

# when calling a function from any of the controller modules the syntax is
# "self.[_reference to controller as listed in script].function

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

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

        self._file_store = FileInfo()


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
        self.tx_refresh_button.configure(fg_color="transparent")

        self.A20_instance_label = ctk.CTkLabel(self.tx_list_frame)
        self.A20_instance_label.pack(side="left", padx=5, pady=5)
        self.A20_instance_label.configure(text="Transmitters", font=("Inclusive Sans", 20))

        self.options_frame = ctk.CTkFrame(self.frame_left)
        self.options_frame.pack(side="bottom", fill='both', pady=1, padx=1)
        self.options_frame.configure(fg_color="transparent")

        self.options_label = ctk.CTkLabel(self.options_frame)
        self.options_label.pack(padx=5, pady=5)
        self.options_label.configure(text="Options", font=("Inclusive Sans", 20))

        self.A20_path_button = ctk.CTkButton(self.options_frame, text="Manually Choose TX", command=self.manual_a20_sel_to_textbox)
        self.A20_path_button.pack(pady=10)
        self.A20_path_button.configure(fg_color=Colour.BUTTON.value)

        self.folder_path_button = ctk.CTkButton(self.options_frame, text="Choose Destination", command=self.update_label_with_folder_path)
        self.folder_path_button.pack(pady=10)
        self.folder_path_button.configure(fg_color=Colour.BUTTON.value)

        self.options_label = ctk.CTkLabel(self.frame_middle)
        self.options_label.pack(padx=5, pady=10)
        self.options_label.configure(text="File List", font=("Inclusive Sans", 20))


        self.a20_listbox = lb.CTkListbox(self.frame_middle,
                                         height=300,
                                         command=self.add_to_playback)

        self.a20_listbox.pack(fill="both", pady=0, padx=10)
        self.a20_listbox.insert(0, "Files will show here...")
        self.a20_listbox.configure(border_width=1,
                                   border_color=Colour.OFF_WHITE.value,
                                   fg_color=Colour.BACKGROUND_DARK.value,
                                   hover_color=Colour.GREY.value,
                                   highlight_color=Colour.BACKGROUND_COLOR.value,
                                   font=("Inclusive Sans", 13)
                                   )

        self.info_label = ctk.CTkLabel(self.frame_right)
        self.info_label.pack(padx=5, pady=10)
        self.info_label.configure(text="Copy Window", font=("Inclusive Sans", 20))


        self.terminal_textbox = ctk.CTkTextbox(self.frame_right, height=80)
        self.terminal_textbox.pack(fill="both", pady=0, padx=10)
        self.terminal_textbox.insert("2.0", "No folder selected...") # placeholder text
        self.terminal_textbox.configure(fg_color=Colour.BACKGROUND_DARK.value,
                                        border_width=1,
                                        border_color=Colour.OFF_WHITE.value,
                                        font=("Inclusive Sans", 13)
                                        )


        self.file_info_label = ctk.CTkLabel(self.frame_right)
        self.file_info_label.pack(padx=5, pady=5)
        self.file_info_label.configure(text="selected file info", font=("Inclusive Sans", 20))


        self.file_info_textbox = ctk.CTkTextbox(self.frame_right, height=150)
        self.file_info_textbox.pack(fill="both", pady=7, padx=10)
        self.file_info_textbox.insert("2.0", "No folder selected...") # placeholder text
        self.file_info_textbox.configure(fg_color=Colour.BACKGROUND_DARK.value,
                                        border_width=1,
                                        border_color=Colour.OFF_WHITE.value,
                                        font=("Inclusive Sans", 13)
                                        )


        self.options_frame_mid = ctk.CTkFrame(self.frame_middle)
        self.options_frame_mid.pack(side="bottom", pady=10, padx=1)
        self.options_frame_mid.configure(fg_color="transparent")

        self.extra_button = ctk.CTkButton(self.options_frame_mid, text="Show todays", command=self.add_to_playback)
        self.extra_button.pack(side="left", fill="x", padx=5, pady=0)
        self.extra_button.configure(fg_color=Colour.BUTTON.value)

        self.extra_button_two = ctk.CTkButton(self.options_frame_mid, text="Clear Files")
        self.extra_button_two.pack(side="left", fill="x", padx=5, pady=0)
        self.extra_button_two.configure(fg_color=Colour.BUTTON.value, command=self.clear_textbox)

        self.move_files_button = ctk.CTkButton(self.frame_right, text="Move Files to Folders", command=self.call_move_files)
        self.move_files_button.pack(side="bottom", fill="x", padx=5, pady=10)
        self.move_files_button.configure(fg_color=Colour.PINK.value)
        self.drive_buttons = {}


        self.playback_label = ctk.CTkLabel(self.frame_footer)
        self.playback_label.pack(side="left", padx=5, pady=5)
        self.playback_label.configure(text="Playback", font=("Inclusive Sans", 20))


        self.playhead_slider = ctk.CTkSlider(self.frame_footer)
        self.playhead_slider.pack(pady=20, padx=20)
        self.playhead_slider.configure(
            height=20,
            width=600,
            button_color=Colour.PINK.value,
            border_width=1,
            from_=0,
            to=100

        )

#-----------------------------------------
# Handle manual selection of transmitter
#------------------------------------------

    def manual_a20_sel_to_textbox(self) -> None:
          # Clear the text box immediately
        path = self._controller.select_A20_path()

        if path:
            # print(f"manual sel path : {path}")
            self.A20_path: str = path

            # Get the list of files from the selected path
            received_file_list: list = self._usb_controller.info_getter(path)
            # print(f"Received files: {received_file_list}")

            self.a20_listbox.delete(0, "end")

            # Check if any files were received and insert them into the text box
            if received_file_list:
                count = 0
                # self.a20_listbox.delete(0, "end")# Ensure the list is not empty
                for file_info in received_file_list:
                    stored_info: dict = {
                        "count" : f"{count}",
                        "info" : file_info['length']
                    }
                    display_text: str = f"{file_info['count']}    {file_info['file_name']}     {file_info['length']}     {file_info['start_tc']}     {file_info['mb']:.2f} MB"
                    # display_text: str = f"{file_info['count']}-{file_info['file_name']} : {file_info['mb']:.2f} MB : length-{file_info['length']} : start tc-{file_info['start_tc']}\n"
                    self.a20_listbox.insert("end", display_text)
                    count = count + 1

            else:
                print("No files found in the selected directory.")
        else:
            print("ERROR: No path selected.")

            return stored_info


    def add_to_playback(self, item):


        i = self.a20_listbox.curselection() # gets the selected item index in the listbox

        self._file_store.hold_files( item)

        print(f"File number {i + 1}")
        self.file_info_textbox.delete("1.0", "end")
        self.file_info_textbox.insert("2.0", f"File Number: {i}")



    def update_label_with_folder_path(self) -> None:
        self.folder_path: str = self._controller.folder_select_path()

        if self.folder_path:
            self.terminal_textbox.delete("1.0", "end")
            self.terminal_textbox.insert("end", text=f"Selected folder path:\n{self.folder_path}")
        else:
            print("No folder path selected.")



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
                self.drive_buttons[label] = button
                logging.info(f"Button for {label} packed successfully.")

        else:
            logging.info("No transmitters connected, soz.")


    def select_tx_button(self, a20_mount_point):# -> Any:# -> Any:# -> Any:
        self.a20_listbox.delete(0, "end")
        logging.info(f"Selected TX mount point: {a20_mount_point}")  # Log the selected mount point
        if a20_mount_point:
            received_file_list: str = self._usb_controller.info_getter(a20_mount_point)  # Retrieve the file list
            logging.info(f"Received file list: {received_file_list}")  # Log the received file list
            self.A20_path = a20_mount_point  # Store the selected mount point

            try:
                count: int = 0
                for file_info in received_file_list:
                    logging.info(f"Processing file info: {file_info}")  # Log each file info being processed
                    display_text = f"{file_info['count']}-{file_info['file_name']} : {file_info['mb']} MB : length-{file_info['length']} : start-{file_info['start_tc']}\n"
                    count: int = count + 1
                    self.a20_listbox.insert(f"{count}", display_text)  # Populate the text box
                logging.info("File list populated in the text box.")  # Log successful population
            except ValueError as e:
                logging.error(f"Error loading A20 mount point: {e}")  # Log any errors encountered
        else:
            logging.warning("No mount point selected.")  # Log if no mount point is provided
        return a20_mount_point

    def clear_textbox(self) -> None:
        self.a20_listbox.delete(0, "end")


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
        self.terminal_textbox.insert("end", progress_bar + '\n')
        # self.terminal_textbox.see("end")
        self.update()



    def play_selected_audio(self) -> None:
        """Play the selected audio file."""
        self.play_audio(self.audio_file_path)


    def play_audio(self, file_path: str) -> None:
        """Play audio using FFmpeg."""
        try:
            subprocess.run(['ffmpeg', '-i', file_path, '-f', 'alsa', 'default'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while trying to play the audio: {e}")

app = App()
app.mainloop()

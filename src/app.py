import customtkinter as ctk
import os
from typing import Union, Callable
from utils.enums import Colour
from controllers.main_controller import MainController
from controllers.drive_controller import DriveController

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._controller = MainController()
        self._drive_controller = DriveController()
        # self._controller: Union[MainController, None] =None
        self.geometry("1000x500")

        self.title("A20 TX File Mover")

        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)


        

        self.A20_path = ""
        self.folder_path = ""
        self.create_layout()
# Heading

    def create_layout(self):

        self.frame_header = ctk.CTkFrame(self, fg_color=Colour.BLUE.value)
        self.frame_header.grid(row=0, columnspan=3, padx=5, pady=5, sticky="nswe")
        
        self.label_heading =ctk.CTkLabel(self.frame_header)
        self.label_heading.pack(side="left", padx=10, pady=10)
        self.label_heading.configure(text="A20 TX - FILE MOVER", font=("Inclusive Sans", 25))
        
        current_time = self._controller.global_time()

        self.time_heading =ctk.CTkLabel(self.frame_header)
        self.time_heading.pack(side="right", padx=10)
        self.time_heading.configure(text=f"{current_time}", font=("Inclusive Sans", 15))
        
        self.frame_left = ctk.CTkFrame(self, fg_color=Colour.BACKGROUND_COLOR.value)
        self.frame_left.grid(row=1, column=0, rowspan=2, padx=5, pady=5, sticky="nswe")
        self.frame_left.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)

        self.frame_middle = ctk.CTkFrame(self, fg_color=Colour.BACKGROUND_COLOR.value)
        self.frame_middle.grid(row=1, column=1, rowspan=2, padx=5, pady=5, sticky="nswe")
        self.frame_middle.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)

        self.frame_right = ctk.CTkFrame(self, fg_color=Colour.BACKGROUND_COLOR.value)
        self.frame_right.grid(row=1, column=2, rowspan=2, padx=5, pady=5, sticky="nswe")
        self.frame_right.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)
        
        self.folder_path_select = ctk.CTkButton(self.frame_middle, text="Choose Folder Path", command=self.update_textbox_with_folder_path)
        self.folder_path_select.pack(pady=20)

# Textbox for folder path

        self.folder_textbox = ctk.CTkTextbox(self.frame_middle, height=300, wrap=ctk.WORD)
        self.folder_textbox.pack(fill="x", expand=True, pady=10, padx=20)
        self.folder_textbox.insert("1.0", "No folder selected") # placeholder text
        self.folder_textbox.configure(border_width=1, border_color=Colour.OFF_WHITE.value)




# Manually select path to A20 mount

        self.A20_path_select = ctk.CTkButton(self.frame_left, text="Manually Choose A20", command=self.update_textbox_with_A20_path)
        self.A20_path_select.pack(pady=10)

        self.A20_textbox = ctk.CTkTextbox(self.frame_left, height=100)
        self.A20_textbox.pack(side= "bottom", fill="x", expand=True, pady=10, padx=20)
        self.A20_textbox.insert("2.0", "No A20 selected") # placeholder text
        self.A20_textbox.configure(border_width=1, border_color=Colour.OFF_WHITE.value)


        self.move_files_button = ctk.CTkButton(self.frame_right, text="Move Files to Folders", command=self.call_move_files)
        self.move_files_button.pack(pady=20)
        
# Progress bar

        self.progressbar = ctk.CTkProgressBar(self.frame_right)
        self.progressbar.pack(padx=10, pady=10)
        self.progressbar.configure(fg_color=Colour.ORANGE.value, progress_color=Colour.OFF_WHITE.value)
        self.progressbar.set(0)

        self.drive_buttons = {}

        self.update_drives()

        self.schedule_drive_update()
    
    updated_date = MainController.A20_convert_name
    
    def update_textbox_with_A20_path(self):
            path = self._controller.select_A20_path()
            new_names = self._controller.A20_convert_name(path)
            self.A20_textbox.delete("1.0", "end")
            for name in new_names:
                self.A20_textbox.insert("end", name + "\n")


    def update_textbox_with_folder_path(self):
        self.folder_path = self._controller.select_folder_path()
        if self.folder_path:
            folder_list = os.listdir(self.folder_path)
            self.folder_textbox.delete("1.0", "end")
            self.folder_textbox.insert("end",
                                         text=f"PATH:\n\n{self.folder_path}\n\nFOLDERS:\n"
                                         )
            for folder in folder_list:
                full_path = os.path.join(self.folder_path, folder)
                if os.path.isdir(full_path):
                    self.folder_textbox.insert("end", folder + "\n")

    def schedule_drive_update(self):
        """
        Schedule an update of the drive list every 5000 ms (5 seconds).
        """
        self._drive_controller.update_drive_list(self.update_drives)
        self.after(5000, self.schedule_drive_update)

# Automatic button creation for any A20 TX found to be plugged in using VID. 
    def update_drives(self, tx_devices=None):
        if tx_devices is None:
            tx_devices = self._drive_controller.get_VID()

        new_drives = set(device['device_node'] for device in tx_devices)
            # update_drives = self._drive_controller.update_drive_list()
        for drive in list(self.drive_buttons.keys()):
            if drive not in new_drives:
                self.drive_buttons[drive].destroy()
                del self.drive_buttons[drive]
            
        for device in tx_devices:
            device_node = device['device_node']
            mount_point = device['mount_point']
            if mount_point is not None:
                drive_label = os.path.basename(mount_point)
                if device_node not in self.drive_buttons:
                    button = ctk.CTkButton(self.frame_left,
                        text=f"TX: {drive_label}"
                    )
                    button.pack(pady=10)
                    self.drive_buttons[device_node] = button
            else:
                print("whatever man")
            self.after(5000, self._drive_controller.update_drive_list)



    def update_progress(self, progress):
        self.progressbar.set(progress)

    def call_move_files(self):
        
        if self.A20_path and self.folder_path:
            self._controller.move_files(self.A20_path, self.folder_path, self.update_progress)
        else:
            print("Please select both paths before moving files.")

app = App()
app.mainloop()
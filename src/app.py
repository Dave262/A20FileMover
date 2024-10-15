import customtkinter as ctk
import os
from typing import Union, Callable
from utils.enums import Colour
from controllers.main_controller import MainController

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._controller = MainController() 

        # self._controller: Union[MainController, None] =None

        self.geometry("900x500")
        self.title("A20 TX File Mover")

        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

        self.A20_path = ""
        self.folder_path = ""

# Heading

        frame_header = ctk.CTkFrame(self, fg_color=Colour.BLUE.value)
        frame_header.grid(row=0, columnspan=3, padx=5, pady=5, sticky="nswe")
        
        self.label_heading =ctk.CTkLabel(frame_header)
        self.label_heading.pack(side="left", padx=10, pady=10)
        self.label_heading.configure(text="A20 TX - FILE MOVER", font=("Inclusive Sans", 25))
        
        current_time = self._controller.global_time()

        self.time_heading =ctk.CTkLabel(frame_header)
        self.time_heading.pack(side="right", padx=10)
        self.time_heading.configure(text=f"{current_time}", font=("Inclusive Sans", 15))
        
        frame_left = ctk.CTkFrame(self, fg_color=Colour.BACKGROUND_COLOR.value)
        frame_left.grid(row=1, column=0, rowspan=2, padx=5, pady=5, sticky="nswe")
        frame_left.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)

        frame_middle = ctk.CTkFrame(self, fg_color=Colour.BACKGROUND_COLOR.value)
        frame_middle.grid(row=1, column=1, rowspan=2, padx=5, pady=5, sticky="nswe")
        frame_middle.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)

        frame_right = ctk.CTkFrame(self, fg_color=Colour.BACKGROUND_COLOR.value)
        frame_right.grid(row=1, column=2, rowspan=2, padx=5, pady=5, sticky="nswe")
        frame_right.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)
        
        

        button_select_folder = ctk.CTkButton(frame_left, text="Choose Folder Path", command=self.update_textbox_with_folder_path)
        button_select_folder.pack(pady=20)


        # self.label_dir_path = ctk.CTkLabel(frame_left, height=20)
        # self.label_dir_path.pack(fill="x", expand=True, pady=10, padx=10)
        # # self.label_dir_path.insert("1.0", "no folder path") # placeholder text
        # self.label_dir_path.configure(text="no folder path")
# Textbox for folder path

        self.textbox_dir_list = ctk.CTkTextbox(frame_left, height=300, wrap=ctk.WORD)
        self.textbox_dir_list.pack(fill="x", expand=True, pady=10, padx=20)
        self.textbox_dir_list.insert("1.0", "No folder selected") # placeholder text
        self.textbox_dir_list.configure(border_width=1, border_color=Colour.OFF_WHITE.value)

#A20 Files
        
        button_select_A20 = ctk.CTkButton(frame_middle, text="Choose A20 Path", command=self.update_textbox_with_A20_path)
        button_select_A20.pack(pady=20)

        # self.label_A20_path = ctk.CTkLabel(frame_middle, height=20)
        # self.label_A20_path.pack(fill="x", expand=True, pady=10, padx=20)
        # self.label_A20_path.configure(text="no A20 selected")

        self.textbox_A20_list = ctk.CTkTextbox(frame_middle, height=300)
        self.textbox_A20_list.pack(fill="x", expand=True, pady=10, padx=20)
        self.textbox_A20_list.insert("1.0", "No A20 selected") # placeholder text
        self.textbox_A20_list.configure(border_width=1, border_color=Colour.OFF_WHITE.value)


        button_move_files = ctk.CTkButton(frame_right, text="Move Files to Folders", command=self.call_move_files)
        button_move_files.pack(pady=20)
        
# Progress bar

        self.progressbar = ctk.CTkProgressBar(frame_right)
        self.progressbar.pack(padx=10, pady=10)
        self.progressbar.configure(fg_color=Colour.ORANGE.value, progress_color=Colour.OFF_WHITE.value)
        self.progressbar.set(0)

    
    updated_date = MainController.extract_numbers_convert
    
    def update_textbox_with_A20_path(self):
        self.A20_path = self._controller.select_A20_path()
        # self.label_A20_path.configure(text=f"A20 Folder: {self.A20_path}")

        if self.A20_path:
            file_list = os.listdir(self.A20_path)  
            self.textbox_A20_list.delete("1.0", "end")
            self.textbox_A20_list.insert("end",
                                         text=f"--------------- PATH ---------\n{self.folder_path}\n\n\n ------------- FOLDERS ---------\n"
                                         )
            self.textbox_A20_list.delete("1.0", "end")
            for file in file_list:
                self.textbox_A20_list.insert("end", file + "\n")


    def update_textbox_with_folder_path(self):
        self.folder_path = self._controller.select_folder_path()
        # self.label_dir_path.configure(text=f"Destination Folder: {self.folder_path}")

        if self.folder_path:
            folder_list = os.listdir(self.folder_path)
            self.textbox_dir_list.delete("1.0", "end")
            self.textbox_dir_list.insert("end",
                                         text=f"----------------- PATH --------------\n\n{self.folder_path}\n\n --------------- FOLDERS ------------\n"
                                         )
            for folder in folder_list:
                full_path = os.path.join(self.folder_path, folder)
                if os.path.isdir(full_path):
                    self.textbox_dir_list.insert("end", folder + "\n")

        
    def update_progress(self, progress):
        self.progressbar.set(progress)

    def call_move_files(self):
        
        if self.A20_path and self.folder_path:
            self._controller.move_files(self.A20_path, self.folder_path, self.update_progress)
        else:
            print("Please select both paths before moving files.")
 

app = App()
app.mainloop()
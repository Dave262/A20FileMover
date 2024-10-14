import customtkinter as ctk
from file_move import select_folder_path, select_A20_path, move_files
from file_sorter import global_time, extract_numbers_convert
import style_sheet
import os
import shutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x480")
        self.title("A20 TX File Mover")

        self.grid_rowconfigure((0,1), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.A20_path = ""
        self.folder_path = ""

        frame_left = ctk.CTkFrame(self)
        frame_left.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nswe")

        frame_right = ctk.CTkFrame(self)
        frame_right.grid(row=0, column=1, rowspan=2, columnspan=2, padx=5, pady=5, sticky="nswe")

        frame_right.grid_rowconfigure(0, weight=1)
        frame_right.grid_rowconfigure(1, weight=0)
        frame_right.grid_columnconfigure((0, 1), weight=1)

        subframe_right_L = ctk.CTkFrame(frame_right)
        subframe_right_L.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

        subframe_right_R = ctk.CTkFrame(frame_right)
        subframe_right_R.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
# Progress bar


        self.progressbar = ctk.CTkProgressBar(frame_right)
        self.progressbar.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=10)
        self.progressbar.configure(fg_color=style_sheet.BACKGROUND_DARK, progress_color=style_sheet.OFF_WHITE)
        self.progressbar.set(0)




        button_select_folder = ctk.CTkButton(frame_left, text="Choose Folder Path", command=self.update_textbox_with_folder_path)
        button_select_folder.pack(pady=20)


# Textbox for folder path
        self.label_dir_path = ctk.CTkLabel(subframe_right_L, height=20)
        self.label_dir_path.pack(fill="x", expand=True, pady=10, padx=10)
        # self.label_dir_path.insert("1.0", "no folder path") # placeholder text
        self.label_dir_path.configure(text="no folder path")


        self.textbox_dir_list = ctk.CTkTextbox(subframe_right_L, height=180)
        self.textbox_dir_list.pack(fill="x", expand=True, pady=10, padx=20)
        self.textbox_dir_list.insert("1.0", "This is where your folder list will appear") # placeholder text
        self.textbox_dir_list.configure(border_width=1, border_color=style_sheet.YELLOW)


#A20 Files
        
        button_select_A20 = ctk.CTkButton(frame_left, text="Choose A20 Path", command=self.update_textbox_with_A20_path)
        button_select_A20.pack(pady=20)


        self.label_A20_path = ctk.CTkLabel(subframe_right_L, height=20)
        self.label_A20_path.pack(fill="x", expand=True, pady=10, padx=20)
        self.label_A20_path.configure(text="no A20 selected")


        self.textbox_A20_list = ctk.CTkTextbox(subframe_right_L, height=180)
        self.textbox_A20_list.pack(fill="x", expand=True, pady=10, padx=20)
        self.textbox_A20_list.insert("1.0", "This is where your A20 files will appear") # placeholder text
        self.textbox_A20_list.configure(border_width=1, border_color=style_sheet.YELLOW)



        button_move_files = ctk.CTkButton(frame_left, text="Move Files to Folders", command=self.call_move_files)
        button_move_files.pack(pady=20)



    
    def update_textbox_with_A20_path(self):
        self.A20_path = select_A20_path()
        self.label_A20_path.configure(text=f"A20 Folder: {self.A20_path}")

        if self.A20_path:
            file_list = os.listdir(self.A20_path)  
            self.textbox_A20_list.delete("1.0", "end")
            for file in file_list:
                self.textbox_A20_list.insert("end", file + "\n")



    def update_textbox_with_folder_path(self):
        self.folder_path = select_folder_path()
        self.label_dir_path.configure(text=f"Destination Folder: {self.folder_path}")

        if self.folder_path:
            folder_list = os.listdir(self.folder_path)
            self.textbox_dir_list.delete("1.0", "end")
            for folder in folder_list:
                self.textbox_dir_list.insert("end", folder + "\n")

        
    def update_progress(self, progress):
        self.progressbar.set(progress)

    def call_move_files(self):
        if self.A20_path and self.folder_path:
            move_files(self.A20_path, self.folder_path, self.update_progress)
        else:
            print("Please select both paths before moving files.")
 








app = App()
app.mainloop()
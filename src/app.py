from typing import Union
import customtkinter as ctk
from typing import Union, Callable
from utils.enums import Colour
from controllers.main_controller import MainController
# from src.controllers.macos_drive_controller_v2 import MacUsbDeviceController
from controllers.linux_drive_controller import LinuxDeviceHandler
from utils.system_get import SystemGet
# from controllers.mac_usb_controller_v1 import MacUsbControlerV1
from controllers.macos_drive_controller_v2 import FileReport


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
        self.grid_columnconfigure((0,1,2), weight=1)  
        
        self.geometry("1000x500")
        self.title("A20 TX File Mover")
        

        system_get = SystemGet()
        system_platform = system_get.system_trigger()

        if system_platform == "Darwin":
            self._usb_controller = FileReport()
        elif system_platform == "Linux":
            self._usb_controller  = LinuxDeviceHandler()
        else:
            raise Exception(f"Unsupported platform: {system_platform}")

        # init controllers
        self._controller = MainController()
        # self._usb_controller = MacUsbDeviceController()   

        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((1,2), weight=1)
        self.grid_columnconfigure((0), weight=0)

        self.A20_path = ""
        self.folder_path = ""
        self.create_layout()
        self.create_tx_buttons()

# Heading
    def create_layout(self):

        self.frame_header = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_header.grid(row=0, columnspan=3, padx=1, pady=1, sticky="nswe")
        
        self.label_heading =ctk.CTkLabel(self.frame_header)
        self.label_heading.pack(side="left", padx=10, pady=10)
        self.label_heading.configure(text="A20 TX - FILE MOVER", font=("Inclusive Sans", 25))
        

        self.time_heading =ctk.CTkLabel(self.frame_header)
        self.time_heading.pack(side="right", padx=10)
        self.time_heading.configure(text=f"{self._controller.global_time()}", font=("Inclusive Sans", 15))
        
        self.frame_left = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_left.grid(row=1, column=0, rowspan=2, padx=3, pady=3, sticky="nswe")
        self.frame_left.configure()

        self.frame_middle = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_middle.grid(row=1, column=1, rowspan=2, padx=3, pady=3, sticky="nswe")
        self.frame_middle.configure()

        self.frame_right = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_right.grid(row=1, column=2, rowspan=2, padx=3, pady=3, sticky="nswe")
        self.frame_right.configure()
        
        # self.folder_path_select = ctk.CTkButton(self.frame_middle, text="Choose Folder Path", command=self.update_textbox_with_folder_path)
        # self.folder_path_select.pack(pady=20)

# Folder Stuff

        self.folder_label = ctk.CTkTextbox(self.frame_right, height=50, fg_color="transparent")
        self.folder_label.pack(fill="x", pady=10, padx=20)
        self.folder_label.insert("0.0", "Placeholder Folder Ha!")

        self.A20_instance_frame = ctk.CTkFrame(self.frame_left)
        self.A20_instance_frame.pack(side="top", pady=1, padx=1)
        self.A20_instance_frame.configure(fg_color="transparent", border_width=2, border_color=Colour.OFF_WHITE.value)
        
        self.A20_instance_label = ctk.CTkLabel(self.A20_instance_frame)
        self.A20_instance_label.pack(padx=5, pady=5)
        self.A20_instance_label.configure(text="Transmitter List", font=("Inclusive Sans", 20))

        self.options_frame = ctk.CTkFrame(self.frame_left)
        self.options_frame.pack(side="bottom", fill='both', pady=1, padx=1)
        self.options_frame.configure(fg_color="transparent", border_width=2, border_color=Colour.OFF_WHITE.value)
        
        self.options_label = ctk.CTkLabel(self.options_frame)
        self.options_label.pack(padx=5, pady=5)
        self.options_label.configure(text="Options", font=("Inclusive Sans", 20))
        
        self.A20_path_button = ctk.CTkButton(self.options_frame, text="Manually Choose TX", command=self.manual_a20_sel_to_textbox)
        self.A20_path_button.pack(pady=10)
        self.A20_path_button.configure(fg_color=Colour.PINK.value)
        
                
        self.folder_path_button = ctk.CTkButton(self.options_frame, text="Choose Destination", command=self.update_label_with_folder_path)
        self.folder_path_button.pack(pady=10)
        self.folder_path_button.configure(fg_color=Colour.PINK.value)       
        
        self.options_label = ctk.CTkLabel(self.frame_middle)
        self.options_label.pack(padx=5, pady=5)
        self.options_label.configure(text="File List", font=("Inclusive Sans", 20))

        self.A20_textbox = ctk.CTkTextbox(self.frame_middle, height=300)
        self.A20_textbox.pack(side= "top", fill="x", pady=10, padx=10)
        self.A20_textbox.insert("2.0", "A20 files will show here...") # placeholder text
        self.A20_textbox.configure(border_width=1, border_color=Colour.OFF_WHITE.value)
        
        self.options_frame_mid = ctk.CTkFrame(self.frame_middle)
        self.options_frame_mid.pack(side="bottom", pady=1, padx=1)
        self.options_frame_mid.configure(fg_color=Colour.BACKGROUND_COLOR.value, border_width=2, border_color=Colour.OFF_WHITE.value)
        
        self.extra_button = ctk.CTkButton(self.options_frame_mid, text="file names")
        self.extra_button.pack(side="left", fill="x", padx=5, pady=2)
        self.extra_button.configure(fg_color=Colour.PINK.value)
        
        
        self.extra_button_two = ctk.CTkButton(self.options_frame_mid, text="placeholder")
        self.extra_button_two.pack(side="left", fill="x", padx=5, pady=2)
        self.extra_button_two.configure(fg_color=Colour.PINK.value)
        
        
        self.extra_button_three = ctk.CTkButton(self.options_frame_mid, text="placeholder")
        self.extra_button_three.pack(side="left", fill="x", padx=5, pady=2)
        self.extra_button_three.configure(fg_color=Colour.PINK.value)


        self.move_files_button = ctk.CTkButton(self.frame_right, text="Move Files to Folders", command=self.call_move_files)
        self.move_files_button.pack(pady=20)
        self.drive_buttons = {}       




# Progress bar


        self.progress_bar = ctk.CTkProgressBar(self.frame_right)
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar.configure(fg_color=Colour.PINK.value, progress_color=Colour.OFF_WHITE.value)
        self.progress_bar.set(0)
  
    updated_date = MainController.A20_convert_name
    
    
    def manual_a20_sel_to_textbox(self):
            """_summary_
            passes the contents of a manually selected drive through the file renamer to the a20 textbox
            """
            
            path = self._controller.select_A20_path()
            
            if path:
                self.A20_path = path
            
                new_names = self._controller.A20_convert_name(path)
                self.A20_textbox.delete("1.0", "end")
                for name in new_names:
                    self.A20_textbox.insert("end", name + "\n")
            else:
                print("No path for A20")
    
    def update_label_with_folder_path(self):        
        self.folder_path = self._controller.select_folder_path()
       
        if self.folder_path:
            self.folder_label.delete("1.0", "end")
            self.folder_label.insert("end", text=f"{self.folder_path}")
                                   
            print(f"Folder path set to: {self.folder_path}")
        else:
            print("No folder path selected.")
        

    
    def create_tx_buttons(self, passed_label_list=None):
        
        if passed_label_list is None:
            passed_label_list = self._usb_controller.mount_drives() # definine the list

# Clear any existing drive buttons
        for button in self.drive_buttons.values():
            button.destroy()
        self.drive_buttons.clear()        
        # for drive_info in passed_label_list:
        
        for tx in passed_label_list:
            print(tx)
    # Create a new button
            button = ctk.CTkButton(self.A20_instance_frame, text=f"TX: {tx}", command=lambda tx_button=tx: self.handle_drive_selection(tx_button))
            button.pack(pady=10)  # Adjust layout as needed       

    # Store the button in the dictionary for future reference
            self.drive_buttons[tx] = button 
            # self.after(5000, self._usb_controller.mount_drives)
                
    
    def handle_drive_selection(self, a20_mount_point):
        if a20_mount_point:
            received_file_list = self._usb_controller.info_getter()
            self.A20_path = a20_mount_point # gets a20 files ready to move
            try:
                self.A20_textbox.delete("1.0", "end") 
                for file_info in received_file_list:
                    display_text = f"{file_info['count']}-{file_info['file_name']} : {file_info['mb']} MB : start tc-{file_info['start_tc']}\n" 
                    self.A20_textbox.insert("end", display_text)
                print(f"handle_drive_selection can see: {a20_mount_point}")
            except ValueError:
                print("Couldn't load a20 mount pointt")
        return a20_mount_point    

    
    def update_progress(self, progress):
        self.progressbar.set(progress)

    
    def call_move_files(self):

        
        if self.A20_path and self.folder_path:
            print("i see both paths")
            self._controller.move_files(self.A20_path, self.folder_path, app.progress_bar)

        else:
            print("Please select both paths before moving files.")

app = App()
app.mainloop()

import os, pyudev, psutil
import customtkinter as ctk
from tkinter import filedialog, messagebox


class AutoMount(object):
  def __init__(self, ):
    super().__init__()
    
    
    self.destination_dir = None
    self.list_drives()



  def list_drives(self):
    target_vid = "1fc9"
    
    context = pyudev.Context
    for drive in context.list_devices(subsystem='usb'):
      vid = drive.get("ID_VENDOR_ID")
      if vid == target_vid:
        print(f"found matching vid: {vid}")
        

if __name__ == "__main__":
  auto_mount = AutoMount()
  connected_drives = auto_mount.list_drives()


  
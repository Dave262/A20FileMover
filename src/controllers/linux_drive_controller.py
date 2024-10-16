import os
import pyudev
import psutil
import customtkinter as ctk
from tkinter import filedialog, messagebox


class DriveController:
    def __init__(self):
        super().__init__()
        self.destination_dir = None
        # self.drive_buttons = {} 
        self.update_drive_list()


    def select_destination(self):
        self.destination_dir = filedialog.askdirectory()
        if self.destination_dir:
            messagebox.showinfo("Destination Set", f"Destination directory set to:\n{self.destination_dir}")

    def get_mount_point(self, device_node):
        """
        Find the mount point of a given block device.
        """
        for partition in psutil.disk_partitions():
            if device_node in partition.device:
                return partition.mountpoint
        return None

    def get_VID(self):
        target_vid = "1fc9"
        context = pyudev.Context()
        devices = []
        for device in context.list_devices(subsystem='usb'):
            vid = device.get('ID_VENDOR_ID')
            if vid == target_vid:
                for child in device.children:
                    if child.subsystem == 'block' and child.device_type == 'disk':
                        mount_point = self.get_mount_point(child.device_node)
                        devices.append({
                            'vid': vid,
                            'mount_point': mount_point,
                            'device_node': child.device_node
                        })
                        print(f"Found device with VID {vid} at {mount_point} ({child.device_node})")
        return devices

    def update_drive_list(self, update_ui_callback=None):
        """
        get a list of all mounted drives
        """
        tx_devices = self.get_VID()
        new_drives = set(device['device_node'] for device in tx_devices)

        for device in tx_devices:
            device_node = device['device_node']
            mount_point = device['mount_point']
            if mount_point is not None:
                drive_label = os.path.basename(mount_point)
                print(f"{drive_label}:{tx_devices}")

            else:
                print(f"Warning: No mount point found for device {device_node}")
        
        if update_ui_callback:
            update_ui_callback(tx_devices)

        return tx_devices
        

if __name__ == "__main__":
    controller = DriveController()
    # devices = controller.update_drive_list()

   
    # app.mainloop()   
    
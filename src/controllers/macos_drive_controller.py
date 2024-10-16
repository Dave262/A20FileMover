import psutil
import usb.core
import usb.util

class MacUsbDeviceController:
    def __init__(self):
        super().__init__()

    def list_drives(self):
        drives_info = [] # blank list that will hold the device info
        drives = psutil.disk_partitions()
        usb_devices = usb.core.find(find_all=True)
        usb_device_info = {f"{hex(device.idVendor)}:{hex(device.idProduct)}": usb.util.get_string(device, device.iProduct) for device in usb_devices}

        # Use a set to track unique mount points
        unique_mountpoints = set()

        for drive in drives:
            if 'exfat' in drive.fstype.lower():
                drive_label = drive.mountpoint.replace("/Volumes/","")   
                for usb_device_key, product in usb_device_info.items():
                    vid, pid = usb_device_key.split(':')
                    # Check if the mount point is already added
                    if drive.mountpoint not in unique_mountpoints:
                        drives_info.append({
                            'name': drive_label,
                            'vid': vid,
                            # 'pid': pid,
                            'model': product,
                            'mountpoint': drive.mountpoint
                        })
                        unique_mountpoints.add(drive.mountpoint)  # Add to the set to track unique mount points

        # Debugging: Print the collected drives
        print("Collected Drives Info:", drives_info)

        return drives_info  # Return the filtered list of unique drives

if __name__ == "__main__":
    usb_controller = UsbDeviceHandler()
    drives = usb_controller.list_drives()  # Call the method
    print("Detected USB drives:")
    for drive in drives:
        print(drive) 
    

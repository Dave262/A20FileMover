import psutil
import usb.core


class MacUsbControlerV1:
    def __init__(self):
        super().__init__()

    def list_drives(self):
        """
        Analyses all drives on the system and returns a list of dictionaries containing info for each 'exfat' drive.
        :return: list_of_drives
        """
        list_of_drives = []
        system_drives = psutil.disk_partitions()

        for exfat_drive in system_drives:
            if exfat_drive.fstype == "exfat":
                drive_info = {
                    'device': exfat_drive.device,
                    'mountpoint': exfat_drive.mountpoint,
                    'fstype': exfat_drive.fstype
                }

                # Get additional USB info
                device_info = usb.core.find(find_all=True)
                for drive in device_info:
                    drive_info.update({
                        'VID': hex(drive.idVendor),
                        'Model': usb.util.get_string(drive, drive.iProduct)
                    })

                list_of_drives.append(drive_info)

        if list_of_drives:
            print(list_of_drives)
            return list_of_drives
        else:
            print("No exfat drives found")
            return []

if __name__ == "__main__":
    usb_controller = MacUsbControlerV1()
    drive_dict = usb_controller.list_drives()  # Call the method

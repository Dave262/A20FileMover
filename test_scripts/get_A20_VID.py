import pyudev
import psutil

def get_usb_device_info():
    """
    Get a list of all USB storage devices with their VID, PID, and mount point.
    """
    context = pyudev.Context()
    devices = []
    for device in context.list_devices(subsystem='usb'):
        vid = device.get('ID_VENDOR_ID')
        pid = device.get('ID_MODEL_ID')

        # Check if VID and PID exist and this is a USB storage device
        if vid and pid:
            # Find associated block device (usually the actual storage)
            for child in device.children:
                if child.subsystem == 'block' and child.device_type == 'disk':
                    mount_point = get_mount_point(child.device_node)
                    devices.append({
                        'name': child.device_node,
                        'vid': vid,
                        'pid': pid,
                        'mount_point': mount_point
                    })
                    print(f"Drive: {child.device_node}, VID: {vid}, PID: {pid}, Mount point: {mount_point}")
    return devices

def get_mount_point(device_node):
    """
    Find the mount point of a given block device.
    """
    for partition in psutil.disk_partitions():
        if device_node in partition.device:
            return partition.mountpoint
    return None

# Example usage
usb_devices = get_usb_device_info()



# VID = 1fc9
# PID = 009f
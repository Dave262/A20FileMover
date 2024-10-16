import os 
import platform

class SystemGet:
    def __init__(self):
        super().__init__()

    def system_trigger():
        system_name = os.name
        system_platform = platform.system()
        return system_platform, system_name
    
    
if __name__ == "__main__":
    system_get = SystemGet
    system_name= system_get.system_trigger()
    print(system_name)
    
import os 
import platform

class SystemGet:
    def __init__(self):
        super().__init__()


    def system_trigger(self):
        """_summary_
        Checks the system being used and returns it as a string.

        Returns:
            _type_: str 

        """
        # system_name = os.name
        system_platform = platform.system()
        print(f"Operating system = {system_platform}")
        return system_platform


if __name__ == "__main__":
    system_get = SystemGet()
    system_get.system_trigger()
    # system_name= system_get.system_trigger()


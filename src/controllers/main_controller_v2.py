import hashlib
import os
import re
import time
from tkinter import filedialog

# import wavinfo
from tqdm import tqdm


class MainController:
    def __init__(self, update_gui_callback):
        super().__init__()

        self.update_gui_callback = update_gui_callback

    # ---------------
    # Get Date
    # ---------------

    def global_time(self) -> str:
        """
          summary_
        Uses time module to get the current date based on users system.
          Returns:
              str: month day year eg. (October 25 2024)
        """
        # time_object = time.localtime()
        local_date: str = time.strftime("%B %d %Y")  # date but no time
        print(local_date)
        return local_date

    # ------------------
    # File Functions
    # ------------------

    def folder_select_path(self) -> str:
        folder_path: str = filedialog.askdirectory(
            initialdir="/home/david/Python_Projects/Fake_Folders/",
            title="Select destination folder",
        )
        print(f"Destination path : {folder_path}")
        return folder_path

    def select_A20_path(
        self,
    ) -> str:
        tx_path: str = filedialog.askdirectory(
            initialdir="/home/david/Python_Projects/",
            title="please select your A20 pack",
        )
        return tx_path

    def match_files_to_folder(self, folder_path: str, tx_path: str) -> None:
        """
        Makes a dictionary of the tx_path and folder_path names : paths and then matches them based on names
        it then creates a new dictionary 'file_and_folder_dict' which is each file and the path to the folder it matches.

        Args:
            folder_path (str): can be user selected
            tx_path (str): can be user selected or taken from tx button
        """
        if folder_path and tx_path:
            print(f"The folder path is: {folder_path}")
            # Folder dictionary creation
            folder_list: list = [
                folder
                for folder in os.listdir(folder_path)
                if re.match(r"^[^.]+$", folder)
            ]
            folder_dict: dict = {
                folder: os.path.join(folder_path, folder) for folder in folder_list
            }
            for folder, path in folder_dict.items():
                print(f"{folder} : {path}")

            # Transmitter dictionary
            tx_files: list = os.listdir(
                tx_path
            )  # this will include hidden files and non-wav files
            file_and_folder_dict = {}  # init dict

            for file in tx_files:
                if file.endswith(".wav"):
                    for folder in folder_dict:
                        if folder.lower() in file.lower():  # only return wav files
                            file_and_folder_dict[os.path.join(tx_path, file)] = (
                                os.path.join(folder_path, folder)
                            )

            for (
                key,
                value,
            ) in file_and_folder_dict.items():  # full file path and full folder path
                # print(file_and_folder_dict)
                return file_and_folder_dict

    def calculate_checksum(
        self, file_path, hash_algo="md5"
    ) -> str:  # calculating checksum for src and dst before deleting files.
        """
        MD5 checksum performed before the file move and after

        Args:
            file_path (_type_): _description_
            hash_algo (str, optional): _description_. Defaults to 'md5'.

        Returns:
            str: _description_
        """
        hash_func = hashlib.new(hash_algo)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def move_files(self, file_and_folder_dict) -> None:
        """
        Moves files to their respective folders based on name matching

        Parameters:
            file_and_folder_dict (dict): A dictionary of file paths and their corresponding destination folders.

        Returns:
            None

        Raises:
            Exception: If there is an error moving the files.
        """
        if file_and_folder_dict:
            print("Moving files...")
            try:
                for file_path, folder_path in file_and_folder_dict.items():
                    file_size: int = os.path.getsize(file_path)
                    file_name = os.path.basename(file_path)
                    print(f"Copying - {file_name} with size {file_size/1048576:.1f} mb")

                    source_checksum = self.calculate_checksum(file_path, "md5")

                    destination_file_path = os.path.join(
                        folder_path, os.path.basename(file_path)
                    )

                    with open(file_path, "rb") as src_file, open(
                        destination_file_path, "wb"
                    ) as dst_file:
                        with tqdm(
                            total=file_size,
                            desc="Progress: ",
                            unit="B",
                            unit_scale=True,
                        ) as progress_bar:
                            total_bytes_copied = 0
                            for chunk in iter(lambda: src_file.read(1024 * 1024), b""):
                                dst_file.write(chunk)

                                total_bytes_copied += len(chunk)
                                progress_bar.update(len(chunk))

                                self.update_gui_callback(
                                    total_bytes_copied,
                                    file_size,
                                    os.path.basename(file_path),
                                )
                            self.update_gui_callback(
                                file_size, file_size, os.path.basename(file_path)
                            )
                    destination_checksum = self.calculate_checksum(
                        destination_file_path, "md5"
                    )

                    if source_checksum != destination_checksum:
                        raise Exception(
                            f"Checksum mismatch for {file_name}, copy might be corrupted."
                        )
                    else:
                        print(f"Checksum verified for {file_name}")

                    time.sleep(
                        1
                    )  # fixes issue where file wouldn't be removed after copy
                    if os.path.exists(destination_file_path):
                        os.remove(file_path)
                        print(f"Moved {file_path} to {folder_path}")
                        print(f"REMOVED {file_path}")
                    else:
                        print("ERROR: file not present in dst")

            except Exception as e:
                print(f"Error moving files: {str(e)}")
        else:
            print("no files to move")

    def update_custom_progress_bar(self, copied, total, file_name) -> None:
        bar_length = 30  # Length of the bar (number of segments)
        filled_length = int(
            bar_length * copied // total
        )  # Calculate how many segments are filled
        bar = "|" * filled_length + "." * (bar_length - filled_length)  # Create the bar
        progress_string = f"Copying : {file_name}\n[{bar}]\n {copied / 1048576:.1f} MB of {total / 1048576:.1f} MB"  # Print the progress bar

        return progress_string


# -----------------------------
# Info storage
# -----------------------------


if __name__ == "__main__":
    controller = MainController()
    # dict = controller.match_files_to_folder
    date = controller.global_time()
    file_match = controller.match_files_to_folder(
        "/home/david/Python_Projects/Fake_Folders/",
        "/home/david/Python_Projects/Fake_A20_Bodypack/",
    )
    controller.move_files(file_match)
    # controller.update_custom_progress_bar()

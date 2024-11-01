import os
import logging
import datetime
import wavinfo


class FileInfo:
    def __init__(self) -> None:
        super().__init__()
        self.file_path: str = "src/audio/"
        self.only_wav_list: list = []
        self.file_path_dict = {}

    def create_wav_list(self):
        all_files = os.listdir(self.file_path)

        for file in all_files:
            if file.endswith(".wav"):
                self.only_wav_list.append(file)

    def info_getter(self):
        counter = 1
        self.wav_list = []  # Clear the list at the beginning

        selected_files = self.only_wav_list
        directory = self.file_path

        if selected_files:
            print(selected_files)
        else:
            path_list = self.send_path_list  # List of drive mount points
        for wav_file in selected_files:
            try:
                info = wavinfo.WavInfoReader(os.path.join(directory, wav_file))
            except Exception as e:
                logging.error(f"Failed to read {wav_file}: {e}")
                continue

            # time.sleep(0.01)
            bext_metadata = info.bext
            general_metadata = info.fmt  # Sample rate, bit depth, etc.
            chunk_metadata = info.data

            # Useful options for wav data to pull
            file_name = bext_metadata.originator
            start_tc = bext_metadata.originator_time
            file_time_ref = (
                bext_metadata.time_reference
            )  # Number of samples - referenced after midnight
            sample_rate = general_metadata.sample_rate
            samples = chunk_metadata.frame_count  # Total samples
            bytes = chunk_metadata.byte_count
            # path = os.path.join(self.file_list)

            file_megabytes = int(bytes) / 1048576
            file_run_time_float = samples / sample_rate  # Seconds with decimal places
            file_run_time_int = round(file_run_time_float)
            time_delta = datetime.timedelta(
                seconds=file_run_time_int
            )  # Hours, minutes, seconds

            file_info = {
                "count": counter,
                "file_name": file_name,
                "mb": round(file_megabytes, 2),
                "length": time_delta,
                "start_tc": start_tc,
                "bit depth": general_metadata,
                # "path" : path
            }

            self.timeref = file_time_ref
            self.sample_rate = sample_rate

            file_info_string: str = f"{counter}-{wav_file} : {file_name} : {round(file_megabytes, 2)} MB : {time_delta} : start tc-{start_tc}"
            print(file_info_string)

            counter += 1
            self.wav_list.append(file_info)
            self.file_path_dict[file_info_string] = self.file_path


if __name__ == "__main__":
    file_info = FileInfo()

    file_info.create_wav_list()
    file_info.info_getter()
    print(file_info.file_path_dict)  # dict of file info with the relevant file path

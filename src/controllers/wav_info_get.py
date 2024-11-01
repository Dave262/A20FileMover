from wavinfo import WavInfoReader
import datetime
import os
import re


class WavInfoGet:
    def __init__(self):
        super().__init__()

    def info_getter(self, passed_file) -> dict:
        if passed_file:
            info = WavInfoReader(passed_file)

            file_name = os.path.basename(passed_file)

            # Use getattr with a default value of None
            bext_metadata = getattr(info, "bext", None)
            general_metadata = getattr(info, "fmt", None)
            chunk_metadata = getattr(info, "data", None)
            # bullet_metadata = getattr(info, 'info', None)

            # Extract metadata with default values
            talent_name = getattr(bext_metadata, "originator", None)
            start_tc = getattr(bext_metadata, "originator_time", None)
            file_time_ref = getattr(bext_metadata, "time_reference", None)
            sample_rate = getattr(general_metadata, "sample_rate", None)
            samples = getattr(chunk_metadata, "frame_count", None)
            bytes = getattr(chunk_metadata, "byte_count", None)
            bit_depth = getattr(general_metadata, "bits_per_sample", None)
            orig_date = getattr(bext_metadata, "originator_date", None)
            description = getattr(bext_metadata, "description", None)
            product_id = getattr(bext_metadata, "originator_ref", None)

            # Calculate file size and runtime
            file_megabytes = int(bytes) / 1048576 if bytes else None
            file_run_time_float = (
                samples / sample_rate if samples and sample_rate else None
            )
            file_run_time_int = (
                round(file_run_time_float) if file_run_time_float else None
            )
            time_delta = (
                datetime.timedelta(seconds=file_run_time_int)
                if file_run_time_int
                else None
            )

            # Extract frame rate from description
            match = (
                re.search(r"sSPEED=([\d.]+-ND)", description) if description else None
            )
            frame_rate = match.group(1).replace("0", "") if match else None

            file_info = {
                "file_name": file_name,
                "talent_name": talent_name,
                "size": round(file_megabytes, 2) if file_megabytes else None,
                "length": time_delta,
                "start_tc": start_tc,
                "bit_depth": bit_depth,
                "sample_rate": sample_rate,
                "info": orig_date,
                "frame_rate": frame_rate,
                "product_id": product_id,
                "rec_date": orig_date,
            }

            self.timeref = file_time_ref
            self.sample_rate = sample_rate

        return file_info


if __name__ == "__main__":
    wav_info = WavInfoGet()
    wav_info.info_getter("src/audio/Brent-240930110056.wav")

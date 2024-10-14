import os

import time
# from datetime import date
from datetime import datetime
import re


def global_time():
    time_object = time.localtime()
  
    local_time = time.strftime("%B %d %Y - %H:%M:%S", time_object)
    print(local_time)
    return local_time


# Function that strips all characters form the file string and returns a readable date from the number suffix

def extract_numbers_convert(path):
    for file in os.listdir(path):

        names = re.findall(r'\D+', file.removesuffix(".wav"))
        names_results = "".join(names)
        numbers = re.findall(r'\d+', file)
        numbers_result = "".join(numbers)

        if len(numbers_result) ==12:
            try:
                date_time = datetime.strptime(numbers_result, "%y%m%d%H%M%S")
                formatted_date = date_time.strftime("%d/%m/%Y")
                formatted_time = date_time.strftime("%H:%M:%S")
                print(f"{names_results} Rec Date: {formatted_date}, Start TC: {formatted_time}")
            except ValueError:
                print(f"Unexpected date format in {numbers_result}")        
        else:
            print(f"Unexpected number format in {numbers_result}")





path = "/home/david/Python_Projects/Fake_A20_Bodypack/"

extract_numbers_convert(path)
global_time()



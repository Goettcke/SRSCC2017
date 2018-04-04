#!/usr/bin/env python3

import os
import io
import re
from shutil import copy

input_folder_name = "houses-before-process"
output_folder_name = "houses"

count = len(os.listdir(input_folder_name))
count_len = len(str(count))

house_id_bin_size = 1000

biggest_house_bin = int(count / house_id_bin_size)



def split_by(s, delimiters):
    return list(filter(None, re.split("[{}]+".format("".join(delimiters)), s)))

for i, filename in enumerate(os.listdir(input_folder_name)):
    s = bytes(filename, encoding="utf8", errors="replace").decode("utf8")

    in_path = os.path.join(input_folder_name, filename)

    split = split_by(filename, ["_","."])

    year = int(split[1])
    house_id = int(split[2])

    house_bin = int(house_id / house_id_bin_size)

    house_bin_str = "{low:{fill}{width}}_{high:{fill}{width}}".format(
        low=house_bin*house_id_bin_size,
        high=(house_bin+1)*house_id_bin_size-1,
        fill='0',
        width=count_len,
    )

    print("({curr:{fill}{width}}/{total}) {filename}".format(
        curr=i+1, fill=' ', width=count_len, total=count, filename=filename
    ), end="")

    out_path = os.path.join(output_folder_name, str(year), house_bin_str)

    print("\t-> {}".format(out_path))

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    copy(in_path, out_path)


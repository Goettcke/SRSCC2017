#!/usr/bin/env python3

import os
import io
from shutil import copy

input_folder_name = "output"
output_folder_name = "output2"

count = len(os.listdir(input_folder_name))
count_len = len(str(count))

limit = 100

for i, filename in enumerate(os.listdir(input_folder_name)):

    s = bytes(filename, encoding="utf8", errors="replace").decode("utf8")

    print("({curr:{fill}{width}}/{total}) {filename}".format(
        curr=i+1, fill=' ', width=count_len, total=count, filename=s
    ), end="")

    in_path = os.path.join(input_folder_name, filename)

    with io.open(in_path, 'r', encoding='utf8', errors="ignore") as f:
        for j, raw_line in enumerate(f):
            if j != 2:
                continue

            line = raw_line.split("|")

            if len(line) < 9:
                print("\t (ignoring)", end="")
                break

            amt    = line[8]
            herred = line[7]
            sogn   = line[6]

            print("\t-> {}/{}/{}".format(amt, herred, sogn), end="")

            out_path = os.path.join(output_folder_name, amt, herred, sogn)

            if not os.path.exists(out_path):
                os.makedirs(out_path)

            copy(in_path, out_path)

            break # Don't loop over more lines in the file

    print()

    #if i >= limit:
    #    break

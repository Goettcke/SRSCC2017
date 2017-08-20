# coding=utf-8
import re

import io

#run datasplitter then converter
ff_name = "FT1845_SDU_V2.csv"
target_file_name = "FT1845_2_utf8.csv"


with open(ff_name, 'rb') as source_file:
  with open(target_file_name, 'w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(re.sub(' +',' ',contents.lower().replace("?","")))
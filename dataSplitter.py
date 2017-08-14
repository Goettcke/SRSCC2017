# coding=utf-8
import re

import io


ff_name = "FT1845_SDU.csv"
target_file_name = "FT1845_2_utf8.csv"


ffw = open("FT1845_2_utf8.csv", "w")
counter = 0



with open(ff_name, 'rb') as source_file:
  with open(target_file_name, 'w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(re.sub(' +',' ',contents.decode('utf-16').encode('utf-8').lower().replace("?","")))
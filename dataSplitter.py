# coding=utf-8
import re

def splitter(ff_name,target_file_name):
  with open(ff_name, 'rb') as source_file:
    with open(target_file_name, 'w+b') as dest_file:
      contents = source_file.read()
      dest_file.write(re.sub(' +',' ',contents.lower().replace("?","")))
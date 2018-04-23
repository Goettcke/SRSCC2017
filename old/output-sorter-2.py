#!/usr/bin/env python3

import os
import io
from shutil import copy

input_folder_name = "output"
output_folder_name = "people"

count = len(os.listdir(input_folder_name))
count_len = len(str(count))

respect_limit = False
limit = 100

delimiter = "|"


class Person:
    # match_nr|vaegt|navn|foedested|foedeaar|erhverv|sogn|herred|amt|husstands_familienr|husmatch|koen|civilstand|overhoved|kipnr|loebenr|id|navn_afstand_meta|navne_afstand_leven|meta_fornave|meta_efternavn|meta_foedested
    def __init__(self, **kwargs):
        # Quick hack to avoid writing a lot of lines
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def from_line(raw_line, year):
        line = raw_line.strip()
        parts = line.split(delimiter)

        assert len(parts) > 20

        weight = parts[1] if parts[1] else None
        birth_year = int(parts[4])
        kipnr = parts[14]
        loebenr = parts[15]
        amt = parts[8]

        return Person(
            weight=weight, 
            year=year, 
            birth_year=birth_year, 
            kipnr=kipnr, 
            loebenr=loebenr,
            amt=amt,
        )





class CSVWriter:
    csv_writers = {}

    def __init__(self, filename):
        self.filename = filename

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        # Write the header to the file right-away:
        with open(self.filename, "w") as f:
            print(self.get_header(), file=f)

        self.file = open(self.filename, "a")

    @staticmethod
    def find_by_amt(amt):
        if amt not in CSVWriter.csv_writers:
            path = os.path.join(output_folder_name, "{}.csv".format(amt))
            CSVWriter.csv_writers[amt] = CSVWriter(path)
        return CSVWriter.csv_writers[amt]


    def write(self, person, candidates):
        for cand in candidates:
            print(self.get_line(person, cand), file=self.file)
        print("", file=self.file)


    def get_header(self):
        return "v1;a_ft;a_kipnr;a_lbenr;b_ft;b_kipnr;b_lbenr;score"

    def get_line(self, person, candidate):
        person_fields = ["year", "kipnr", "loebenr"]
        candidate_fields = ["year", "kipnr", "loebenr", "weight"]
        column_length = 1+len(person_fields) + len(candidate_fields)
        column_placeholders = ["{}"] * column_length
        row_fmt = ";".join(column_placeholders)

        column_values = [""]

        for field in person_fields:
            assert hasattr(person, field)
            column_values.append(getattr(person, field))

        for field in candidate_fields:
            assert hasattr(candidate, field)
            column_values.append(getattr(candidate, field))

        return row_fmt.format(*column_values)



for i, filename in enumerate(os.listdir(input_folder_name)):

    s = bytes(filename, encoding="utf8", errors="ignore").decode("utf8")

    if s.startswith(".") or s.startswith("_"):
        continue

    print("({curr:{fill}{width}}/{total}) {filename}".format(
        curr=i+1, fill=' ', width=count_len, total=count, filename=s
    ), end="")

    in_path = os.path.join(input_folder_name, filename)

    with io.open(in_path, 'r', encoding='utf8', errors="ignore") as f:
        lines = f.readlines()

        assert len(lines) > 3

        person = Person.from_line(lines[2], 1845)
        candidates = [Person.from_line(line, 1850) for line in lines[5:] if len(line) > 1]

        CSVWriter.find_by_amt(person.amt).write(person, candidates)

        print("\t-> {}.csv".format(person.amt), end="")


    print()

    if respect_limit and i >= limit:
        break

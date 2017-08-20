# -*- coding: utf-8 -*-
import re

def danishcharacterconverter(inputfile, outputfile) :
    inputfile = open("FT1845_2_utf8.csv")
    outputfile = open("otooe.csv", "w")
    for line in inputfile :
        resline = ""
        for c in line :
            if (ord(c) == 248) or (ord(c) == 216) :
                resline += "oe"
            elif ord(c) == 230 or ord(c) == 198 :
                resline += "ae"
            elif ord(c) == 229 or ord(c) == 197 :
                resline += "aa"

            else :
                resline += c.lower()
        outputfile.write(resline)

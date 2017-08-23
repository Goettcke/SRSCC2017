# -*- coding: utf-8 -*-

import getData
from dataSplitter import *
from dm import damerau_levenshtein_distance
from metaphone import singlemetaphone
from converter import danishcharacterconverter
from Person import Person, foedested_comparison, foedeaar_comparison
from Person import *
print "Susanne, Regina"

p1 = Person(1845)
p2 = Person(1850)
p3 = Person(1850)

f1845 = "FT1845_SDU_V2.csv"
ffw1845 = "f1845.csv"
f1850 = "FT1850_SDU_V2.csv"
finter = "inter.csv"
ffw1850 = "f1850.csv"

""" This is how we convert the files from their format to ours
datasplitter is not needed anymore"""
#danishcharacterconverter(f1845,ffw1845)

#splitter(f1850,finter)
#danishcharacterconverter(finter,ffw1850)



people1845 = getData.get_people(ffw1845, "m",1845)
people1850 = getData.get_people(ffw1850, "m",1850)


candidates = set([])
limit = 17
oldnumberofcandidates = 0
while (len(candidates) < 10 and limit > 0) :
    limit = limit - 1
    print limit
    for i in range (0,len(people1850)):
        if (is_match(people1850[i], people1845[0], limit)):
            print "Success"
            candidates.add(people1850[i])



for person in candidates:
    person_print_information(person)
# Example that shows how the name_comparison function works. So 1. is 100 percent difference. 0 is no difference.

print singlemetaphone("christian thrane marie",1)




p1.meta_fornavn = singlemetaphone("laurids",1)
p1.mlnavn = "g"
p1.meta_efternavn = singlemetaphone("rosendahl",1)


p2.meta_fornavn = singlemetaphone("lautits",1)
p2.mlnavn = "g"
p2.meta_efternavn = singlemetaphone("goettcke",1)

p3.meta_fornavn = "xxxxxxxxxxxxxxxxx"
p3.mlnavn = "xxxxxxxxxxxxxx"
p3.meta_efternavn = "xxxxxxxxxxxxxxxxxxxxxxxxxx"


person_print_information(p1)
person_print_information(p2)

print name_comparison(p1,p2)


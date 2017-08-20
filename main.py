# -*- coding: utf-8 -*-

import getData
from dm import damerau_levenshtein_distance
from metaphone import singlemetaphone

from Person import Person, foedested_comparison, foedeaar_comparison
from Person import *
print "Susanne, Regina"



f = "otooe.csv"
#getData.get_people_1845(f,"m")

#p = getData.people[1]

print singlemetaphone("thrane",1)
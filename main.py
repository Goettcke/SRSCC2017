# -*- coding: utf-8 -*-

import getData
from dm import damerau_levenshtein_distance
from metaphone import singlemetaphone

from Person import Person, foedested_comparison, foedeaar_comparison

print "Susanne, Regina"



#f = "1845smallutf8.csv"
#getData.get_people_to(f,"k")


#p = getData.people[2]

#assert isinstance(p, Person)

#print p.fornavn + " " + p.mlnavn + " " + p.efternavn

p1 = "poul"
p2 = "povl"

dmres = damerau_levenshtein_distance(p1,p2)
print dmres



metaphoneretp1 = singlemetaphone(p1,1)
metaphoneretp2 = singlemetaphone(p2,1)

print metaphoneretp1
print metaphoneretp2


dmres = damerau_levenshtein_distance(metaphoneretp1,metaphoneretp2)







print dmres
#metaphoneret = singlemetaphone(niels laustsen pleiesøn,1)

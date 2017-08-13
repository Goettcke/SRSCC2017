# -*- coding: utf-8 -*-

import getData
from metaphone import singlemetaphone

from Person import Person, foedested_comparison, foedeaar_comparison

print "Susanne, Regina"



f = "1845smallutf8.csv"

getData.get_people_to(f,"K")
p = getData.people[2]
assert isinstance(p, Person)
print str(p.fornavn + " " + p.mlnavn + " " + p.efternavn)

metaphoneret = singlemetaphone(p.fornavn,1)
print metaphoneret

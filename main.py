# -*- coding: utf-8 -*-

import getData
from dm import damerau_levenshtein_distance
from metaphone import singlemetaphone

from Person import Person, foedested_comparison, foedeaar_comparison
from Person import *
print "Susanne, Regina"



f = "otooe.csv"
getData.get_people_1845(f,"m")


print singlemetaphone("thrane",1)
p1 = Person(1845)
p2 = Person(1850)
p3 = Person(1850)

for person in getData.people:
    person.meta_fornavn = singlemetaphone(person.fornavn, 1)
    person.meta_efternavn = singlemetaphone(person.efternavn, 1)

for i in range(2, len(getData.people)):
    if (is_match(getData.people[i], getData.people[1])):
        print "Success"
        print person_print_information(getData.people[1])
        print person_print_information(getData.people[i])


# Example that shows how the name_comparison function works. So 1. is 100 percent difference. 0 is no difference.
p1.fornavn = "hamme"
p1.mlnavn = "gert"
p1.efternavn = "hadoukin"


p2.fornavn = "hammer"
p2.mlnavn = "gerta"
p2.efternavn = "hadouking"

p3.fornavn = "xxxxxxxxxxxxxxxxx"
p3.mlnavn = "xxxxxxxxxxxxxx"
p3.efternavn= "xxxxxxxxxxxxxxxxxxxxxxxxxx"


print name_comparison(p1,p2)
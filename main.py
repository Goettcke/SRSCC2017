# -*- coding: utf-8 -*-


import sys
import getData
import Person
from metaphone import singlemetaphone

from Person import Person, foedested_comparison, foedeaar_comparison

print "Susanne, Regina"
import io




p1 = Person(1845)
p2 = Person(1850)
p3 = Person (1880)

p1.foedested = "Bolbro"
p2.foedested = "Bolbro"
p3.foedested = "Sverige"

p1.foedeaar = 1989
p2.foedeaar = 1990
p3.foedeaar = 1987


people = []

weight =  foedeaar_comparison(p1,p3)

print "Weight is: " + str(weight)




f = "1845smallutf8.csv"

#getData.get_people_to(f,"K")
#p = getData.people[2]
#assert isinstance(p, Person)
#print str(p.navn)
#print p.sogn
#print p.foedeaar
#print str(p.kon == "M")
metaphoneret = singlemetaphone("phedsr jonatan susanne regina marie høistrup hex701",1)



a = "a"
a = a + "b"
print a

print metaphoneret

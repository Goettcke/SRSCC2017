import sys
import getData
import Person
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
getData.get_people_to(f)
p = getData.people[1]
assert isinstance(p, Person)
print str(len(p.test)) + p.navn + str(p.test == "1845")




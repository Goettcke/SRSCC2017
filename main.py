import sys
import getData
from Person import Person
print "Susanne, Regina"


reload(sys)
f = "toy/FT1845.csv"
fo = open(f) # This is simple how to open a file

line = fo.readline().decode('iso-8859-1') # For at kunne haandterer danske tegn
line = fo.readline().decode('iso-8859-1') # For at kunne haandterer danske tegn

lineSplit = line.split("|")

p = Person(1845)
p.herred = lineSplit[4]

print "Person year: " + str(p.year)
print "herred " + p.herred
print line
getData.getPeople(f)



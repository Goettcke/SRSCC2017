import sys
from Person import Person
print "Susanne, Regina"


reload(sys)
fo = open("toy/FT1845.csv") # This is simple how to open a file

line = fo.readline().decode('iso-8859-1') # For at kunne haandterer danske tegn
line = fo.readline().decode('iso-8859-1') # For at kunne haandterer danske tegn

lineSplit = line.split("|")

p = Person(1845)
p.herred = lineSplit[4]

print "Person year: " + str(p.year)
print "herred " + p.herred
print line



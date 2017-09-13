# -*- coding: utf-8 -*-

import getData
import os
from multiprocessing import  Process
from dataSplitter import *
from dm import damerau_levenshtein_distance
from metaphone import singlemetaphone
from converter import danishcharacterconverter
from Person import Person, foedested_comparison, foedeaar_comparison
from Person import *
print "Susanne, Regina"


def lookupperson(peoplelist, limit) :
    ffw1845 = "f1845.csv"
    ffw1850 = "f1850.csv"
    people1845 = getData.get_people(ffw1845, "m", 1845)
    people1850 = getData.get_people(ffw1850, "m", 1850)
    candidates = []

    for number in peoplelist :
        person = people1845[number]
        while (len(candidates) < 10 and limit > 0) :
            limit = limit - 1
            print limit
            for i in range (0,len(people1850)):
                if (is_match(people1850[i], person, limit)):
                    print "Success"
                    if candidates.__contains__(people1850[i]) :
                        print "contained the dude"
                    else :
                        p = people1850[i]
                        p.weight = limit
                        print "weight: " +  str(p.weight)
                        candidates.append(p)

        candidates.sort(key=lambda x : x.weight, reverse=True)
        person_array_iterator(candidates)
        person_array_writer(person,candidates)

if __name__ == '__main__':
    threads = [x for x in range(0,4)]
    print threads
    intervals = []
    counter = 1;
    peopleperthread = 1
    limit = 20
    for i in threads :
        personnumbers = []
        for j in range(counter,counter+peopleperthread) :
            personnumbers.append(j)
            counter = counter + peopleperthread
        intervals.append(personnumbers)
    print intervals
    procs = []
    for number in threads:
        proc = Process(target=lookupperson, args=(intervals[number],limit,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


"""
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

"""
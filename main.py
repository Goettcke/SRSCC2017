import getData
from multiprocessing import  Process
from dataSplitter import *
from dm import damerau_levenshtein_distance
from getData import getHustande
from metaphone import singlemetaphone
from converter import danishcharacterconverter
from Person import Person, foedested_comparison, foedeaar_comparison
from Person import *
print "Susanne, Regina"
#New problem seems to be that we only end up with highest valued candidates.
def lookupperson(peoplelist) :
    ffw1845 = "f1845.csv"
    ffw1850 = "f1850.csv"
    people1845 = getData.get_people(ffw1845, 1845)
    people1850 = getData.get_people(ffw1850, 1850)
    husArr1845 = getHustande(people1845)
    husArr1850 = getHustande(people1850)
    minlimit = 0
    for number in peoplelist :
        candidates = []
        person = people1845[number]
        print "Looking for"
        person_print_information(person)
        for i in range (0,len(people1850)):
            persondistance = person_distance_score(people1850[i], person)
            if (persondistance > minlimit):
                p = people1850[i]
                p.weight = persondistance
                """
                candidates = removelowmatches(minlimit, candidates)
                minlimit = findminlimit(candidates)# must make a minlimit finder here 
                p.weight = persondistance 
                #print "weight: " +  str(p.weight) # Should probably add probability here 
                """
                candidates.append(p)

        if(len(candidates) > 0) :
            print "length of candidates" + str(len(candidates))
            for candidate in candidates:
                if (husdistance(people1845,people1850,person,candidate,husArr1845,husArr1850) == 10) :
                    candidate.husmatch = True
                    candidate.weight += 20
                    person.housestring = housestring(people1845,people1850,person,candidate,husArr1845,husArr1850)

            candidates.sort(key=lambda x: x.weight, reverse=True)
            #person_array_iterator(candidates)
            candidates = takeWeights(candidates)
            person_array_writer(person, candidates)
        else :
            print "Foej for helvede"



def takeWeights (candidateList) :
    resCandidates = []
    weightNR = 0
    for candidate in candidateList :
        currentWeight = candidate.weight
        if (currentWeight <= 0 or weightNR > 4) :
            return resCandidates
        else :
            resCandidates.append(candidate)
        weightNR += 1
    return resCandidates

if __name__ == '__main__':
    threads = [x for x in range(0,1)]
    print threads
    intervals = []
    counter = 1
    peopleperthread = 1000
    limit = 20
    for i in threads :
        personnumbers = []
        for j in range(counter,counter+peopleperthread) :
            personnumbers.append(j)
            counter = counter + 1
        intervals.append(personnumbers)
    print intervals
    procs = []
    for number in threads:
        proc = Process(target=lookupperson, args=(intervals[number],))
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

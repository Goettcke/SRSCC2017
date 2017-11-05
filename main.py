#!/usr/bin/env python2

# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

import os.path
import shutil
import getData
import sys
from multiprocessing import  Process
from dm import damerau_levenshtein_distance
from getData import getHustande
from metaphone import singlemetaphone
#from converter import danishcharacterconverter
#from dataSplitter import *
from Person import *


print "Susanne, Regina"
#New problem seems to be that we only end up with highest valued candidates.



def lookupperson(peoplelist) :
    people1845 = getData.get_people(config.f1845_filename, 1845)
    people1850 = getData.get_people(config.f1850_filename, 1850)

    husArr1845 = getHustande(people1845)
    husArr1850 = getHustande(people1850)

    minlimit = config.person_distance_base_score

    count_no_matches = 0

    for number in peoplelist :
        candidates = []
        person = people1845[number]
        #print "Looking for"
        #person_print_information(person)
        for i in xrange (0,len(people1850)):
            if(person.koen == people1850[i].koen) :
                persondistance = person_distance_score(people1850[i], person)
                if (persondistance > minlimit):
                    p = people1850[i].copy()
                    p.weight = persondistance
                    """
                    candidates = removelowmatches(minlimit, candidates)
                    minlimit = findminlimit(candidates)# must make a minlimit finder here 
                    p.weight = persondistance 
                    #print "weight: " +  str(p.weight) # Should probably add probability here 
                    """
                    candidates.append(p)

        if(len(candidates) > 0) :
           # print "length of candidates" + str(len(candidates))
            for candidate in candidates:
                if (husdistance(people1845,people1850,person,candidate,husArr1845,husArr1850) == config.husstand_match_points) :
                    candidate.husmatch = True
                    candidate.weight += config.husmatch_weight_boost
                    person.housestring = housestring(people1845,people1850,person,candidate,husArr1845,husArr1850)

            candidates.sort(key=lambda x: x.weight, reverse=True)
            #person_array_iterator(candidates)
            candidates = takeWeights(candidates, config.max_candidates_to_include)
            person_array_writer(person, candidates)
        else :
           print "No good candidates found for " + personstring_short(person)
           count_no_matches += 1

    count_has_matches = len(peoplelist) - count_no_matches
    percent = (count_has_matches / float(len(peoplelist))) * 100
    
    print("Status:")
    print("  People considered:      %d" % len(peoplelist))
    print("  People with matches:    %d" % count_has_matches)
    print("  People without matches: %d" % count_no_matches)
    print("  Percentage matched:     %.1f %%" % percent)

    if len(peoplelist) > 0:
        print("Thread %d-%d ended." % (peoplelist[0], peoplelist[-1])) 
    else:
        print("Thread of empty interval ended.")




def takeWeights (candidateList, max_candidates) :
    resCandidates = []
    weightNR = 0
    for candidate in candidateList :
        currentWeight = candidate.weight
        if (currentWeight <= 0 or weightNR > max_candidates) :
            return resCandidates
        else :
            resCandidates.append(candidate)
        weightNR += 1
    return resCandidates

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: ./main.py lowbound highbound threads [config-file]")
        sys.exit(1)

    lowbound = int(sys.argv[1])
    highbound = int(sys.argv[2])
    threads = int(sys.argv[3])

    default_config_filename = "default.ini"

    def c(filename):
        return os.path.join("configs", filename)

    # Initialize the config object.
    # We read a base config file and if given another config file as argument
    # we load that as well which will override some of the values.
    if len(sys.argv) >= 5:
        config.init(c(default_config_filename), c(sys.argv[4]))
    else:
        config.init(c(default_config_filename))


    # Create output folder if it doesn't exist
    # https://stackoverflow.com/a/273227
    try:
        os.makedirs(config.output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    # Copy config file inside output-folder so we know what parameters it was run with.
    if len(config.filenames) == 0:
        print("Error: No config files loaded.")
        sys.exit(1)

    base_conf = config.filenames[0]
    shutil.copyfile(base_conf, os.path.join(config.output_folder, "_default_parameters.ini"))

    if len(config.filenames) >= 2:
        extra_conf = config.filenames[1]
        shutil.copyfile(extra_conf, os.path.join(config.output_folder, "_specific_parameters.ini"))




    # Start threads
    peopleperthread = (highbound-lowbound)/threads
    excess = (highbound-lowbound) - peopleperthread*threads

    intervals = []
    counter = lowbound
    limit = 20
    for i in xrange(threads) :
        personnumbers = []
        if(i != threads - 1) :
            for j in xrange(counter,counter+peopleperthread) :
                personnumbers.append(j)
                counter = counter + 1
            intervals.append(personnumbers)
        else :
            for j in xrange(counter,counter+peopleperthread+excess) :
                personnumbers.append(j)
                counter = counter + 1
            intervals.append(personnumbers)

    print intervals
    procs = []
    for i in xrange(threads):
        proc = Process(target=lookupperson, args=(intervals[i],))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print("All threads ended.")


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

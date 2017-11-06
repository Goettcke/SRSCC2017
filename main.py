#!/usr/bin/env python2

# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

import os.path
import shutil
import sys
import itertools
from multiprocessing import Process

import getData
from Person import *



def lookupperson(peoplelist) :
    if len(peoplelist) == 0:
        print("Thread of empty interval ended.")
        return

    people1845 = getData.get_people(config.f1845_filename, 1845)
    people1850 = getData.get_people(config.f1850_filename, 1850)

    husArr1845 = getData.getHustande(people1845)
    husArr1850 = getData.getHustande(people1850)

    minlimit = config.person_distance_base_score

    count = 0
    count_no_matches = 0
    status_freq = config.status_frequency

    for number in peoplelist :
        candidates = []
        person1845 = people1845[number]
        #print "Looking for"
        #person_print_information(person)

        if count % status_freq == 0:
            print("Status: Currently at " + personstring_short(person1845))

        for person1850 in people1850:
            if(person1845.koen == person1850.koen) :
                persondistance = person_distance_score(person1845, person1850)
                if (persondistance > minlimit):
                    p = person1850.copy()
                    p.weight = persondistance
                    candidates.append(p)

        if(len(candidates) > 0) :
            for candidate in candidates:
                if (husdistance(people1845,people1850,person1845,candidate,husArr1845,husArr1850) == config.husstand_match_points) :
                    candidate.husmatch = True
                    candidate.weight += config.husmatch_weight_boost

            candidates.sort(key=lambda x: x.weight, reverse=True)

            candidates = takeWeights(candidates, config.max_candidates_to_include)

            person_array_writer(person1845, candidates, people1845, people1850, husArr1845, husArr1850, config.output_houses)

        else :
           print "No good candidates found for " + personstring_short(person1845)
           count_no_matches += 1

        count += 1

    count_has_matches = count - count_no_matches
    percent = (count_has_matches / float(count)) * 100
    
    print("Status:")
    print("  People considered:      %d" % count)
    print("  People with matches:    %d" % count_has_matches)
    print("  People without matches: %d" % count_no_matches)
    print("  Percentage matched:     %.1f %%" % percent)

    print("Thread %d-%d ended." % (peoplelist[0], peoplelist[-1])) 




def takeWeights (candidateList, max_candidates) :
    new_cand_list = []

    for cand in candidateList:
        if len(new_cand_list) >= max_candidates:
            break
        if cand.weight < 0:
            break

        new_cand_list.append(cand)

    return new_cand_list


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

    
    # Make it faster to determine name_comparison_method
    config.name_comp_method = hash(config.name_comparison_method)
    config._old = hash("old")
    config._sort_fornavne = hash("sort-fornavne")

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

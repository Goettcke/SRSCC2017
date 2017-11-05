# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

import re

from bisect import bisect_left

from Person import *
from Person import is_overhoved
bad_formatted_people = []
from metaphone import *

# 0 kipnr
# 1  kilde
# 2 sogn
# 3 herred
# 4 amt
# 5 lbnr
# 6 kildehenvisning
# 7 stednavn
# 8 husstnr
# 9 matr_nr_adresse
# 10 antal familier/hus
# 11 navn
# 12 koen
# 13 alder
# 14 civilstkode
# 15 foedested
# 16 erhverv
# 17 kommentarer
# 18 foedeaar

#0 amt
#1 herred
#2 sogn
#3 navn
#4 koen
#5 foedested
#6 foedeaar
#7 Civilstand
#8 Position
#9 Erhverv
#10 husstnr
#11 kipnr
#12 loebenr


"""

Housematch: +20
Foedeaar: equal: +10, 1->5 year difference +8,+6,+4,+2,0 otherwise -100. 
Foedested : on exact match +10
is_overhoved : +3   
name_comparison : all names combined must not differ by more than 30% and first character in first name and last name must be equal. 
Erhverv comparison : +5 if equal else -1 
"""



def get_people(filename, year):
    fo = open(filename)
    counter = 1
    people = []
    pid = 0
    for line in fo:

        if line.startswith("amt|herred"):
            # Ignore the header
            continue

        lineSplit = line.split("|")
        #print line
        #print len(lineSplit)
        if (len(lineSplit)  == 13) :
            p = Person(year)

            p.amt = lineSplit[0]
            p.herred = lineSplit[1]
            p.sogn = lineSplit[2]

            navn_split = lineSplit[3].split(" ")
            p.navnsplit = navn_split

            #assert len(navn_split) >= 2, (navn_split, pid)


            p.fornavn = navn_split[0]

            if (len(navn_split) > 2) :
                for i in xrange(1,len(navn_split)-1,1):
                    try :
                        p.mlnavn = p.mlnavn + navn_split[i] + " "
                    except:
                        print "error with person" + line

                p.mlnavn = p.mlnavn.strip()

            if(len(navn_split) == 2) :
                p.efternavn = navn_split[1]
            else :
                p.efternavn = navn_split[-1]


            p.fornavne_list = navn_split[:-1]
            if config.sort_fornavne:
                p.fornavne_list.sort()
            if config.name_use_metaphone:
                p.fornavne_list = map(metaphone, p.fornavne_list)


            p.koen = lineSplit[4]

            """ 
            matchObj = re.match(r'(.*)sogn(.*)', lineSplit[5])

            if (matchObj != None):
                p.foedested = p.sogn
            else:
                p.foedested = lineSplit[5]
            """
            p.foedested = lineSplit[5]
            p.meta_foedested = metaphone(p.foedested)


            if(is_number(lineSplit[6])) :
                p.foedeaar = int(lineSplit[6])
            else :
                p.foedeaar = 0


            p.civilstand = lineSplit[7]
            p.position = lineSplit[8]
            p.erhverv = lineSplit[9]
            p.husstands_familienr = lineSplit[10]
            p.kipnr = lineSplit[11]
            p.lbnr = lineSplit[12]

            if config.name_use_metaphone:
                p.meta_fornavn   = metaphone(p.fornavn)
                p.meta_mlnavn    = metaphone(p.mlnavn)
                p.meta_efternavn = metaphone(p.efternavn)
            else:
                p.meta_fornavn   = p.fornavn
                p.meta_mlnavn    = p.mlnavn
                p.meta_efternavn = p.efternavn



            p.id = pid # So all people have a unique ID
            pid += 1
            people.append(p)
            p.housestring = None
        counter += 1

    print "Got : " + str(len(people)) + " people from dataset"
    return people

def getHustande(peopleArr) :
    currentHouse = peopleArr[0].husstands_familienr
    husArr = []
    currentIndex = 0
    people = []
    for i in xrange (len(peopleArr)) :
        if (peopleArr[i].husstands_familienr != currentHouse) :
            husArr.append(people)
            currentHouse = peopleArr[i].husstands_familienr
            people = []
            currentIndex += 1
        else :
            people.append(peopleArr[i].id)

        peopleArr[i].hustandsindex = currentIndex

    # print str(husArr[0]) + "getting person"
    #p = getPerson(peopleArr, husArr[1337][0])
    #p2 = peopleArr[1337]
    #print len(peopleArr)
    #print p.fornavn +" " +  p.mlnavn  + " " + p.efternavn
    #print p2.fornavn +" " +  p2.mlnavn  + " " + p2.efternavn
    #print " got person"
    #print alternategetPerson(peopleArr,p.id)
    return husArr


def is_number(foedeaar):
    try:
        int(foedeaar)
        return True
    except:
        return False

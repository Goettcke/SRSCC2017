import re

from bisect import bisect_left

from Person import *
from Person import is_overhoved
bad_formatted_people = []
from metaphone import singlemetaphone
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


def get_people(filename, koen,  year):
    fo = open(filename)
    counter = 1
    people = []
    pid = 0
    for line in fo:
        lineSplit = line.split("|")
        #print line
        #print len(lineSplit)
        if (len(lineSplit)  == 13 and koen == lineSplit[4]) :
            p = Person(year)
            p.amt = lineSplit[0]
            p.herred = lineSplit[1]
            p.sogn = lineSplit[2]
            navn_split = lineSplit[3].split(" ")
            p.fornavn = navn_split[0]
            p.navnsplit = navn_split

            if (len(navn_split) > 2) :
                for i in range(1,len(navn_split)-1,1):
                    try :
                        p.mlnavn = p.mlnavn + navn_split[i][0]
                    except:
                        print "error with person" + line

            if(len(navn_split) == 2) :
                p.efternavn = navn_split[1]
            else :
                p.efternavn = navn_split[-1]


            p.koen = lineSplit[4]

            matchObj = re.match(r'(.*)sogn(.*)', p.foedested)

            if (matchObj == None):
                p.foedested = p.sogn
            else:
                p.foedested = lineSplit[5]

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
            p.meta_fornavn = singlemetaphone(p.fornavn,1)
            p.meta_efternavn = singlemetaphone(p.efternavn,1)
            p.id = pid
            pid += 1
            people.append(p)
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
        else :
            people.append(peopleArr[i].id)

        peopleArr[i].hustandsindex = currentIndex
        currentIndex += 1

    print str(husArr[0]) + "getting person"
    p = getPerson(peopleArr, husArr[1337][0])
    p2 = peopleArr[1337]
    print len(peopleArr)
    print p.fornavn +" " +  p.mlnavn  + " " + p.efternavn
    print p2.fornavn +" " +  p2.mlnavn  + " " + p2.efternavn
    print " got person"
    print alternategetPerson(peopleArr,p.id)
    return husArr


def is_number(foedeaar):
    try:
        int(foedeaar)
        return True
    except:
        return False
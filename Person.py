# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

from dm import *
import re
import os, errno
import os.path
import copy
import itertools

class Person:

    testcounter = 0

    def __init__(self, year):
        assert isinstance(year, int)
        self.year = year # tilfoej en ekstra parameter, der kigger paa om aaret giver mening i forhold til alderen.
        self.kipNr = str()
        self.kilde = str()
        self.sogn = str() # dmld
        self.herred = str() # dmld
        self.amt = str() # dmld
        self.lbnr = int()
        self.kildehenvisning = str()
        self.stednavn = str()
        self.husstands_familienr = int()
        self.hustandsindex = int() # index i hustandsarray
        self.matr_nr_adresse = None
        self.fornavn = str() #dmld metaphone
        self.mlnavn = str() # dm uden metaphone
        self.efternavn = str() #dmld metaphone
        self.meta_fornavn = str()  # dmld metaphone
        self.meta_mlnavn = str()  # dmld metaphone
        self.meta_efternavn = str()  # dmld metaphone
        #self.kon = bool()
        self.koen = str() # "k" or "m"
        self.alder_tal = int() # direkte maalign eller
        self.foedeaar = int() # direkte maalign eller
        self.civilstand = int()
        self.civilstand_source = str()
        self.foedested = "" #numerisk eller dmld
        self.valid = True
        self.matches = dict()
        self.erhverv = str()
        self.id = -1
        self.group = -1
        self.test = str()
        self.position = str()
        self.weight = int() # The weight, that the person was found using.
        self.navnsplit = []
        self.husmatch = bool()
        self.housestring = str()

    def copy(self):
        return copy.deepcopy(self)


def name_comparison(p1, p2) :
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)

    if config.name_comparison_method == "old":
        if(len(p1.meta_efternavn) > 0 and len(p2.meta_efternavn) > 0 and \
           len(p1.meta_fornavn) > 0 and len(p2.meta_fornavn) > 0 ):

            # Focus on the first letters of fornavn and efternavn first. If they don't match, don't bother.
            if(p1.meta_fornavn[0] == p2.meta_fornavn[0] and p1.meta_efternavn[0] == p2.meta_efternavn[0]) :
                # Fornavn
                fn_percentdifference = percent_levenshtein_helper(p1.meta_fornavn, p2.meta_fornavn)

                # Higher weight on fornavn
                if fn_percentdifference >= config.fornavn_max_percent_difference:
                    return 2

                # Mellemnavn
                ml_percentdifference = percent_levenshtein_helper(p1.meta_mlnavn, p2.meta_mlnavn)

                # Efternavn
                en_percentdifference = percent_levenshtein_helper(p1.meta_efternavn, p2.meta_efternavn)

                result = fn_percentdifference + ml_percentdifference + en_percentdifference

                return result / 3
    elif config.name_comparison_method == "sort-fornavne":
        count = 0
        percent_diff = 0
        
        for (fornavn1, fornavn2) in itertools.izip_longest(p1.fornavne_list, p2.fornavne_list, fillvalue=""):
            percent_diff += percent_levenshtein_helper(fornavn1, fornavn2)
            if fornavn1 != "" and fornavn2 != "":
                # Only count this fornavn comparison if one of the names actually exists
                count += 1

        percent_diff += percent_levenshtein_helper(p1.meta_efternavn, p2.meta_efternavn)
        count += 1

        return percent_diff / count


    return 2 # 100% mismatch

#Legacy code, just if binarysearch is needed in some future development
def getPerson(peoplearr , pid) :
    left = 0
    right = len(peoplearr)
    while left < right:
        mid = (left + right) // 2
        if pid > peoplearr[mid].id:
            left = mid + 1
        else:
            right = mid
    if left != len(peoplearr) and peoplearr[left].id == pid:
        return peoplearr[left]
    else:
        raise ValueError("{!r} is not in sequence".format(pid))


def alternategetPerson(peoplearr, pid) :
    print str(peoplearr[pid].id) + " " + str(pid)

def husdistance(peoplearr1,peoplearr2,p1,p2,husarr1,husarr2) :
    hus1size = len(husarr1[p1.hustandsindex])
    hus2size = len(husarr2[p2.hustandsindex])
    #print "hussizes " + str(hus1size) + " _ " +  str(hus2size)
    totalhusdistance = 0
    peopleinhouse1 = []
    peopleinhouse2 = []

    if(hus1size == 0 or hus2size == 0) :
        housedivisor = max(hus1size, hus2size) ## Could potentially give division by 0 if both zero but not in 1845 1850.
    else :
        housedivisor = min(hus1size,hus2size)

    for i in xrange(hus1size) :
        peopleinhouse1.append(peoplearr1[husarr1[p1.hustandsindex][i]])
    for i in xrange(hus2size) :
        peopleinhouse2.append(peoplearr2[husarr2[p2.hustandsindex][i]])

    for person in peopleinhouse1 :
        # print "Muuh "   + person.fornavn # check it makes the correct comparisons
        for person2 in peopleinhouse2 :
         #   print "Maaaeeh " + person2.fornavn # Just to check that It actually enters the loop
            totalhusdistance += person_distance_score(person,person2)
    if(hus1size != 0) :
        if((totalhusdistance / housedivisor) > config.husstand_min_weight) :
            return config.husstand_match_points
        else :
            return config.husstand_mismatch_points

def housestring(peoplearr1,peoplearr2,p1,p2,husarr1,husarr2) :
    output = "   Start of New HOUSE  \n  "
    hus1size = len(husarr1[p1.hustandsindex])
    hus2size = len(husarr2[p2.hustandsindex])
    peopleinhouse1 = []
    peopleinhouse2 = []

    for i in xrange(hus1size) :
        peopleinhouse1.append(peoplearr1[husarr1[p1.hustandsindex][i]])

    for i in xrange(hus2size) :
        peopleinhouse2.append(peoplearr2[husarr2[p2.hustandsindex][i]])

    output += " ------- Start house1 --------- \n"
    for person in peopleinhouse1 :
        output += personstring(person)

    output += " ------- End of house1 --------- \n"


    output += " ------- Start house2 --------- \n"

    for person2 in peopleinhouse2 :
        output += personstring(person2)
    output += " ------- End of house2 --------- \n"
    output += "   End of New HOUSE  \n  "
    return output



    #Saa koerer vi dobbelt metaphonoe
# TODO Make more specific assignment of values to inexact cases.
def foedeaar_comparison(person1,person2) : # Enten 10 eller 0 Grov sortering
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)

    age_diff = abs(person1.foedeaar - person2.foedeaar)

    if age_diff == 0:
        return config.foedeaar_match_points
    elif age_diff <= config.foedeaar_max_difference:
        # Take the age difference between 0 and 2
        # and map into 10 and 0 (in that order, so an age diff of 0 gives 10 points).
        interpolate_score = interpolate(
            age_diff,
            0, config.foedeaar_max_difference,
            config.foedeaar_match_points, 0
        )
        return interpolate_score
    else:
        return config.foedeaar_mismatch_points


# TODO apply double metaphone to inexact matching foedested
def foedested_comparison(person1, person2) : # Maks 5 else 0
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)
    #print "Foedested_comparison"
    matchObj = re.match(r'(.*)sogn(.*)',person1.foedested)
    matchObj2 = re.match(r'(.*)sogn(.*)',person2.foedested)

    if (matchObj != None and matchObj2 != None): # Case both is some version of "heri sognet"
        if(person1.sogn == person2.sogn) :
          #  print "Both is something herisognet, so comparing sogn"
            return config.foedested_sogn_match_points
        elif(person1.herred == person2.herred) :
            return config.foedested_herred_match_points

    elif(matchObj != None and matchObj2 == None) :
       # print "person1 contains herisognet"
        person1places = [person1.amt,person1.herred,person1.sogn]
     #   print person1places
        for p1place in person1places :
            if (p1place == person2.sogn):
               # print p1place + " matches " + person2.sogn
                return config.foedested_sogn_match_points

    elif (matchObj == None and matchObj2 != None):
       # print "person2 contains herisognet"
        person2places = [person2.amt, person2.herred, person2.sogn]
        for p2place in person2places:
            if (p2place == person1.sogn):
               # print p2place + " matches " + person1.sogn
                return config.foedested_sogn_match_points
    else :
        if config.foedested_use_metaphone:
            if person1.meta_foedested == person2.meta_foedested:
                return config.foedested_exact_match_points
        else:
            if(person1.foedested == person2.foedested) :
               # print "none of the foedesteder contained sogn and matched exact"
                return config.foedested_exact_match_points
   # print "none of the foedesteder contained sogn and didn't match so returning 0"

    return config.foedested_mismatch_points


def is_overhoved(person) :
    assert isinstance(person, Person)
    if(person.position == "husstandsoverhoved") :
        return True
    else :
        return False

def overhoved_comparison(p1,p2) :
    if(is_overhoved(p1) == is_overhoved(p2)) :
        return config.overhoved_match_points
    else :
        return config.overhoved_mismatch_points

def erhverv_comparison(p1,p2):
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)
    if(p1.erhverv == p2.erhverv):
        return config.erhverv_match_points
    else :
        return config.erhverv_mismatch_points

def person_distance_score(p1, p2):
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)

    result = config.person_distance_base_score # 0 by default

    name_comparison_diff = name_comparison(p1, p2)

    if (name_comparison_diff <= config.name_comparison_max_percent_difference) : 
        result += foedeaar_comparison(p1,p2) 
        result += foedested_comparison(p1,p2) 
        result += overhoved_comparison(p1,p2) 
        result += erhverv_comparison(p1,p2)

        if config.use_name_comparison_boost:
            # The name difference will be between 0.0 and config.name_comparison_max_percentage_difference,
            # commonly between 0.0 and 0.3. 
            # First interpolate this into a 0.0-1.0 scale.
            interpolated_diff = interpolate(
                name_comparison_diff, 
                0.0, config.name_comparison_max_percent_difference, 
                0.0, 1.0
            )
            # If the diff is very small, e.g. close to 0, we should give full points.
            # If the diff is very big, e.g. close to 1, we should give no points.
            # So we take 1 - diff to get this effect.
            # Finally we scale with a factor so it can be between 0 to 100 or 0 to 10 if we want.
            result += int((1 - interpolated_diff)*config.name_comparison_boost_scale)

        p1.name_comparison_diff = name_comparison_diff

    return result # Which in this case is equal to 0


def is_match(p1,p2,limit):
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)
    if(person_distance_score(p1, p2) > limit) : # So just use the distance directlyt
        return True
    else :
        return False

# removes matches in the list that are lower than a certain limit. 
def removelowmatches(limit,inputlist) : 
    output = [] 
    for person in inputlist : 
        if person.weight > limit : 
            output.append(person)
    print "removed: " + str(len(inputlist)-len(output)) + " candidates" 
    return output

def findminlimit(inputlist) : 
    limit = 30 #This should be a universal max weights
    for person in inputlist : 
        if(person.weight < limit) : 
            limit = person.weight
    return limit

def interpolate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def person_print_information(p1):
    assert isinstance(p1, Person)

    print "navn: " + str(p1.fornavn) + " " + str(p1.mlnavn) + " " + str(p1.efternavn)

    print "foedested: " + str(p1.foedested)

    print "foedeaar: " + str(p1.foedeaar)

    print "is overhoved: " + str(is_overhoved(p1))

    print "erhverv: " + str(p1.erhverv)

    print "weight: " + str(p1.weight)

    print "sogn: " + str(p1.sogn)
    print "amt: " + str(p1.amt)
    print "husstandsfamilienr: " + str(p1.husstands_familienr)
    print "meta_fornavn: " + str(p1.meta_fornavn)
    print "meta_efternavn: " + "'" + str(p1.meta_efternavn)+ "'"
    print "civilstand: " + str(p1.civilstand)
    print "navnsplit: " + str(p1.navnsplit)
    print "\n"

def person_array_iterator(listi) :
    for p in listi :
        person_print_information(p) # p is a person


def personstring (person) :
    output = "navn: " + str(person.fornavn) + " " + str(person.mlnavn) + " " + str(person.efternavn) + "\n"
    output += "foedested: " + str(person.foedested) + "\n"
    output += "foedeaar: " + str(person.foedeaar) + "\n"
    output += "is overhoved: " + str(is_overhoved(person)) + "\n"
    output += "erhverv: " + str(person.erhverv) + "\n"
    output += "sogn: " + str(person.sogn) + "\n"
    output += "amt: " + str(person.amt) + "\n"
    output += "husstandsfamilienr: " + str(person.husstands_familienr) + "\n"
    output += "meta_fornavn: " + "'" + str(person.meta_fornavn) +"'" + "\n"
    output += "meta_mlnavn: " + "'" + str(person.meta_mlnavn) +"'" + "\n"
    output += "meta_efternavn: " + "'" + str(person.meta_efternavn) + "'"  + "\n"
    output += "koen: " + str(person.koen) + "\n"
    output += "civilstand: " + str(person.civilstand) + "\n"
    output += "navnsplit: " + str(person.navnsplit) + "\n"
    output += "fornavne_list: " + str(person.fornavne_list) + "\n"
    output += "meta_foedested: " + "'" + str(person.meta_foedested) +"'" + "\n"
    try:
        output += "name_comparison_diff: " + str(person.name_comparison_diff) + "\n"
    except AttributeError:
        pass
    output += "weight: " + str(person.weight) + "\n\n"
    return output

def personstring_short (person) :
    return str(person.fornavn) + " " + str(person.mlnavn) + " " + str(person.efternavn) + " (" + str(person.id) + ")"


def person_array_writer(person, listi) : # person is the person we're looking for
    output = "Person we're looking for: \n --------------------\n"
    output += personstring(person)
    output += "--------------------\n \n---- Matches ----" + "\n"

    for p in listi :
        output += personstring(p) # p is a person

    mlnavn_list = person.mlnavn.split(" ")
    if len(mlnavn_list) == 1 and mlnavn_list[0] == "":
        mlnavn_list = []

    file_base_name = "_".join([
        person.fornavn] + mlnavn_list + [person.efternavn, 
        str(person.foedeaar), str(person.husstands_familienr), str(person.id)
    ])

    file_house_name = file_base_name + "_house"


    f = open(os.path.join(config.output_folder, file_base_name) + ".txt", 'w')
    f.write(output)
    f.close()

    if(person.housestring != None) :
        f = open(os.path.join(config.output_folder, file_house_name) + ".txt", 'w')
        f.write(person.housestring)



























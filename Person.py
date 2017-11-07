# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

from dm import *
from metaphone import *
import re
import sys
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
        self.position = str()
        self.weight = int() # The weight, that the person was found using.
        self.navnsplit = []
        self.husmatch = bool()
        self.name_comparison_diff = float("inf")
        self.name_comparison_diff_leven = float("inf")

    def copy(self):
        return copy.deepcopy(self)


def name_comparison(p1, p2) :
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)

    if not config.use_legacy_name_comparison:
        count = 0
        score = 0

        fornavne_score = config.name_comparison_fornavne_score
        efternavn_score = config.name_comparison_efternavn_score

        for (fornavn1, fornavn2) in itertools.izip_longest(p1.meta_fornavne_list, p2.meta_fornavne_list, fillvalue=""):
            if compare_metaphone(fornavn1, fornavn2):
                score += fornavne_score
            count += fornavne_score

        if compare_metaphone(p1.meta_efternavn, p2.meta_efternavn):
            score += efternavn_score
        count += efternavn_score

        return 1.0 - score / float(count)



    else:
        if(len(p1.meta_efternavn) > 0 and len(p2.meta_efternavn) > 0 and \
           len(p1.meta_fornavn) > 0 and len(p2.meta_fornavn) > 0 ):

            # Focus on the first letters of fornavn and efternavn first. If they don't match, don't bother.
            if(p1.meta_fornavn[0] == p2.meta_fornavn[0] and p1.meta_efternavn[0] == p2.meta_efternavn[0]) :
                # Fornavn
                fn_percentdifference = percent_levenshtein_helper(p1.meta_fornavn, p2.meta_fornavn)

                # Higher weight on fornavn
                if fn_percentdifference >= config.legacy_fornavn_max_percent_difference:
                    return 2

                # Mellemnavn
                ml_percentdifference = percent_levenshtein_helper(p1.meta_mlnavn, p2.meta_mlnavn)

                # Efternavn
                en_percentdifference = percent_levenshtein_helper(p1.meta_efternavn, p2.meta_efternavn)

                result = fn_percentdifference + ml_percentdifference + en_percentdifference

                return result / 3
        return 2 # 100% mismatch



def husdistance(peoplearr1,peoplearr2,p1,p2,husarr1,husarr2) :
    hus1 = husarr1[p1.husstands_familienr]
    hus2 = husarr2[p2.husstands_familienr]

    hus1size = len(hus1)
    hus2size = len(hus2)

    #print "hussizes " + str(hus1size) + " _ " +  str(hus2size)
    totalhusdistance = 0
    peopleinhouse1 = []
    peopleinhouse2 = []

    if hus1size == 0 and hus2size == 0:
        housedivisor = 1
    elif hus1size == 0 or hus2size == 0:
        housedivisor = max(hus1size, hus2size)
    else:
        housedivisor = min(hus1size,hus2size)

    for i in xrange(hus1size) :
        peopleinhouse1.append(peoplearr1[hus1[i]])

    for i in xrange(hus2size) :
        peopleinhouse2.append(peoplearr2[hus2[i]])

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


her_i_sognet_regex = re.compile(r'(.*)sognet(.*)')

def foedested_comparison(person1, person2) : 
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)

    matchObj1 = re.match(her_i_sognet_regex, person1.foedested)
    matchObj2 = re.match(her_i_sognet_regex, person2.foedested)

    p1_wrote_her_i_sognet = matchObj1 != None
    p2_wrote_her_i_sognet = matchObj2 != None

    if (p1_wrote_her_i_sognet and p2_wrote_her_i_sognet): # Case both is some version of "heri sognet"
        if(person1.sogn == person2.sogn) :
            return config.foedested_sogn_match_points
        elif(person1.herred == person2.herred) :
            return config.foedested_herred_match_points
        elif(person1.amt == person2.amt) :
            return config.foedested_amt_match_points

    elif(p1_wrote_her_i_sognet and not p2_wrote_her_i_sognet) :
        person1places = [person1.amt, person1.herred, person1.sogn]

        for p1place in person1places :
            if (p1place == person2.sogn):
                return config.foedested_sogn_match_points

    elif (not p1_wrote_her_i_sognet and p2_wrote_her_i_sognet):
        person2places = [person2.amt, person2.herred, person2.sogn]

        for p2place in person2places:
            if (p2place == person1.sogn):
                return config.foedested_sogn_match_points
    else :
        if config.foedested_use_metaphone:
            if compare_metaphone(person1.meta_foedested, person2.meta_foedested):
                return config.foedested_exact_match_points
        else:
            if(person1.foedested == person2.foedested) :
                return config.foedested_exact_match_points

    return config.foedested_mismatch_points


def is_overhoved(person, yes_result = True, no_result = False) :
    assert isinstance(person, Person)
    if(person.position == "husstandsoverhoved") :
        return yes_result
    else :
        return no_result

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

    p2.name_comparison_diff = name_comparison_diff
    
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
            result += int((1 - interpolated_diff)*config.name_comparison_boost_points)

        if config.use_name_comparison_leven_boost:
            percent_diff = 0.0
            count = 0

            for (fornavn1, fornavn2) in itertools.izip_longest(p1.fornavne_list, p2.fornavne_list, fillvalue=""):
                percent_diff += percent_levenshtein(fornavn1, fornavn2)
                count += 1

            percent_diff += percent_levenshtein(p1.efternavn, p2.efternavn)
            count += 1

            avg_percent_diff = percent_diff / count

            p2.name_comparison_diff_leven = avg_percent_diff

            # If the average percentage difference is high (towards 1), we give a penalty.
            # If the average percentage difference is low (towards 0), we give a bouns.
            interpolated_score = interpolate(
                avg_percent_diff, 
                0.0, 1.0,
                config.name_comparison_leven_boost_points/2, -config.name_comparison_leven_boost_points/2
            )

            result += int(round(interpolated_score))

    return result # Which in this case is equal to 0



def interpolate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)



longest_attr = 0

def personstring (person, indent = "", part_of_house = False) :
    attributes = []
    pad = 3

    def l(attr = "", s = ""):
        global longest_attr
        longest_attr = max(longest_attr, len(attr))
        attributes.append((attr, str(s)))

    l("navn", personstring_short(person, False))
    l("foedested", person.foedested)
    l("foedeaar", person.foedeaar)
    l("erhverv", person.erhverv)
    l()
    l("sogn", person.sogn)
    l("herred", person.herred)
    l("amt", person.amt)
    l("husstandsfamilienr", person.husstands_familienr)
    l()
    l("koen", person.koen)
    l("civilstand", person.civilstand)
    l("er overhoved", is_overhoved(person, "ja", "nej"))
    l()
    l("kipnr", person.kipnr)
    l("loebenr", person.lbnr)
    l()
    l("id", person.id)
    l("meta_fornavn", person.meta_fornavn)
    l("meta_mlnavn", person.meta_mlnavn)
    l("meta_efternavn", person.meta_efternavn)
    l("meta_foedested", person.meta_foedested)
    l("navnsplit", person.navnsplit)
    l("fornavne", person.fornavne_list)
    l("meta_fornavne", person.meta_fornavne_list)


    if person.year != 1845:
        try:
            l("name_comparison_diff",  person.name_comparison_diff)
        except AttributeError:
            pass

        try:
            l("husmatch",  person.husmatch)
        except AttributeError:
            pass

    if person.year != 1845 and not part_of_house:
        l("weight", person.weight)

    output = ""
    for attr, s in attributes:
        if attr != "":
            output += indent + (attr + ":").ljust(longest_attr+pad, " ") + s
        output += "\n"


    return output



def personstring_short(person, with_id = True) :
    res = " ".join(person.navnsplit)
    if with_id:
        res += " (" + str(person.id) + ")"
    return res



def housestring(person, people_arr, hus_arr):
    hus = hus_arr[person.husstands_familienr]

    hus_size = len(hus)

    people_in_house = []

    for i in xrange(hus_size) :
        people_in_house.append(people_arr[hus[i]])

    output = "HOUSE:\n"
    for person in people_in_house:
        output += "    ---------------------------------------------\n"
        output += personstring(person, "    ", True)
        output += "    ---------------------------------------------\n\n"

    return output


def get_person_filepath(person):
    file_base_name = "_".join(
        person.navnsplit + 
        [str(person.foedeaar), str(person.husstands_familienr), str(person.id)]
    )

    path = os.path.join(config.output_folder, file_base_name)

    return path

def person_array_writer(person, candidates, people1845, people1850, husArr1845, husArr1850, output_houses = True) : # person is the person we're looking for
    output = ""

    output += "================================================\n"
    output += "Person we're looking for:\n"
    output += personstring(person)
    if output_houses:
        output += "\n"
        output += housestring(person, people1845, husArr1845)
    output += "================================================\n"
    output += "\n"


    for i, p in enumerate(candidates):
        output += "--------------- Match %d start -------------------------\n" % (i+1)
        output += personstring(p) # p is a person
        if output_houses:
            output += "\n"
            output += housestring(p, people1850, husArr1850)
        output += "--------------- Match %d end   -------------------------\n" % (i+1)
        output += "\n"



    path = get_person_filepath(person)

    if output_houses:
        f = open(path + "_house.txt", 'w')
    else:
        f = open(path + ".txt", 'w')
    f.write(output)
    f.close()


def person_array_writer_csv(person, candidates, delimiter = "|"):
    atttributes = [
        "match_nr", "vaegt", "navn", "foedested", "foedeaar", 
        "erhverv", "sogn", "herred", "amt", "husstands_familienr", "husmatch",
        "koen", "civilstand", "overhoved", 
        "kipnr", "loebenr", "id",
        "navn_afstand_meta", "navne_afstand_leven",
        "meta_fornave", "meta_efternavn", "meta_foedested",
    ]

    def line(p, match_nr):
        w = p.weight if p.weight > 0 else ""
        name_diff = "%.1f %%" % (p.name_comparison_diff * 100)
        name_diff_leven = "%.1f %%" % (p.name_comparison_diff_leven * 100)
        fornavne = " ".join(str(x) for x in p.meta_fornavne_list)
        return [
            match_nr, w, personstring_short(p, False), p.foedested, p.foedeaar,
            p.erhverv, p.sogn, p.herred, p.amt, p.husstands_familienr, p.husmatch,
            p.koen, p.civilstand, is_overhoved(p),
            p.kipnr, p.lbnr, p.id,
            name_diff, name_diff_leven,
            fornavne, p.meta_efternavn, p.meta_foedested,
        ]

    path = get_person_filepath(person)

    f = open(path + "_simple.csv", 'w')

    f.write("sep=" + delimiter + "\n")

    f.write(delimiter.join(["emne", ""] + atttributes[2:]) + "\n")

    atttribute_values = line(person, "")
    f.write(delimiter.join(str(a) for a in atttribute_values) + "\n")

    f.write("\n")

    f.write(delimiter.join(atttributes) + "\n")

    for i, cand in enumerate(candidates):
        atttribute_values = line(cand, i+1)
        f.write(delimiter.join(str(a) for a in atttribute_values) + "\n")

    f.close()














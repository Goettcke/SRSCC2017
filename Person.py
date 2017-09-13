
from dm import damerau_levenshtein_distance
class Person:
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
        self.matr_nr_adresse = None
        self.fornavn = str() #dmld metaphone
        self.mlnavn = str() # dm uden metaphone
        self.efternavn = str() #dmld metaphone
        self.meta_fornavn = str()  # dmld metaphone
        self.meta_efternavn = str()  # dmld metaphone
        self.kon = bool()
        self.alder_tal = int() # direkte maalign eller
        self.foedeaar = int() # direkte maalign eller
        self.civilstand = int()
        self.civilstand_source = str()
        self.foedested = "" #numerisk eller dmld
        self.valid = True
        self.matches = dict()
        self.erhverv = str()
        self.nregteskab = int()
        self.id = -1
        self.group = -1
        self.home_index = -1
        self.test = str()
        self.position = str()
        self.weight = int() # The weight, that the person was found using.
        pass


# TODO Apply Double Metaphone to inexact names.
def name_comparison(p1, p2) :
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)
    fn_percentdifference = damerau_levenshtein_distance(p1.meta_fornavn, p2.meta_fornavn) / float(percent_denominator(p1.meta_fornavn,p2.meta_fornavn))
    ml_percentdifference = damerau_levenshtein_distance(p1.mlnavn, p2.mlnavn) / float(percent_denominator(p1.mlnavn,p2.mlnavn))
    en_percentdifference = damerau_levenshtein_distance(p1.meta_efternavn, p2.meta_efternavn) / float(percent_denominator(p1.meta_efternavn,p2.meta_efternavn))
    result = fn_percentdifference + ml_percentdifference + en_percentdifference
    return result/3

def percent_denominator(navn1,navn2):
    denominator = float(max(len(navn1), len(navn2)))
    if (denominator != 0):
        return denominator
    else :
        return 1 # To ensure we're not deviding by 0


    #Saa koerer vi dobbelt metaphonoe
# TODO Make more specific assignment of values to inexact cases.
def foedeaar_comparison(person1,person2) : # Enten 10 eller 0 Grov sortering
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)

    if (abs(person1.foedeaar - person2.foedeaar) < 3) :
        return 10 #man kan udvide med en variabel, der aendres med distancen imellem de to aldre
    else :
        return 3 - abs(person1.foedeaar - person2.foedeaar)



# TODO apply double metaphone to inexact matching foedested
def foedested_comparison(person1, person2) : # Maks 5 else 0
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)
    if person1.foedested == person2.foedested :
        return 10
    else :
        return 0

def is_overhoved(person) :
    assert isinstance(person, Person)
    if(person.position == "husstandsoverhoved") :
        return True
    else :
        return False
def overhoved_comparison(p1,p2) :
    if(is_overhoved(p1) == is_overhoved(p2)) :
        return 3
    else :
        return 0

def person_distance_score(p1, p2):
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)
    result = 0
    if (name_comparison(p1, p2) <= 0.1) : # Smaller than 33percent difference
        result = foedeaar_comparison(p1,p2) + foedested_comparison(p1,p2) + overhoved_comparison(p1,p2) + erhverv_comparison(p1,p2)

    return result # Which in this case is equal to 0

def erhverv_comparison(p1,p2):
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)
    if(p1.erhverv == p2.erhverv):
        return 5
    else :
        return -1


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
    limit = 30 #This should be a universal max weight
    for person in inputlist : 
        if(person.weight < limit) : 
            limit = person.weight
    return person.weight

def person_print_information(p1):
    assert isinstance(p1, Person)

    print "navn: " + str(p1.fornavn) + " " + str(p1.mlnavn) + " " + str(p1.efternavn)

    print "foedested: " + str(p1.foedested)

    print "foedeaar: " + str(p1.foedeaar)

    print "is overhoved: " + str(is_overhoved(p1))

    print "erhverv: " + str(p1.erhverv)

    print "weight: " + str(p1.weight)

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
    output += "weight: " + str(person.weight) + "\n\n"
    return output


def person_array_writer(person, listi) : # person is the person we're looking for
    output = "Person we're looking for: \n --------------------\n"
    output += personstring(person)
    output += "--------------------\n \n---- Matches ----" + "\n"

    for p in listi :
        output += personstring(p) # p is a person

    f = open(str("output/" + person.fornavn + "_" + person.mlnavn +  "_"  + person.efternavn + str(person.foedeaar) + str(person.weight)) + ".txt", 'w')
    f.write(output)































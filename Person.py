from idlelib import TreeWidget

from dm import damerau_levenshtein_distance
class Person:
    def __init__(self, year):
        assert isinstance(year, int)
        self.year = year # tilfoej en ekstra parameter, der kigger paa om aaret giver mening i forhold til alderen.
        self.kipNr = unicode()
        self.kilde = unicode()
        self.sogn = unicode() # dmld
        self.herred = unicode() # dmld
        self.amt = unicode() # dmld
        self.lbnr = int()
        self.kildehenvisning = unicode()
        self.stednavn = unicode()
        self.husstands_familienr = int()
        self.matr_nr_adresse = None
        self.fornavn = unicode() #dmld metaphone
        self.mlnavn = unicode() # dm uden metaphone
        self.efternavn = unicode() #dmld metaphone
        self.kon = bool()
        self.alder_tal = int() # direkte maalign eller
        self.foedeaar = int() # direkte maalign eller
        self.civilstand = int()
        self.civilstand_source = unicode()
        self.foedested = unicode() #numerisk eller dmld
        self.valid = True
        self.matches = dict()
        self.erhverv = unicode()
        self.nregteskab = int()
        self.id = -1
        self.group = -1
        self.home_index = -1
        self.test = unicode()
        self.position = str()
        pass


# TODO Apply Double Metaphone to inexact names.
def name_comparison(p1, p2) :
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)
    if p1.navn == p2.navn :
        return 25
    #elif (doubleMetaphone(person1.navn,person2.navn) > 0 ) :
    #   return doubleMetaphone(person1.navn,person2.navn)
    else :
        fn_percentdifference = damerau_levenshtein_distance(p1.fornavn, p2.fornavn) / max(p1.fornavn, p2.fornavn)
        ml_percentdifference = damerau_levenshtein_distance(p1.mlnavn, p2.mlnavn) / max(p1.fornavn, p2.fornavn)
        en_percentdiffernece = damerau_levenshtein_distance(p1.efternavn, p2.efternavn) / max(p1.fornavn, p2.fornavn)
        result = 10 - damerau_levenshtein_distance(p1.fornavn, p2.fornavn)
        result += 5 - damerau_levenshtein_distance(p1.mlnavn, p2.mlnavn)
        result += 10 - damerau_levenshtein_distance(p1.efternavn, p2.efternavn)

    #Saa koerer vi dobbelt metaphonoe
# TODO Make more specific assignment of values to inexact cases.
def foedeaar_comparison(person1,person2) :
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)

    if (abs(person1.foedeaar - person2.foedeaar) < 3) :
        return 10 #man kan udvide med en variabel, der aendres med distancen imellem de to aldre
    else :
        return 0



# TODO apply double metaphone to inexact matching foedested
def foedested_comparison(person1, person2) :
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)
    if person1.fodested == person2.fodested :
        return 5
    else :
        return 0

def is_overhoved(person) :
    assert isinstance(person, Person)
    if(person.position == "husstandsoverhoved") :
        return True
    else :
        return False
def overhoved_comparison(p1,p2) :
    if(is_overhoved(p1) and is_overhoved(p2)) :
        return 5

def person_distance(p1,p2) :
    assert isinstance(p1, Person)
    assert isinstance(p2, Person)


    foedeaar_comparison(p1,p2)  + name_comparison(p1,p2) + foedested_comparison(p1,p2)

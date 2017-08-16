class Person:
    def __init__(self, year):
        assert isinstance(year, int)
        self.year = year
        self.kipNr = unicode()
        self.kilde = unicode()
        self.sogn = unicode()
        self.herred = unicode()
        self.amt = unicode()
        self.lbnr = int()
        self.kildehenvisning = unicode()
        self.stednavn = unicode()
        self.husstands_familienr = int()
        self.matr_nr_adresse = None
        self.fornavn = unicode()
        self.mlnavn = unicode()
        self.efternavn = unicode()
        self.kon = bool()
        self.alder_tal = int()
        self.foedeaar = int()
        self.civilstand = int()
        self.civilstand_source = unicode()
        self.foedested = unicode()
        self.valid = True
        self.matches = dict()
        self.erhverv = unicode()
        self.nregteskab = int()
        self.id = -1
        self.group = -1
        self.home_index = -1
        self.test = unicode()
        pass


# TODO Apply Double Metaphone to inexact names.
def name_comparison(person1,person2) :
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)
    if person1.navn == person2.navn :
        return 10
    #elif (doubleMetaphone(person1.navn,person2.navn) > 0 ) :
    #   return doubleMetaphone(person1.navn,person2.navn)
    else :
        return 0

    #Saa koerer vi dobbelt metaphonoe
# TODO Make more specific assignment of values to inexact cases.
def foedeaar_comparison(person1,person2) :
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)

    if (abs(person1.foedeaar - person2.foedeaar) < 2) :
        return 10
    else :
        return 0



# TODO apply double metaphone to inexact matching foedested
def foedested_comparison(person1, person2) :
    assert isinstance(person1, Person)
    assert isinstance(person2, Person)
    if person1.fodested == person2.fodested :
        return 10
    else :
        return 0






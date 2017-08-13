class Person:
    def __init__(self, year):
        assert isinstance(year, int)
        self.year = year
        self.kipNr = str()
        self.kilde = str()
        self.sogn = str()
        self.herred = str()
        self.amt = str()
        self.lbnr = int()
        self.kildehenvisning = str()
        self.stednavn = str()
        self.husstands_familienr = int()
        self.matr_nr_adresse = None
        self.fornavn = str()
        self.mlnavn = str()
        self.efternavn = str()
        self.kon = bool()
        self.alder_tal = int()
        self.foedeaar = int()
        self.civilstand = int()
        self.civilstand_source = str()
        self.foedested = str()
        self.valid = True
        self.matches = dict()
        self.erhverv = str()
        self.nregteskab = int()
        self.id = -1
        self.group = -1
        self.home_index = -1
        self.test = str()
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






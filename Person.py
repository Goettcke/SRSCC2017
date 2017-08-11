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
        self.navn = str()
        self.kon = bool()
        self.alder_tal = int()
        self.fodeaar = int()
        self.civilstand = int()
        self.civilstand_source = str()
        self.fodested = str()
        self.valid = True
        self.matches = dict()
        self.erhverv = str()
        self.nregteskab = int()
        self.id = -1
        self.group = -1
        self.home_index = -1
        pass


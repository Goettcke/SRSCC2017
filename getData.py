from Person import Person

people = []
bad_formatted_people = []

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

 # Hej Zuzka !!!! !!!
def getPeople(filename):
    fo = open(filename)
    while True:
        line = fo.readline().decode("iso-8859-1")
        lineSplit = line.split("|")
        if not line :
            break
        else :
            p = Person(1845)
            p.kipNr = lineSplit[0]
            p.kilde = lineSplit[1]
            p.sogn = lineSplit[2]
            p.herred = lineSplit[3]
            p.amt = lineSplit[4]
            p.lbnr = lineSplit[5]
            p.kildehenvisning = lineSplit[6]
            p.stednavn = lineSplit[7]
            p.husstnr = lineSplit[8]
            p.matr_nr_adresse = lineSplit[9]
            p.antal_familier_hus = lineSplit[10]
            p.navn = lineSplit[11]
            p.koen = lineSplit[12]
            p.alder = lineSplit[13]
            p.civilstkode = lineSplit[14]
            p.foedested = lineSplit[15]
            p.erhverv = lineSplit[16]
            p.kommentarer = lineSplit[17]
            p.foedeaar = lineSplit[18]
            p.navn = lineSplit[11]
            print "kipnr:  " + p.kipNr + " navn: " + p.navn
            people.append(p)


def get_people_to(filename,koen):
    fo = open(filename)
    counter = 1
    for line in fo:
        lineSplit = line.split("|")
        if (len(lineSplit)  == 13 and koen == lineSplit[5]) :
            counter = counter + 1
            p = Person(1845)
            p.amt = lineSplit[0]
            p.herred = lineSplit[1]
            p.sogn = lineSplit[2]
            p.test = lineSplit[3]


            navn_split = lineSplit[4].split(" ")
            p.fornavn = navn_split[0]

            for i in range(1,len(navn_split)-1,1):
                p.mlnavn = p.mlnavn + navn_split[i][0]

            p.efternavn = navn_split[-1]

            p.koen = lineSplit[5]
            p.foedested = lineSplit[6]
            p.foedeaar = lineSplit[7]
            p.civilstand = lineSplit[8]
            p.position = lineSplit[9]
            p.erhverv = lineSplit[10]
            p.kipnr = lineSplit[11]
            p.lbnr = lineSplit[12]
            people.append(p)



"""
def get_people_to(filename,koen):
    fo = open(filename)
    counter = 1
    while True:
        line = fo.readline()
        lineSplit = line.split("|")
        if not line :
            break
        else :
            if (len(lineSplit)  == 13 and koen == lineSplit[5]) :
                counter = counter + 1
                p = Person(1845)
                p.amt = lineSplit[0]
                p.herred = lineSplit[1]
                p.sogn = lineSplit[2]
                p.test = lineSplit[3]


                navn_split = lineSplit[4].split(" ")
                p.fornavn = navn_split[0]

                for i in range(1,len(navn_split)-1,1):
                    p.mlnavn = p.mlnavn + navn_split[i][0]

                p.efternavn = navn_split[-1]

                p.koen = lineSplit[5]
                p.foedested = lineSplit[6]
                p.foedeaar = lineSplit[7]
                p.civilstand = lineSplit[8]
                p.position = lineSplit[9]
                p.erhverv = lineSplit[10]
                p.kipnr = lineSplit[11]
                p.lbnr = lineSplit[12]
                people.append(p)
    




"""
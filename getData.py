from Person import Person
fo = open("TOY/FT1845.csv") # This is simple how to open a file


def getPeople(file):
    fo = open(file)
    while True:
        line = fo.readline()
        if line == None :
            break
        else :
            p = Person(1845)

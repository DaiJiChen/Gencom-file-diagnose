import sys


class Gedcom:
    def __init__(self, filename):
        self.analyse(filename)

    #analyse GEDCOM file line by line, and store data into two dictionarries.
    def analyse(self, filename):
        lines = open(filename, 'r')
        for line in lines:
            print("a")


def main(filename):
    gc = Gedcom(filename)


if __name__ == "__main__":
    main("gedcomfile.ged")
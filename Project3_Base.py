#Thomas Chu  18 September 2019
#Jichen Dai  26 Sept 2019
#I pledge my honor that I have abided by the Stevens Honor System
import prettytable as pt
import datetime
import os
import validate
    
    


class Gedcom:
    def __init__(self, filename):
        self.individuals = dict()
        self.families = dict()

        self.indi_table = pt.PrettyTable()
        self.indi_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        self.fam_table = pt.PrettyTable()
        self.fam_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                             "Children"]
        self.analyse(filename)

    #analyse GEDCOM file line by line, and store data into two dictionarries.
    def analyse(self, filename):
        lines = open(filename, 'r')
        indi = ""
        fam = ""
        plevel = ""  # DATE will use the previous line.
        ptag = ""
        flag = 0
        for x in lines:
            #Extract information from inputline: <level> <tag> <args>
            x = x.strip('\n')
            x = x.strip()
            level = x[0]
            strip1 = x[2:]
            split = strip1.split(' ',1)
            tag = split[0]
            if len(split) > 1:
                args = split[1]
            else:
                args = ''
            if level == "0" and args in ["INDI", "FAM"]:
                tag, args = args, tag

            #levle == "0" means beginning of a individual or family
            if level == "0":
                if tag  == "INDI":
                    flag = 1
                    indi = args.replace("@", "")
                    self.individuals[indi] = Individual()
                if tag == "FAM":
                    flag = 2
                    fam = args.replace("@", "")
                    self.families[fam] = Family()

            elif flag in [1, 2]:
                if args != "":
                # if args == "", it is BIRT or DEAT or MARR or DIV. We will deal with it in the next line.
                    if level == "1":
                        args = args.replace("@", "")
                        if flag == 1:
                            if tag == "NAME":
                                self.individuals[indi].name = args
                            elif tag == "SEX":
                                self.individuals[indi].sex = args
                            elif tag == "FAMC":
                                self.individuals[indi].famc = args
                            elif tag == "FAMS":
                                self.individuals[indi].fams.add(args)
                        elif flag == 2:
                            if tag == "HUSB":
                                self.families[fam].husb = args
                            elif tag == "WIFE":
                                self.families[fam].wife = args
                            elif tag == "CHIL":
                                self.families[fam].chil.add(args)

                    elif level == "2" and tag == "DATE":
                        if flag == 1:
                            if ptag == "BIRT":
                                self.individuals[indi].birt = args
                            elif ptag == "DEAT":
                                self.individuals[indi].deat = args
                        elif flag == 2:
                            if ptag == "MARR":
                                self.families[fam].marr = args
                            elif ptag == "DIV":
                                self.families[fam].div = args
            plevel = level
            ptag = tag
        for indi in self.individuals.values():
            indi.calcuAge()

    #Put the data in two dictionaries into two prettytables, and print prettytables.
    def print_table(self):
        print("Individual Table")
        for ID, indi in self.individuals.items():
            self.indi_table.add_row([ID, indi.name, indi.sex, indi.birt, indi.age, indi.alive, indi.deat, indi.famc, indi.fams])
        print(self.indi_table)

        print("Family Table")
        for ID, fam in self.families.items():
            if fam.husb != None and fam.wife != None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, self.individuals[fam.husb].name, fam.wife, self.individuals[fam.wife].name, fam.chil])
            elif fam.husb == None and fam.wife == None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, None, fam.wife, None, fam.chil])
            elif fam.husb == None and fam.wife != None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, None, fam.wife, self.individuals[fam.wife].name, fam.chil])
            elif fam.husb != None and fam.wife == None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, self.individuals[fam.husb].name, fam.wife, None, fam.chil])
        print(self.fam_table)



############################################ define Individual and Family ################################################################
class Family:
    def __init__(self):
        self.marr = None
        self.div = None
        self.husb = None
        self.wife = None
        self.chil = set()


class Individual:
    def __init__(self):
        self.name = None
        self.sex = None
        self.birt = None
        self.age = None
        self.alive = True
        self.deat = None
        self.famc = None
        self.fams = set()

    def calcuAge(self):
        if self.deat == None:
            self.alive = True
        else:
            self.alive = False
        if self.alive:
            self.age = datetime.datetime.now().year - int(self.birt.split(' ',2)[2])
        else:
            self.age = int(self.deat.split(' ',2)[2]) - int(self.birt.split(' ',2)[2])



def main(filename):
    gc = Gedcom(filename)
    validate(gc)
    gc.print_table()
    

if __name__ == "__main__" :
    main(sys.argv[1:])
    
    
    
  
    

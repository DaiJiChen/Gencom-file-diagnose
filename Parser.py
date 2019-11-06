#Thomas Chu  18 September 2019
#Jichen Dai  26 Sept 2019
#I pledge my honor that I have abided by the Stevens Honor System
import prettytable as pt
from datetime import date
import os
import validate
import sys
from operator import itemgetter

months = {
    "JAN":1,
    "FEB":2,
    "MAR":3,
    "APR":4,
    "MAY":5,
    "JUN":6,
    "JUL":7,
    "AUG":8,
    "SEP":9,
    "OCT":10,
    "NOV":11,
    "DEC":12
}

days = {
    1:31,
    2:28,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}


#converts a date in GEDCOM format to a date object, checking for invalid dates
def makeDate(GEDDate):
    temp = GEDDate.split(' ')
    day = int(temp[0])
    month = months[temp[1]]
    if day > days[month]:
        return date(int(temp[2]),month,days[month])
    else:
        return date(int(temp[2]), months[temp[1]], int(temp[0]))

#calculates the number of years from date1 to date2 if date2 is supplied, years since date1 if not
def calcAge(date1, date2=date.today()):
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))


class Gedcom:
    def __init__(self, filename):
        self.US42 = []
        self.existedIndi = {}
        self.existedFam = {}
        self.duplicateIndi = []
        self.duplicateFam = []
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
                if tag == "INDI":
                    flag = 1
                    indi = args.replace("@", "")
                    if indi not in self.existedIndi:
                        self.existedIndi[indi] = 1
                        self.individuals[indi] = Individual()
                    else:
                        flag = 3
                        self.duplicateIndi.append("US22 Error with individual  " + str(indi) + " : " + "duplicate ID")
                if tag == "FAM":
                    flag = 2
                    fam = args.replace("@", "")
                    if fam not in self.existedFam:
                        self.existedFam[fam] = 1
                        self.families[fam] = Family()
                    else:
                        flag = 3
                        self.duplicateFam.append("US22 Error with family  " + str(fam) + " : " + "duplicate ID")

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
        self.illDate() # US41
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
            # US28 orderSiblingsByAge
            chil = []
            for indi in fam.chil:
                chil.append(indi)
            if len(fam.chil) > 1:
                for i in range(len(chil)-1):
                    for j in range(i+1, len(chil)):
                        if self.individuals[chil[i]].age < self.individuals[chil[j]].age:
                            chil[i], chil[j] = chil[j], chil[i]

            if fam.husb != None and fam.wife != None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, self.individuals[fam.husb].name, fam.wife, self.individuals[fam.wife].name, chil])
            elif fam.husb == None and fam.wife == None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, None, fam.wife, None, chil])
            elif fam.husb == None and fam.wife != None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, None, fam.wife, self.individuals[fam.wife].name, chil])
            elif fam.husb != None and fam.wife == None:
                self.fam_table.add_row([ID, fam.marr, fam.div, fam.husb, self.individuals[fam.husb].name, fam.wife, None, chil])
        print(self.fam_table)

    # US29: list all deceased individuals outside the prettytable
    def list_deceased(self):
        print("\nUS29 ---------------- list all deceased individuals -----------------")
        for indiID, indi in self.individuals.items():
            if indi.deat != None:
                print("Individual " + indiID + "(" + indi.name + ") : Died in", indi.deat, "at the age of", str(indi.age) + ".")

    # US30: list all living married people outside the prettytable
    def list_livingMarriage(self):
        print("\nUS30 ---------------- list all living married people ----------------")
        for indiID, indi in self.individuals.items():
            if(indi.deat == None):
                married = 0
                for famID, fam in self.families.items():
                    if fam.husb == indiID or fam.wife == indiID:
                        married = 1
                if married == 0:
                    print("Individual", indiID, "is alive and is not married")

    def displayOutput(self,flags):
        if not flags:
            self.print_table()
        for flag in flags:
            if flag == "print": self.print_table()
            if flag == "US29": self.list_deceased()
            if flag == "US30": self.list_livingMarriage()

          
    def illDate(self):
        for id, indi in self.individuals.items():
            if indi.birt != None:
                temp = indi.birt.split(' ')
                day = int(temp[0])
                month = months[temp[1]]
                if day > days[month]:
                    self.US42.append("US42 Error with individual  "+ str(id)+ ": Birthday "+ str(indi.birt)+ " is illegitimate")
                    temp[0] = str(days[months[temp[1]]])
                indi.birt = temp[0] + " " + temp[1] + " " + temp[2]

            if indi.deat != None:
                temp = indi.deat.split(' ')
                day = int(temp[0])
                month = months[temp[1]]
                if day > days[month]:
                    self.US42.append("US42 Error with individual   " + str(id) + ": death date "+ str(indi.deat)+ " is illegitimate")
                    temp[0] = str(days[months[temp[1]]])
                indi.deat = temp[0] + " " + temp[1] + " " + temp[2]

        for id, fam in self.families.items():
            if fam.div != None:
                temp = fam.div.split(' ')
                day = int(temp[0])
                month = months[temp[1]]
                if day > days[month]:
                    self.US42.append("US42 Error with family      "+ str(id)+ ": divorce date " + str(fam.div)+ " is illegitimate")
                    temp[0] = str(days[months[temp[1]]])
                fam.div = temp[0] + " " + temp[1] + " " + temp[2]

            if fam.marr != None:
                temp = fam.marr.split(' ')
                day = int(temp[0])
                month = months[temp[1]]
                if day > days[month]:
                    self.US42.append("US42 Error with family      " + str(id)+ ": marriage date "+ str(fam.marr)+ " is illegitimate")
                    temp[0] = str(days[months[temp[1]]])
                fam.marr = temp[0] + " " + temp[1] + " " + temp[2]
                
                
    #US29 List deceased
    def deceasedIndividuals(self):
        deceasedIndividuals= []
        for id, indi in self.individuals.items():    
            if indi.deat != None:
                deceasedIndividuals.append(id)          
        print("Deceased individuals: " + str(deceasedIndividuals))
        
    # US28 Order siblings by age
    def siblingsByAge(self):
        for famid, fam in self.families.items():
            if fam.chil != None:
                childOrder = dict()
                children = fam.chil
                for childId in children:
                    childBirt = makeDate(self.individuals[childId].birt)
                    childAge = calcAge(childBirt)
                    childOrder[childId] = childAge 
                childOrder = sorted(childOrder.items(),key=itemgetter(1), reverse=True)
                print("Ordered siblings in family ", famid, " are : ", childOrder)

                
                
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
            self.age = calcAge(makeDate(self.birt))
        else:
            self.age = calcAge(makeDate(self.birt),makeDate(self.deat))



def main(filename, flags):
    gc = Gedcom(filename)
    gc.displayOutput(flags)
    print("\n\n\n========================= Error informations ==========================\n")
    validate.validate(gc)
    for x in gc.duplicateIndi:
        print(x)
    for x in gc.duplicateFam:
        print(x)
    for x in gc.US42:
        print(x)

if __name__ == "__main__" :
        if len(sys.argv) == 2:
            main(sys.argv[1],[])
        elif len(sys.argv) > 2:
            main(sys.argv[1],sys.argv[2:])
        else:
            print("ERROR: Must provide a gedcom filename")

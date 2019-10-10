from datetime import date

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


#converts a date in GEDCOM format to a date object
def makeDate(GEDDate):
    temp = GEDDate.split(' ')
    return date(int(temp[2]), int(months[temp[1]]), int(temp[0]))

#calculates the number of years from date1 to date2 if date2 is supplied, years since date1 if not
def calcAge(date1, date2=date.today()):
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))


#define testing functions here
#each testing function should take in an entire Gedcom and iterate over the individuals/families
#it will remove any entries that fail its test and print a message identifying the individual/family id
#ex. 
#def birth_before_death(gc):
#   for indiv in gc.individuals:
#     if fail:
#       print failure message
#       gc.families/individuals.pop(id)



           
# Code for birth and death and marriage and divorce before current date (functions commented out because they were not tested yet)
# def birtDeatB4CurrDate(gc):
#     for id, indi in gc.individuals.items():
#         if calcAge(indi.birt) >= 0:
#             print("Error with individual ", id, ": Birth is after current date.")
#             gc.individuals.pop(id)
#         elif calcAge(indi.deat) >= 0:
#             print("Error with individual ", id, ": Death is after current date.")
#             gc.individuals.pop(id)
            
# def marrDivB4CurrDate(gc):
#     for id, fam in gc.families.items():
#         marrdate = makeDate(fam.marr)
#         divdate =  makeDate(fam.div)
#         if calcAge(marrdate) >= 0:
#             print("Error with family ", id, ": Marriage is after current date.")
#             gc.individuals.pop(id)
#         elif calcAge(divdate) >= 0:
#             print("Error with family ", id, ": Divorce is after current date.")
#             gc.individuals.pop(id)


# US02
def BirtBeforeMarr(gc):
    for id, fam in gc.families.items():
        if fam.marr != None:
            marrdate = makeDate(fam.marr)
            remove = False
            if fam.husb != None:
                husb = gc.individuals[fam.husb]
                husbbirt = makeDate(husb.birt)
                if calcAge(husbbirt, marrdate) < 0:
                    print("ERROR: FAMILY: US03: Family ", id, ": Individual ", husb.name, " borns", husb.birt,
                          " before marry", fam.marr)
                    return 0
                    remove = True
            if fam.wife != None:
                wife = gc.individuals[fam.wife]
                wifebirt = makeDate(wife.birt)
                if calcAge(wifebirt, marrdate) < 0:
                    print("ERROR: FAMILY: US03: Family ", id, ": Individual ", wife.name, " borns", wife.birt,
                          " before marry", fam.marr)
                    return 0
                    remove = True

            if remove:
                gc.families.pop(id)
    return 1


# US03
def BirtBeforeDeat(gc):
    for id, indi in gc.individuals.items():
        if indi.deat != None:
            if indi.age < 0:
                print("ERROR: INDIVIDUAL: US02: ", id, ": Birth", indi.birt," before death", indi.deat)
                return 0
                gc.individuals.pop(id)
    return 1


# US0506 Marriage Before Death AND Divorce Before Death
# Compare date
def CompareDate(date1, date2):
    if date2.year - date1.year > 0:
        return 0
    if date2.year - date1.year < 0:
        return 1
    if date2.year - date1.year == 0:
        if date2.month - date1.month > 0:
            return 0
        if date2.month - date1.month < 0:
            return 1
        if date2.month - date1.month == 0:
            if date2.day - date1.day > 0:
                return 0
            if date2.day - date1.day < 0:
                return 1


# get death date from individuals
def getDeathDate(gc, i):
    for id, indi in gc.individuals.items():
        if i == id:
            if indi.deat != None:
                return indi.deat


# User Story 05
def MarriageBeforeDeath(gc):
    for id, fam in gc.families.items():
        if (getDeathDate(gc, fam.husb) != None):
            if (CompareDate(makeDate(fam.marr), makeDate(getDeathDate(gc, fam.husb))) > 0):
                print(id + " family have marriage dates after death dates")
                return 0
        if (getDeathDate(gc, fam.wife) != None):
            if (CompareDate(makeDate(fam.marr), makeDate(getDeathDate(gc, fam.wife))) > 0):
                print(id + " family have marriage dates after death dates")
                return 0
        else:
            print("There are no marriage dates after the death dates in family " + id)
            return 1


#User Story 06
def DivorceBeforeDeath(gc):    
    for id, fam in gc.families.items():       
        if(fam.div != None):           
            if(getDeathDate(gc,fam.husb) != None):                
                if(CompareDate(makeDate(fam.div),makeDate(getDeathDate(gc,fam.husb)))>0):                   
                    print(id + " family have div dates after death dates")
                    return 0
            if(getDeathDate(gc,fam.wife) != None):                
                if(CompareDate(makeDate(fam.div),makeDate(getDeathDate(gc,fam.wife)))>0):                    
                    print(id + " family have div dates after death dates")
                    return 0
        else:            
            print("There are no div dates after the death dates in family "+ id)
            return 1


# US07
def under150(gc):
    for id, indi in gc.individuals.items():
        if indi.age >= 150:
            print("Error with individual ", id, ": Age is not less than 150")
            gc.individuals.pop(id)


# US10
def marrAfter14(gc):
    for id, fam in gc.families.items():
        if fam.marr != None:
            marrdate = makeDate(fam.marr)
            remove = False
            if fam.husb != None:
                husb = gc.individuals[fam.husb]
                husbbirt = makeDate(husb.birt)
                if calcAge(husbbirt, marrdate) < 14:
                    print("Error with family ", id, ": Individual ", husb, " was not at least 14 at time of marriage")
                    remove = True
            if fam.wife != None:
                wife = gc.individuals[fam.wife]
                wifebirt = makeDate(wife.birt)
                if calcAge(wifebirt, marrdate) < 14:
                    print("Error with family ", id, ": Individual ", wife, " was not at least 14 at time of marriage")
                    remove = True

            if remove:
                gc.families.pop(id)



def validate(gc):
  under150(gc)
  marrAfter14(gc)
  MarriageBeforeDeath(gc)
  DivorceBeforeDeath(gc)
  BirtBeforeDeat(gc)
  BirtBeforeMarr(gc)

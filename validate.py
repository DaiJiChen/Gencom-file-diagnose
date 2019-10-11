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


#define testing functions here
#each testing function should take in an entire Gedcom and iterate over the individuals/families
#it will remove any entries that fail its test and print a message identifying the individual/family id
#ex. 
#def birth_before_death(gc):
#   for indiv in gc.individuals:
#     if fail:
#       print failure message
#       gc.families/individuals.pop(id)



#US01_1           
def birtDeatB4CurrDate(gc):
    removedIndividuals= []
    for id, indi in gc.individuals.items():
        remove = False  
        if indi.birt != None:
            if calcAge(makeDate(indi.birt)) >= 0:
                print("Error with individual ", id, ": Birth is after current date.")
                remove = True      
        if indi.deat != None:
            if calcAge(makeDate(indi.deat)) >= 0:
                print("Error with individual ", id, ": Death is after current date.")
                remove = True
        if remove:
            removedIndividuals.append(id)     
    for removeId in removedIndividuals:
        gc.individuals.pop(removeId)   
                     
#US01_2
def marrDivB4CurrDate(gc):
    removedFams = []
    for famid, fam in gc.families.items():
        remove = False
        if fam.marr != None:
            marrdate = makeDate(fam.marr)
            if calcAge(marrdate) >= 0:
                print("Error with family ", famid, ": Marriage is after current date.")
                remove = True      
        if fam.div != None:
            divdate =  makeDate(fam.div)
            if calcAge(divdate) >= 0:
                print("Error with family ", famid, ": Divorce is after current date.")
                remove = True
        if remove:
            removedFams.append(famid)     
    for removeId in removedFams:
        gc.families.pop(removeId)

        
        

# US02
def BirtBeforeMarr(gc):
    success = -1
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
                    success = 0
                    remove = True
            if fam.wife != None:
                wife = gc.individuals[fam.wife]
                wifebirt = makeDate(wife.birt)
                if calcAge(wifebirt, marrdate) < 0:
                    print("ERROR: FAMILY: US03: Family ", id, ": Individual ", wife.name, " borns", wife.birt,
                          " before marry", fam.marr)
                    success = 0
                    remove = True

            if remove:
                gc.families.pop(id)
    if success == 0:
        return 0
    else:
        return 1


# US03
def BirtBeforeDeat(gc):
    success = -1
    for id, indi in gc.individuals.items():
        if indi.deat != None:
            if indi.age < 0:
                print("ERROR: INDIVIDUAL: US02: ", id, ": Birth", indi.birt," before death", indi.deat)
                success = 0
                gc.individuals.pop(id)
    if success == 0:
        return 0
    else:
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


#User Story 05
def MarriageBeforeDeath(gc):
    success = -1
    for id, fam in gc.families.items():
        if(fam.marr != None):           
            if(getDeathDate(gc,fam.husb) != None):                
                if(CompareDate(makeDate(fam.marr),makeDate(getDeathDate(gc,fam.husb)))>0):                   
                    print(id + " family have marriage dates after death dates")
                    success = 0
            if(getDeathDate(gc,fam.wife) != None):                
                if(CompareDate(makeDate(fam.marr),makeDate(getDeathDate(gc,fam.wife)))>0):                    
                    print(id + " family have marriage dates after death dates")
                    success = 0
        else:            
            print("There are no marriage dates after the death dates in family "+ id)
    if success == 0:
        return 0
    else:
        return 1


#User Story 06
def DivorceBeforeDeath(gc):
    success = -1
    for id, fam in gc.families.items():
        if(fam.div != None):           
            if(getDeathDate(gc,fam.husb) != None):                
                if(CompareDate(makeDate(fam.div),makeDate(getDeathDate(gc,fam.husb)))>0):                   
                    print(id + " family have div dates after death dates")
                    success = 0
            if(getDeathDate(gc,fam.wife) != None):                
                if(CompareDate(makeDate(fam.div),makeDate(getDeathDate(gc,fam.wife)))>0):                    
                    print(id + " family have div dates after death dates")
                    success = 0
        else:            
            print("There are no div dates after the death dates in family "+ id)
    if success == 0:
        return 0
    else:
        return 1


# US07
def under150(gc):
    for id, indi in gc.individuals.items():
        if indi.age >= 150:
            print("Error with individual ", id, ": Age is not less than 150")
            gc.individuals.pop(id)

# US08 US09 marriage before divorce and unique ID
# Get the marriage date of a family
def getMarrDate(gc, f):
    for id, fam in gc.families.items():
        if f == id:
            if fam.marr != None:
                return fam.marr

# Get the divorce date of a family
def getDivDate(gc, f):
    for id, fam in gc.families.items():
        if f == id:
            if fam.div != None:
                return fam.div
            
# US08 marriage before divorce
# divBeforeMarr() takes the entire Gedcom file as argument and iterate over all individual and family records.
# It removes any family that has a marriage date prior to its divorce date.
# It prints a message displaying the family id.
def divBeforeMarr(gc):
    invalid = -1
    for id, fam in gc.families.items():
        divDate = makeDate(getDivDate(gc, id))
        marrDate = makeDate(getMarrDate(gc, id))
        if divDate != None and marrDate != None:
            if CompareDate(marrDate, divDate) > 0:
                print(id + "family has divorce date before marriage date")
                invalid = 0
        else:
            print("Missing divorce date or marriage date in the family record!")
    if invalid == 0:
        return 0
    else:
        return 1

# US22 unique ID
# duplicateID() takes the entire Gedcom file as argument and iterate over all individual and family records.
# It removes any entry (individual or family) that has a duplicate ID.
# It prints a message displaying the entry id.

def duplicateID(gc):
    duplicated = -1

    existedIndi = {}
    duplicateIndi = []

    for indiID in gc.individuals.items():
        if indiID != None:
            if indiID not in existedIndi:
                existedIndi[indiID] = 1
            else:
                if existedIndi[indiID] == 1:
                    duplicateIndi.append(indiID)
                existedIndi[indiID] += 1
        else:
            print("Missing individual ID!")

    existedFam = {}
    duplicateFam = []

    for famID in gc.families.items():
        if famID != None:
            if famID not in existedFam:
                existedFam[famID] = 1
            else:
                if existedFam[famID] == 1:
                    duplicateFam.append(famID)
                existedIndi[famID] += 1
        else:
            print("Missing family ID!")

    if len(duplicateIndi) > 0 or len(duplicateFam) > 0:
        duplicated = 0
    
    if duplicated == 0:
        return 0
    else:
        return 1

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
  duplicateID(gc)
  under150(gc)
  marrAfter14(gc)
  MarriageBeforeDeath(gc)
  DivorceBeforeDeath(gc)
  BirtBeforeDeat(gc)
  BirtBeforeMarr(gc)

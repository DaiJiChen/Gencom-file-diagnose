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
            if calcAge(makeDate(indi.birt)) < 0:
                print("US01 Error with individual ", id, ": Birth is after current date.")
                remove = True      
        if indi.deat != None:
            if calcAge(makeDate(indi.deat)) < 0:
                print("US01 Error with individual ", id, ": Death is after current date.")
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
            if calcAge(marrdate) < 0:
                print("US01 Error with family     ", famid, ": Marriage is after current date.")
                remove = True      
        if fam.div != None:
            divdate =  makeDate(fam.div)
            if calcAge(divdate) < 0:
                print("US01 Error with family     ", famid, ": Divorce is after current date.")
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
                    print("US02 Erroe with individual ", id, ": Individual ", husb.name, " borns", husb.birt,
                          " before marry", fam.marr)
                    success = 0
            if fam.wife != None:
                wife = gc.individuals[fam.wife]
                wifebirt = makeDate(wife.birt)
                if calcAge(wifebirt, marrdate) < 0:
                    print("US02 Erroe with individual ", id, ": Individual ", wife.name, " borns", wife.birt,
                          " before marry", fam.marr)
                    success = 0

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
                print("US03 Error with individual ", id, ": Birth", indi.birt," before death", indi.deat)
                success = 0
    if success == 0:
        return 0
    else:
        return 1

# US04 marriage before divorce
# divBeforeMarr() takes the entire Gedcom file as argument and iterate over all individual and family records.
# It prints a message displaying the family id.
def marrBeforeDiv(gc):
    invalid = -1
    for id, fam in gc.families.items():
        if fam.div != None and fam.marr != None:
            divDate = makeDate(fam.div)
            marrDate = makeDate(fam.marr)
            if calcAge(marrDate, divDate) < 0:
                print("US04 Error with family     ", id + " : family has marriage date after divorce date")
                invalid = 0
    if invalid == 0:
        return 0
    else:
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
                if(calcAge(makeDate(fam.marr),makeDate(getDeathDate(gc,fam.husb)))<0):
                    print("US05 Error with individual ",id + ": family have marriage dates after death dates")
                    success = 0
            if(getDeathDate(gc,fam.wife) != None):                
                if(calcAge(makeDate(fam.marr),makeDate(getDeathDate(gc,fam.wife)))<0):
                    print("US05 Error with individual ",id + ": family have marriage dates after death dates")
                    success = 0
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
                if(calcAge(makeDate(fam.div),makeDate(getDeathDate(gc,fam.husb)))<0):
                    print("US06 Error with individual ", id + ": family have div dates after death dates")
                    success = 0
            if(getDeathDate(gc,fam.wife) != None):
                if(calcAge(makeDate(fam.div),makeDate(getDeathDate(gc,fam.wife)))<0):
                    print("US06 Error with individual ", id + ": family have div dates after death dates")
                    success = 0
    if success == 0:
        return 0
    else:
        return 1


# US07
def under150(gc):
    success = -1
    for id, indi in gc.individuals.items():
        if indi.age >= 150:
            print("US07 Error with individual ", id, ": Age is not less than 150")
            success = 0
    if success == 0:
        return 0
    else:
        return 1


# US10
def marrAfter14(gc):
    success = -1
    for id, fam in gc.families.items():
        if fam.marr != None:
            marrdate = makeDate(fam.marr)

            if fam.husb != None:
                husb = gc.individuals[fam.husb]
                husbbirt = makeDate(husb.birt)
                if calcAge(husbbirt, marrdate) < 14:
                    print("US10 Error with family     ", id, ": Individual ", husb.name, " was not at least 14 at time of marriage")
                    success = 0

            if fam.wife != None:
                wife = gc.individuals[fam.wife]
                wifebirt = makeDate(wife.birt)
                if calcAge(wifebirt, marrdate) < 14:
                    print("US10 Error with family     ", id, ": Individual ", wife.name, " was not at least 14 at time of marriage")
                    success = 0
    if success == 0:
        return 0
    else:
        return 1


# US14
def siblingsFewerThan15(gc):
    success = -1
    for id, fam in gc.families.items():
        if(len(fam.chil) > 15):
            print("US14 Error with family     ", id, ": This family has more than 15 children")
            success = 0
    if success == 0:
        return 0
    else:
        return 1

# US15
def multiBirthLessThan5(gc):
    success = -1
    for famID, fam in gc.families.items():
        birthday = {}
        for indiID, indi in gc.individuals.items():
            if (indi.famc == famID):
                if (indi.birt not in birthday):
                    birthday[indi.birt] = 1
                else:
                    birthday[indi.birt] += 1
        max = 0
        for birthday, number in birthday.items():
            if number>max:
                max = number
        if max>5:
            print("US15 Error with family     ", famID, ": More than five siblings born at the same time")
            success = 0

    if success == 0:
        return 0
    else:
        return 1

#US16
def maleLastNames(gc):
    success = -1
    for id, fam in gc.families.items():
        error = 0
        lastName = None
        if fam.husb != None:
            fatherName = fam.husb.name
            lastName = fatherName.split(' ')[-1]
        for childID in fam.chil:
            child = gc.individuals[childID]
            if child.sex == "M":
                if lastName == None:
                    lastName = child.name.split(' ')[-1]
                else:
                    if lastname != child.name.split(' ')[-1]:
                        success = 0
                        if error == 0:
                            print("US16 Error with family     ", id, ": At least one male has a different last name")
                            error = 1

    if success == 0:
        return 0
    else:
        return 1
    
    
# US17
def NoMarriagesToDescendants(gc):
    success = -1
    husbgroup=set()
    wifegroup=set()
    for id, fam in gc.families.items():
        childrengroup=set()
        if fam.husb != None:
            if fam.wife != None:
                husbset=set()
                husbset.add(fam.husb)
                if(husbset & husbgroup == set()):
                    husbID=fam.husb
                    husbgroup.add(fam.husb)
                    for id, fam_a in gc.families.items():
                        if fam_a.husb == husbID:
                            childrengroup = childrengroup | fam_a.chil
                    for id, fam_b in gc.families.items():
                        if fam_b.husb == husbID:
                            wifefam=set()
                            wifefam.add(fam_b.wife)
                            if(wifefam & childrengroup != set()):
                                print("US17 Error with family     ", id, ": Parents marry their descendants")
                                success = 0                                
    for id, fam in gc.families.items():
        childrengroup=set()
        if fam.husb != None:
            if fam.wife != None:
                wifeset=set()
                wifeset.add(fam.wife)
                if(wifeset & wifegroup == set()):
                    wifeID=fam.wife
                    wifegroup.add(fam.wife)
                    for id, fam_a in gc.families.items():
                        if fam_a.wife == wifeID:
                            childrengroup = childrengroup | fam_a.chil
                    for id, fam_b in gc.families.items():
                        if fam_b.wife == wifeID:
                            husbfam=set()
                            husbfam.add(fam_b.husb)
                            if(husbfam & childrengroup != set()):
                                print("US17 Error with family     ", id, ": Parents marry their descendants")
                                success = 0                                
    if success == 0:
        return 0
    else:
        return 1           
                
# US18
def SiblingsShouldNotMarry(gc):
    success = -1
    for id , fam in gc.families.items():
        if fam.chil != None:
            chilset = fam.chil
            chillist = list(fam.chil)
            if len(chillist)>1:
                i = 0
                while i<len(chillist):
                    chilID=chillist[i]
                    chilset.remove(chilID)
                    for id, family in gc.families.items():
                        if family.husb != None:
                            if family.wife != None:
                                if chilID == family.husb or chilID == family.wife:
                                    famset = set()
                                    famset.add(family.husb)
                                    famset.add(family.wife)
                                    if famset & chilset != set():
                                        print("US18 Error with family     ", id, ": Siblings marry one another")
                                        success = 0
                    i += 1                    
    if success == 0:
        return 0
    else:
        return 1                                   
            
#US21
def roleGender(gc):
    success = -1
    for id, fam in gc.families.items():
        if fam.husb != None:
            husband = gc.individuals[fam.husb]
            if husband.sex != "M":
                print("US21 Error with family     ", id, ": Husband " + husband + " is not male")
                success = 0

        if fam.wife != None:
            wife = gc.individuals[fam.wife]
            if wife.sex != "F":
                print("US21 Error with family     ", id, ": Wife " + wife + " is not female")
                success = 0

    if success == 0:
        return 0
    else:
        return 1

def validate(gc):
  under150(gc)
  marrAfter14(gc)
  MarriageBeforeDeath(gc) # US05
  DivorceBeforeDeath(gc) # US06
  BirtBeforeMarr(gc) # US02
  BirtBeforeDeat(gc) # US03
  marrBeforeDiv(gc) 
  birtDeatB4CurrDate(gc) 
  marrDivB4CurrDate(gc)
  siblingsFewerThan15(gc) # US14
  multiBirthLessThan5(gc) # US15
  maleLastNames(gc)
  NoMarriagesToDescendants(gc) # US17
  SiblingsShouldNotMarry(gc) # US18
  roleGender(gc)

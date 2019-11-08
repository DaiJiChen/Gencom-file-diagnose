from datetime import date

months = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}

days = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}
# converts a date in GEDCOM format to a date object, checking for invalid dates


def makeDate(GEDDate):
    temp = GEDDate.split(' ')
    day = int(temp[0])
    month = months[temp[1]]
    if day > days[month]:
        return date(int(temp[2]), month, days[month])
    else:
        return date(int(temp[2]), months[temp[1]], int(temp[0]))

# calculates the number of years from date1 to date2 if date2 is supplied, years since date1 if not


def calcAge(date1, date2=date.today()):
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))


def countLeapYears(d):
    years = d.year
    if (d.month <= 2):
        years -= 1
    return int(years / 4 - years / 100 + years / 400)


# This function returns number of days between two given dates
def getDifference(dt1, dt2):
    n1 = dt1.year * 365 + dt1.day
    for i in range(0, dt1.month - 1):
        n1 += days[i+1]
    #n1 += countLeapYears(dt1)
    n2 = dt2.year * 365 + dt2.day
    for i in range(0, dt2.month - 1):
        n2 += days[i+1]
    #n2 += countLeapYears(dt2)
    return (n2 - n1)


# define testing functions here
# each testing function should take in an entire Gedcom and iterate over the individuals/families
# it will remove any entries that fail its test and print a message identifying the individual/family id
# ex.
# def birth_before_death(gc):
#   for indiv in gc.individuals:
#     if fail:
#       print failure message




# US01_1
def birtDeatB4CurrDate(gc):
    removedIndividuals = []
    for id, indi in gc.individuals.items():
        remove = False
        if indi.birt != None:
            if calcAge(makeDate(indi.birt)) < 0:
                print("US01 Error with individual ", id,
                      ": Birth is after current date.")
                remove = True
        if indi.deat != None:
            if calcAge(makeDate(indi.deat)) < 0:
                print("US01 Error with individual ", id,
                      ": Death is after current date.")
                remove = True

    if remove == 0:
        return 0
    else:
        return 1

# US01_2
def marrDivB4CurrDate(gc):
    removedFams = []
    for famid, fam in gc.families.items():
        remove = False
        if fam.marr != None:
            marrdate = makeDate(fam.marr)
            if calcAge(marrdate) < 0:
                print("US01 Error with family     ", famid,
                      ": Marriage is after current date.")
                remove = True
        if fam.div != None:
            divdate = makeDate(fam.div)
            if calcAge(divdate) < 0:
                print("US01 Error with family     ", famid,
                      ": Divorce is after current date.")
                remove = True

    if remove == 0:
        return 0
    else:
        return 1


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
                    print("US02 Erroe with individual ", id, ": Individual ", husb.name, " was born", husb.birt,
                          " before marriage date ", fam.marr)
                    success = 0
            if fam.wife != None:
                wife = gc.individuals[fam.wife]
                wifebirt = makeDate(wife.birt)
                if calcAge(wifebirt, marrdate) < 0:
                    print("US02 Erroe with individual ", id, ": Individual ", wife.name, " was born", wife.birt,
                          " before marriage date ", fam.marr)
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
                print("US03 Error with individual ", id, ": Birth",
                      indi.birt, " before death", indi.deat)
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
                print("US04 Error with family     ", id +
                      " : family has marriage date after divorce date")
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


# User Story 05
def MarriageBeforeDeath(gc):
    success = -1
    for id, fam in gc.families.items():
        if(fam.marr != None):
            if(getDeathDate(gc, fam.husb) != None):
                if(calcAge(makeDate(fam.marr), makeDate(getDeathDate(gc, fam.husb))) < 0):
                    print("US05 Error with individual ", id +
                          ": family have marriage dates after death dates")
                    success = 0
            if(getDeathDate(gc, fam.wife) != None):
                if(calcAge(makeDate(fam.marr), makeDate(getDeathDate(gc, fam.wife))) < 0):
                    print("US05 Error with individual ", id +
                          ": family have marriage dates after death dates")
                    success = 0
    if success == 0:
        return 0
    else:
        return 1


# User Story 06
def DivorceBeforeDeath(gc):
    success = -1
    for id, fam in gc.families.items():
        if(fam.div != None):
            if(getDeathDate(gc, fam.husb) != None):
                if(calcAge(makeDate(fam.div), makeDate(getDeathDate(gc, fam.husb))) < 0):
                    print("US06 Error with individual ", id +
                          ": family have div dates after death dates")
                    success = 0
            if(getDeathDate(gc, fam.wife) != None):
                if(calcAge(makeDate(fam.div), makeDate(getDeathDate(gc, fam.wife))) < 0):
                    print("US06 Error with individual ", id +
                          ": family have div dates after death dates")
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
            print("US07 Error with individual ",
                  id, ": Age is not less than 150")
            success = 0
    if success == 0:
        return 0
    else:
        return 1

# US08
# Individual MUST be born after the marriage of his/her parents
def birthB4ParentMarr(gc):
    invalid = -1
    for indiID, indi in gc.individuals.items():
        if indi.birt != None:
            indiBirthDate = makeDate(indi.birt)
            famc = indi.famc
            for famID, fam in gc.families.items():
                if famID == famc:
                    if fam.marr != None:
                        marrDate = makeDate(fam.marr)
                        #print("indi:", indiID, "birth:", indi.birt, "fam:", famID, "marr:", fam.marr)
                        if calcAge(indiBirthDate, marrDate) > 0:
                            print("US08 Error with individual:", indiID, indi.name, "was born", indi.birt,
                                  "before parents' marriage date", fam.marr)
                            invalid = 0
    if invalid == 0:
        return 0
    else:
        return 1

# US09
# Individual MUST be born before the death of his/her parents
def birthB4ParentDeath(gc):
    invalid = -1
    for indiID, indi in gc.individuals.items():
        if indi.birt != None:
            indiBirthDate = makeDate(indi.birt)
            famc = indi.famc
            for famID, fam in gc.families.items():
                if famID == famc:
                    if fam.husb != None:
                        husb = gc.individuals[fam.husb]
                        if husb.deat != None:
                            patDeathDate = makeDate(husb.deat)
                            if calcAge(indiBirthDate, patDeathDate) < 0:
                                print("US09 Error with individual:", indiID, indi.name, "was born", indi.birt, "after father's death date ", husb.deat)
                                invalid = 0
                    if fam.wife != None:
                        wife = gc.individuals[fam.wife]
                        if wife.deat != None:
                            matDeathDate = makeDate(wife.deat)
                            if calcAge(indiBirthDate, matDeathDate) < 0:
                                print("US09 Error with individual:", indiID, indi.name, "was born", indi.birt, "after mother's death date ", wife.deat)
                                invalid = 0
    if invalid == 0:
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

# US11
def noBigamy(gc):
    success = -1
    for indiID, indi in gc.individuals.items():
        if len(indi.fams) > 1:
            famIDs = []
            for familyID in indi.fams:
                famIDs.append(familyID)
            for i in range(len(famIDs)-1):
                for j in range(i + 1, len(famIDs)):
                    if gc.families[famIDs[j]].marr != None and gc.families[famIDs[i]].marr != None:
                        marrDate1 = gc.families[famIDs[i]].marr
                        marrDate2 = gc.families[famIDs[j]].marr
                        if marrDate1 <= marrDate2:
                            if gc.families[famIDs[i]].div == None or gc.families[famIDs[i]].div > marrDate2:
                                success = 0
                                print("US11 Error with individual:", indiID, "is bigamy (", famIDs[i], famIDs[j], ")")
                        elif marrDate1 > marrDate2:
                            if gc.families[famIDs[j]].div == None or gc.families[famIDs[j]].div > marrDate2:
                                success = 0
                                print("US11 Error with individual:", indiID, "is bigamy (", famIDs[i], famIDs[j], ")")
    if success == 0:
        return 0
    else:
        return 1

# US12 Parents not too old    Mother should be less than 60 years older than her children and father should be less than 
# 80 years older than his children
def parrTooOld(gc):
    success = -1
    for famid, fam in gc.families.items():
        removedChildren = []
        
        if fam.chil != None:
            if fam.wife != None:
                mother = gc.individuals[fam.wife]
                motherBirt = makeDate(mother.birt)
                children = fam.chil
                for childId in children:
                    childM = gc.individuals[childId]
                    childBirt = makeDate(childM.birt)
                    if calcAge(motherBirt, childBirt) > 60:
                        removedChildren.append(childId)
                        success = 0
                        print("US12 Error with family     ", famid, ": Mother is 60 years older than her child " + (childM.name) )
                
            if fam.husb != None:
                father = gc.individuals[fam.husb]
                fatherBirt = makeDate(father.birt)
                children = fam.chil
                for childId in children:
                    childH = gc.individuals[childId]
                    childBirt = makeDate(childH.birt)
                    if calcAge(fatherBirt, childBirt) > 80:
                        removedChildren.append(childId)
                        success = 0
                        print("US12 Error with family     ", famid, ": Father is 80 years older than his child " + (childH.name) )
 
        
        
        #for childID in removedChildren:
            #fam.chil.discard(childID)
            #gc.individuals[childID].famc = None
    if success == 0:
        return 0
    else:
        return 1
            
# US13 Siblings spacing    Birth dates of siblings should be more than 8 months apart or less than 2 days 
# apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
def siblingSpace(gc):
    success = -1
    for famid, fam in gc.families.items():
        if fam.chil != None:
            children = fam.chil
            s = []
            for c in children:
                s.append(c)
            #do nested for loop with variable i, j+1
            for i in range(len(s)-1):
                childOne = gc.individuals[s[i]]
                childOneBirt = makeDate(childOne.birt)

                for j in range(i+1, len(s)):
                    childOther = gc.individuals[s[j]]
                    childOtherBirt = makeDate(childOther.birt)
                    if getDifference(childOneBirt, childOtherBirt)<242 and getDifference(childOneBirt, childOtherBirt)>0:
                        success = 0
                        print("US13 Error with family     ", famid, ": Child birth space not valid, child ID:", s[i], s[j])
    
    #for childID in removedChildren:
        #fam.chil.discard(childID)
        #gc.individuals[childID].famc = None
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
            fatherName = gc.individuals[fam.husb].name
            lastName = fatherName.split(' ')[-1]
        for childID in fam.chil:
            child = gc.individuals[childID]
            if child.sex == "M":
                if lastName == None:
                    lastName = child.name.split(' ')[-1]
                else:
                    if lastName != child.name.split(' ')[-1]:
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
            chilset = set() | fam.chil
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

#US19 
def FirstCousinsShouldNotMarry(gc):
    success = -1
    for id,fam_first in gc.families.items():
        allthird = set()
        if fam_first.chil != None:
            chil_firstlist = list(fam_first.chil)
            if len(chil_firstlist)>1:
                i = 0
                while i<len(chil_firstlist):
                    chil_firstID = chil_firstlist[i]
                    chil_secondset = set()
                    for id, family_second in gc.families.items():
                        if chil_firstID == family_second.husb or chil_firstID == family_second.wife:
                            chil_secondset = chil_secondset | family_second.chil
                    allthird = allthird | chil_secondset
                    i += 1
        if fam_first.chil != None:
            chil_firstlist = list(fam_first.chil)
            if len(chil_firstlist)>1:
                i = 0
                while i<len(chil_firstlist):
                    chil_firstID = chil_firstlist[i]
                    chil_secondset = set()
                    for id, family_second in gc.families.items():
                        if chil_firstID == family_second.husb or chil_firstID == family_second.wife:
                            chil_secondset = chil_secondset | family_second.chil
                    allthird = allthird - chil_secondset
                    chil_secondlist = list(chil_secondset)
                    j=0
                    while j<len(chil_secondlist):
                        chil_secondID = chil_secondlist[j]
                        for id, family_third in gc.families.items():
                            if family_third.husb != None and family_third.wife != None:
                                if chil_secondID == family_third.husb or chil_secondID == family_third.wife:
                                    fam_thirdset = set()
                                    fam_thirdset.add(family_third.husb)
                                    fam_thirdset.add(family_third.wife)
                                    fam_thirdset.remove(chil_secondID)
                                    if fam_thirdset & allthird != set():
                                        print("US19 Error with family     ", id, ": First cousins should not marry one another")
                                        success = 0    
                        j +=1 
                    i += 1        
    if success == 0:
        return 0
    else:
        return 1


#US20
def AuntsAndUnclesNotMarryNiecesNephews(gc):
    success = -1
    for id,fam_first in gc.families.items():
        if fam_first.chil != None:
            chil_firstlist = list(fam_first.chil)
            if len(chil_firstlist)>1:
                i = 0
                while i<len(chil_firstlist):
                    chil_firstID = chil_firstlist[i]
                    chil_firstset = set() | fam_first.chil
                    chil_firstset.remove(chil_firstID)
                    chil_secondset = set()
                    for id, family_second in gc.families.items():
                        if chil_firstID == family_second.husb or chil_firstID == family_second.wife:
                            chil_secondset = chil_secondset | family_second.chil
                    chil_secondlist = list(chil_secondset)
                    j = 0
                    while j<len(chil_secondlist):
                        chil_secondID = chil_secondlist[j]
                        for id, family_third in gc.families.items():
                            if family_third.husb != None and family_third.wife != None:
                                if chil_secondID == family_third.husb or chil_secondID == family_third.wife:
                                    fam_thirdset = set()
                                    fam_thirdset.add(family_third.husb)
                                    fam_thirdset.add(family_third.wife)
                                    fam_thirdset.remove(chil_secondID)
                                    if fam_thirdset & chil_firstset != set():
                                        print("US20 Error with family     ", id, ": Aunts and uncles should not marry their nieces or nephews")
                                        success = 0
                        j += 1
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
                print("US21 Error with family     ", id, ": Husband " + fam.husb + " is not male")
                success = 0

        if fam.wife != None:
            wife = gc.individuals[fam.wife]
            if wife.sex != "F":
                print("US21 Error with family     ", id, ": Wife " + fam.wife + " is not female")
                success = 0

    if success == 0:
        return 0
    else:
        return 1

#US23
def uniqueNameBirth(gc):
    success = -1
    pairs = {}
    for id, indi in gc.individuals.items():
        for indiID, individual in gc.individuals.items():
            if id != indiID and indiID > id:
                if indi.name == individual.name and indi.birt == individual.birt:
                    success = 0
                    print("US23 Error with individuals ", id," and ", indiID,": Individuals cannot share a name and birth date")
    
    if success == 0:
        return 0
    else:
        return 1    

# US24
def uniFamBySpouse(gc):
    invalid = -1
    for id1, fam1 in gc.families.items():
        famID1 = id1
        if fam1.husb != None and fam1.wife != None and fam1.marr != None:
            husb1 = fam1.husb
            wife1 = fam1.wife
            marr1 = fam1.marr
            for id2, fam2 in gc.families.items():
                famID2 = id2
                if fam2.husb != None and fam2.wife != None and fam2.marr != None:
                    husb2 = fam2.husb
                    wife2 = fam2.wife
                    marr2 = fam2.marr
                    if famID1 != famID2:
                        if husb1 == husb2 and wife1 == wife2 and marr1 == marr2:
                            invalid = 0
                            print("US24 Error with family     ", id1, "and", id2, "has the same husband, same wife and same marriage date")
    if invalid == 0:
        return 0
    else:
        return 1

# US25
def uniFirstNameFam(gc):
    invalid = -1
    for ID, fam in gc.families.items():
        chil = []
        for indi in fam.chil:
            chil.append(indi)
        if len(fam.chil) > 1:
            for i in range(len(chil) - 1):
                for j in range(i + 1, len(chil)):
                    if gc.individuals[chil[i]].birt == gc.individuals[chil[j]].birt and gc.individuals[chil[i]].name == gc.individuals[chil[j]].name:
                        print("US25 Error with family     ", ID, "has children with same name and same birthday.")
                        invalid = 0
    #for famID, fam in gc.families.items():
        #if fam.chil != None and len(fam.chil) != 0:
            #childName = set()
            #for child in fam.chil:
                #for indiID, indi in gc.individuals.items():
                    #if child == indiID and indi.name != None:
                        #childName.add(indi.name)
            #if len(fam.chil) != len(childName):
                #print("US24 Error with family     ", famID , "has children with same name and same birthday.")
                #invalid = 0
    if invalid == 0:
        return 0
    else:
        return 1

# print US22
def print_US22(gc):
    for x in gc.duplicateIndi:
        print(x)
    for x in gc.duplicateFam:
        print(x)

# US26
def correspondingEntries(gc):
    success = -1
    for indiID, indi in gc.individuals.items():
        # test existence of child record in family
        if indi.famc != None:
            coEntry = 0
            for famID, fam in gc.families.items():
                if famID == indi.famc:
                    for chilID in fam.chil:
                        if chilID == indiID:
                            coEntry = 1
                    if coEntry == 0:
                        success = 0
                        print("US26 Error with family     ", indiID,
                              " Don't have corresponding child record in family ", famID)
        if len(indi.fams) != 0:
        # test existence of sponser record in family
            for sponserID in indi.fams:
                for famID, fam in gc.families.items():
                    if famID == sponserID:
                        if fam.wife != indiID and fam.husb != indiID:
                            success = 0
                            print("US26 Error with family     ", indiID, " Don't have corresponding sponser record in family ",famID)

    for famID, fam in gc.families.items():
        if fam.wife != None:
        # test existence of wife record in individual
            for indiID, indi in gc.individuals.items():
                if indiID == fam.wife:
                    coEntry = 0
                    for sponserID in indi.fams:
                        if sponserID == famID:
                            coEntry = 1
                    if coEntry == 0:
                        success = 0
                        print("US26 Error with individual:", famID, " Don't have corresponding wife record in individual ",indiID)
        if fam.husb != None:
        # test existence of husb record in individual
            for indiID, indi in gc.individuals.items():
                if indiID == fam.husb:
                    coEntry = 0
                    for sponserID in indi.fams:
                        if sponserID == famID:
                            coEntry = 1
                    if coEntry == 0:
                        success = 0
                        print("US26 Error with individual:", famID, " Don't have corresponding wife record in individual ",indiID)
        if len(fam.chil)!=0:
        # test existence of child record in individual
            for chilID in fam.chil:
                for indiID, indi in gc.individuals.items():
                    if indiID == chilID:
                        if indi.famc == None:
                            success = 0
                            print("US26 Error with individual:", famID, " Don't have corresponding child record in individual ", indiID)
    if success == 0:
        return 0
    else:
        return 1

# US42
def print_US42(gc):
    for x in gc.US42: # US42
        print(x)

def validate(gc):
  birtDeatB4CurrDate(gc)# US01
  marrDivB4CurrDate(gc)# US01
  BirtBeforeMarr(gc) # US02
  BirtBeforeDeat(gc) # US03
  marrBeforeDiv(gc) # US04
  MarriageBeforeDeath(gc) # US05
  DivorceBeforeDeath(gc) # US06
  under150(gc) # US07
  birthB4ParentMarr(gc) # US08
  birthB4ParentDeath(gc) # US09
  marrAfter14(gc) # US10
  noBigamy(gc) # US11
  parrTooOld(gc)# US12
  siblingSpace(gc)# US13
  siblingsFewerThan15(gc) # US14
  multiBirthLessThan5(gc) # US15
  maleLastNames(gc) # US16
  NoMarriagesToDescendants(gc) # US17
  SiblingsShouldNotMarry(gc) # US18
  FirstCousinsShouldNotMarry(gc) # US19
  AuntsAndUnclesNotMarryNiecesNephews(gc) # US20
  roleGender(gc) # US21
  print_US22(gc) # US22
  uniqueNameBirth(gc) # US23
  uniFamBySpouse(gc) # US24
  uniFirstNameFam(gc) # US25
  correspondingEntries(gc) # US26
  # US27--US40 is written in Parser
  print_US42(gc) # US42



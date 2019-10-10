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

# Converts a date in GEDCOM format to a date object
def makeDate(GEDDate):
    temp = GEDDate.split(' ')
    return date(temp[2], months[temp[1]], temp[0])

# Calculates the number of years from date1 to date2 if date2 is supplied, years since date1 if not
def calcAge(date1, date2 = date.today):
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

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

def sprint1(gc):
    divBeforeMarr(gc)
    duplicateID(gc) 
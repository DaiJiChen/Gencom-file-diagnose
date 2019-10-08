from datetime import date

def months = {
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
    return date(temp[2], months[temp[1]], temp[0])

#calculates the number of years from date1 to date2 if date2 is supplied, years since date1 if not
def calcAge(date1, date2=date.today):
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

def under150(gc):
    for id, indi in gc.individuals.items():
        if indi.age >= 150:
            print("Error with individual ", id, ": Age is not less than 150")
            gc.individuals.pop(id)

def marrAfter14(gc):
    for id, fam in gc.families.items():
        marrdate = makeDate(fam.marr)
        remove = false
        if fam.husb != None:
            husb = gc.individuals[fam.husb]
            husbbirt = makeDate(husb.birt)
            if calcAge(husbbirt, marrdate) < 14:
                print("Error with family ", id, ": Individual ", husb, " was not at least 14 at time of marriage")
                remove = true
        if fam.wife != None:
            wife = gc.individuals[fam.wife]
            wifebirt = makeDate(wife.birt)
            if calcAge(wifebirt, marrdate) < 14:
                print("Error with family ", id, ": Individual ", wife, " was not at least 14 at time of marriage")
                remove = true
        
        if remove:
            gc.families.pop(id)
            





def validate(gc):
  under150(gc)
  marrAfter14(gc)



# get a GEDCOM file
file = open("C:\\Users\\daiji\\OneDrive\\Desktop\\CS555\\Project\\gedcomfile.ged")

# define three types of supported tag
Level_Tag = ["BIRT", "DEAT", "MARR", "DIV", "HEAD", "TRLR"]
Level_Tag_Argu = ["NAME", "SEX", "FAMC", "FAMS", "HUSB", "WIFE", "CHIL", "DATE", "NOTE"]
Level_Argu_Tag = ["INDI", "FAM"]

# read GEDCOM file line by line
for line in file:
    print("-->" + line,end="")
    str = line.split()
    type = 0  #types of tage

    # type1: lines with no arguments
    for tag in Level_Tag:
        if str[1] == tag:
            type = 1
            print("<--" + str[0] + "|" + str[1] + "|Y|")

    # type2: lines with the structure: level tag arguments
    for tag in Level_Tag_Argu:
        if str[1] == tag:
            type = 2
            print("<--" + str[0] + "|" + str[1] + "|Y|", end=' '),
            for item in str[2:]:
                print(item, end=' ')
            print()

    # type3: lines that tag = INDI or FAM
    for tag in Level_Argu_Tag:
        if type == 0 and str[2] == tag:
            type = 3
            print("<--" + str[0] + "|" + str[2] + "|Y|" + str[1])

    # invalid type
    if type == 0:
        print("<--" + str[0] + "|" + str[1] + "|N|" + str[2])

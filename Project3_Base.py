#Thomas Chu
#18 September 2019
#I pledge my honor that I have abided by the Stevens Honor System

import sys



#create dictionary for keyword lookup
keywords = {
    "0" : {
        "INDI" : "Y",
        "FAM" : "Y",
        "HEAD" : "Y",
        "TRLR" : "Y",
        "NOTE" : "Y"
    },

    "1" : {
        "NAME" : "Y",
        "SEX" : "Y",
        "BIRT" : "Y",
        "DEAT" : "Y",
        "FAMC" : "Y",
        "FAMS" : "Y",
        "MARR" : "Y",
        "HUSB" : "Y",
        "WIFE" : "Y",
        "CHIL" : "Y",
        "DIV" : "Y"
    },
    
    "2" : {
        "DATE" : "Y"
    }
}



def main(argv):
    #Check for correct number of arguments
    if len(argv) != 1:
        print("Correct usage is: Chu_Project2.py <GEDCOM filename>")

    #Open file
    filename = argv[0]
    with open(filename,'r') as f:
        #Read file line by line
        lines = f.readlines()

        #For each line:
        for x in lines:
            #Print input line
            x=x.replace('\n','')
            print("--> ",x,"\n<-- ", sep='', end='')
            
            #Extract information from inputline: <level> <tag> <args>
            level = x[0]
            strip1 = x[2:]
            split = strip1.split(' ',1)
            tag = split[0]
            if len(split) > 1:
                args = split[1]
            else:
                args = ''


            #If level is 1 or 2, line is in form <level> <tag> <args>, so lookup is simple
            if level == "1" or level == "2":
                #Find the keyword in the dictionary. Valid will be "Y" if there, "N" if not.
                valid = keywords[level].get(tag, "N")

            #If level is 0, lookup is more complicated
            else:
                #Attempt to find the keyword.
                valid = keywords[level].get(tag, "N")
                
                #If the keyword is not there, must check if the tag is actually in args
                if valid == "N":
                    valid = keywords[level].get(args, "N")

                    #If the tag is in args, must switch values of tag and args
                    if valid == "Y":
                        tag, args = args, tag
            
            
            #Print the formatted information
            print(level,tag,valid,args, sep="|")




if __name__ == "__main__" :
    main(sys.argv[1:])
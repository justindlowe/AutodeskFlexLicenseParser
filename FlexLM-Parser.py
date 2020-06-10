#import Modules
#MySQL
import mysql.connector as mysql

#Add MySQL Stuff
db = mysql.connect(host="machineaddress", user="username", passwd="password", database="licenseusage")
cursor = db.cursor()

#Define functions
def parselogfile(logfile):
    #Get first date in log file and set this as the date before main parse. This is to accompany the first entries in the log that may be before the first TIMESTAMP entry.
    #---------------------------------------------------------------------
    date = '00/00/0000'
    with open(logfile, 'r') as dategathering:
        for dateline in dategathering:
            linefields = dateline.split(" ")
            if len(linefields) >= 3:
                #Catch and store date
                if linefields[2] == "TIMESTAMP":
                    date = linefields[3].split()[0]
                    break
    dategathering.close()
    #---------------------------------------------------------------------
    #Declare username variable outside of loop
    username = None
    #The loop below will insert results into the following list. This list will be returned by the function.
    listofdata = []
    #Begin loop for log file
    with open(logfile, 'r') as lines:
        for line in lines:
            product = None
            #Split each line
            linefields = line.split(" ")
            #Drop any lines with not enough fields to check for TIMESTAMP. Not necessary but may prevent future errors.
            if len(linefields) >= 3:
                #Catch and store date. As the loop progresses through the log, the date is updated.
                if linefields[2] == "TIMESTAMP":
                    date = linefields[3].split()[0]
            #Drops any lines with not enough fields to check for checkout
            if len(linefields) > 4:
                #If line contains OUT: in field 2
                if linefields[2] == 'OUT:':
                    #This section grabs from the same line
                    #-------------------------------------
                    #Splits line and grabs username
                    username = linefields[4].split("@")[0]
                    #Converts to lowercase. 
                    usernamelowercase = username.lower()
                    #-------------------------------------
                    #The next set of lines searches for product codes and stores the matches as a friendly name. We grab the year instead of comparing for multiple years.
                    if "RVT" in linefields[3].split('"')[1]:
                        product = "Revit " + linefields[3].split('_')[1]
                    if "ACD" in linefields[3].split('"')[1]:
                        product = "AutoCAD " + linefields[3].split('_')[1]
                    if "CIV3D" in linefields[3].split('"')[1]:
                        product = "Civil 3D " + linefields[3].split('_')[1]
                    if "NAVMAN" in linefields[3].split('"')[1]:
                        product = "Navisworks Manage " + linefields[3].split('_')[1]
                    if "RECAP" in linefields[3].split('"')[1]:
                        product = "ReCap " + linefields[3].split('_')[1]
                    if "3DSMAX" in linefields[3].split('"')[1]:
                        product = "3DSMax " + linefields[3].split('_')[1]
            #If product is not blank 
            if product is not None:
                #print(usernamelowercase + " " + date + " " + product)
                listofdata.append([usernamelowercase, date, product])
    lines.close()
    return(listofdata)

def sendtosql(listofdata):
    #Loop through all entries in the list (each entry is a list within a list)
    for i in listofdata:
        #Parse data from list in list
        username = i[0]
        date = i[1]
        product = i[2]
        #prepare SQL query
        query = "INSERT IGNORE INTO licenseusage.main (username, date, product) VALUES (%s,%s,%s)"  % ("'" + username + "'", "'" + date + "'", "'" + product + "'")
        print(query)
        cursor.execute(query)
        db.commit()

#Run program
sendtosql(parselogfile('licensefilepath'))

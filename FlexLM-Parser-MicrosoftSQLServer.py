#import Modules
#SQL
import pyodbc

#Add SQL Stuff
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=servername;DATABASE=VBG-AutodeskLicenseUsage;UID=username;PWD=password')
cursor = conn.cursor()

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
        #SQL Query to check if record already exists in database
        cursor.execute("SELECT [username],[date],[product] FROM [VBG-AutodeskLicenseUsage].[dbo].[main] WHERE username=" + "'"+ username + "'" + " AND date=" + "'" + date + "'" + " AND product=" + "'" + product + "'")
        rowcount = cursor.rowcount
        #If number of rows is zero then no records exist and we will add it
        if rowcount == 0:
            print('Record does not exist. Adding:   ' + username + "     " + date + "     " + product)
            cursor.execute("INSERT INTO [VBG-AutodeskLicenseUsage].[dbo].[main] (username, date, product) VALUES (%s,%s,%s)"  % ("'" + username + "'", "'" + date + "'", "'" + product + "'"))
        else:
            print('This record already exists. Skipping...   ' + username + "     " + date + "     " + product)
        cursor.commit()
    cursor.close()

#Run program
sendtosql(parselogfile('C:\Dev\FlexLMParser\debug.log'))

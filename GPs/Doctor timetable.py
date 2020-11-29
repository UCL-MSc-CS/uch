from datetime import datetime,timedelta
import uch.Database.GP_timetablefunctions as db

def toregulartime(unixtimestamp):
    return datetime.utcfromtimestamp(int(unixtimestamp))

def printdays(date):
    start_date = date - timedelta(days=date.weekday())
    end_date = start_date + timedelta(days=6)
    for single_date in daterange(start_date, end_date):
        print("\n--------------------\n" + datetime.strftime(single_date, "%A %d %b %Y") + "\n--------------------")
        datestring = datetime.strftime(single_date, dateformatstring)
        appointments = db.timetableblock(doctorid, datestring)
        for appointment in appointments:
            reason = appointment[0]
            start = datetime.strftime(toregulartime(appointment[1]), timeformatstring)
            end = datetime.strftime(toregulartime(appointment[2]), timeformatstring)
            appointmentid = appointment[3]
            print(reason + "\t" + start + "-" + end + "\t" + appointmentid)

def selectreason():
    while True:
        reasondict = {1:'scheduled break',2:'admin tasks',3:'emergency leave',4:'other'}
        print("Please select a reason for non-patient hours: ")
        for key,value in reasondict.items():
            print("choose [" + str(key) + "] for " + value)
        option = input(":")
        try:
            if (1 <= int(option) <= len(reasondict)):
                reason = reasondict[int(option)]
                return reason
            else:
                print("You need to enter a value between 1 and " + len(reasondict) + " try again!")
        except:
            print("You failed to enter  number try again")


def validatedate(string):
    while True:
        try:
            datestring = input(string + " (YYYY-MM-DD): ")
            date = datetime.strptime(datestring,dateformatstring)
            return date
        except:
            print("Invalid date entered, try again...")

def validatetime(string):
    while True:
        try:
            timestring = input(string + " (HH:MM): ")
            time = datetime.strptime(timestring,timeformatstring)
            return time
        except:
            print("Invalid date entered, try again...")

def daterange(start_date, end_date):
    for n in range(int((end_date + timedelta(1) - start_date).days)):
        yield start_date + timedelta(n)

def printtimetable():
    now = datetime.today()
    today = datetime(now.year,now.month,now.day)
    print("Select option below to view weekly timetable:")
    print("choose [1] to view this week")
    print("choose [2] to view next week")
    print("choose [3] to view any other week.")
    option = input(":")
    try:
        if(int(option) == 1):
            printdays(today)
        elif(int(option) == 2):
            printdays(today+timedelta(7))
        elif(int(option) == 3):
            selecteddate = validatedate("Please enter a date to view its weekly timetable")
            printdays(selecteddate)
        else:
            print("invalid option choice, please try again")
    except:
        print("You didn't enter a number please try again")

def addholiday():
    startdate = validatedate("Please enter a start date")
    enddate = validatedate("Please enter an end date")
    startdatestring = datetime.strftime(startdate,dateformatstring)
    enddatestring = datetime.strftime(enddate,dateformatstring)
    busy = db.checkiftimebooked(doctorid,startdatestring,clinicstart,enddatestring,clinicend)
    if enddate >= startdate and not busy:
        reason = "holiday"
        appointmentId = ""
        for single_date in daterange(startdate, enddate):
            datestring = datetime.strftime(single_date, dateformatstring)
            db.bookslot(doctorid, datestring, clinicstart, clinicend,reason,appointmentId)
        print("Successfully booked holiday!!!")
    elif enddate >= startdate and busy:
        print("You are busy during this period")
    else:
        print("You have entered an end date that is before a start date. Please try again")

def addnonpatienthours():
    date = validatedate("Please enter a date")
    datestring = datetime.strftime(date, dateformatstring)
    starttime = validatetime("Please enter a start time")
    starttimestring = datetime.strftime(starttime, timeformatstring)
    endtime = validatetime("Please enter an end time")
    endtimestring = datetime.strftime(endtime, timeformatstring)
    busy = db.checkiftimebooked(doctorid,datestring,starttimestring,datestring,endtimestring)
    if starttime < endtime and not busy:
        appointmentId = ''
        reason = selectreason()
        db.bookslot(doctorid, datestring, starttimestring, endtimestring,reason,appointmentId)
        print("Successfully booked in non patient hours for " + datestring)
    elif starttime < endtime and busy:
        print("You already have booked time during this period, please check your timetable")
    else:
        print("You've entered an end time before a start time, please try again")

def clearhours():
    print("Select option below to clear hours: ")
    print("choose [1] to clear multiple days")
    print("choose [2] to clear hours on a given date")
    option = input(":")
    try:
        if(int(option)==1):
            startdate = validatedate("Please enter a start date")
            enddate = validatedate("Please enter an end date") + timedelta(1)
            startdatestring = datetime.strftime(startdate, dateformatstring)
            enddatestring = datetime.strftime(enddate, dateformatstring)
            if enddate > startdate:
                db.deletetime(doctorid,startdatestring,"00:00",enddatestring,"00:00")
                print("Successfully cleared all appointments between the given dates.")
            else:
                print("You need to enter an end date that's before your start date!, try again")
        elif(int(option)==2):
            date = validatedate("Please enter a date")
            datestring = datetime.strftime(date, dateformatstring)
            starttime = validatetime("Please enter a start time")
            starttimestring = datetime.strftime(starttime, timeformatstring)
            endtime = validatetime("Please enter an end time")
            endtimestring = datetime.strftime(endtime, timeformatstring)
            if endtime> starttime:
                db.deletetime(doctorid,datestring,starttimestring,datestring,endtimestring)
                print("Successfully cleared out all appointments in the time specified")
            else:
                print("You need to enter an end time after your start time, try again")
        else:
            print("You need to choose a number from the list provided, try again!")
    except:
        print("You need to enter a number value, try again!")


def continueorexit():
    repeat = True
    while repeat:
        val = input("Do you want to continue (Y/N) ?:")
        if val in ("Y","y"):
            repeat = False
            continueloop[0] = True
        elif val in ("N","n"):
            repeat = False
            continueloop[0] = False
        else:
            print("Please enter a valid response")


dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
doctorid = 1
starthour = 9
startmin = 0
endhour = 18
endmin = 0
clinicstart = "{:02d}".format(starthour) + ":" + "{:02d}".format(startmin)
clinicend =  "{:02d}".format(endhour) + ":" + "{:02d}".format(endmin)
today = datetime.today()
continueloop = [True]

#Todo get doctor details from query for the below print statement
print("Welcome Doctor " + str(doctorid) + " you can view and edit your timetable from this dialog")
while continueloop[0]:
    print("choose [1] to view your timetable")
    print("choose [2] to add holiday")
    print("choose [3] to add non-patient hours")
    print("choose [4] to clear hours from timetable")
    option = input(":")
    if option == "1":
        printtimetable()
    elif option == "2":
        addholiday()
    elif option == "3":
        addnonpatienthours()
    elif option == "4":
        clearhours()
    else:
        print("Invalid option chosen. Try again")
    continueorexit()
    print("------------------------------------------------------------------------------------------------------")

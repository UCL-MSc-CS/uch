from datetime import datetime
import usefulfunctions as uf
import timetablefunctions as db

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
starthour = 9
startmin = 0
endhour = 18
endmin = 0
clinicstart = "{:02d}".format(starthour) + ":" + "{:02d}".format(startmin)
clinicend =  "{:02d}".format(endhour) + ":" + "{:02d}".format(endmin)

def addnonpatienttime(doctoremail):
    print("choose [1] to book a holiday")
    print("choose [2] to add non-patient hours")
    choice = input(":")
    if choice == '1':
        addholiday(doctoremail)
    elif choice == '2':
        addnonpatienthours(doctoremail)
    else:
        print("Invalid option chosen, please try again")

def addholiday(doctoremail):
    startdate = uf.validatedate("Please enter a start date")
    enddate = uf.validatedate("Please enter an end date")
    if enddate >= startdate:
        for single_date in uf.daterange(startdate, enddate):
            datestring = datetime.strftime(single_date,dateformatstring)
            status = db.checkslotavailable(datestring, clinicstart, clinicend, [doctoremail])
            if status[0] == "unavailable":
                print("Sorry, you are busy during this period and cannot book your holiday")
                return 0
        reason = "holiday"
        for single_date in uf.daterange(startdate, enddate):
            datestring = datetime.strftime(single_date, dateformatstring)
            db.book_time(datestring, clinicstart, clinicend, reason, "", [doctoremail])
        print("Successfully booked holiday!!!")
    else:
        print("You have entered an end date that is before a start date. Please try again")


def addnonpatienthours(doctoremail):
    date = uf.validatedate("Please enter a date")
    datestring = datetime.strftime(date, dateformatstring)
    starttime = uf.validatetime("Please enter a start time")
    starttimestring = datetime.strftime(starttime, timeformatstring)
    endtime = uf.validatetime("Please enter an end time")
    endtimestring = datetime.strftime(endtime, timeformatstring)
    status = db.checkslotavailable(datestring, starttimestring, endtimestring, [doctoremail])
    if starttime < endtime and status[0] != 'unavailable':
        reason = selectreason()
        db.book_time(datestring, starttimestring, endtimestring, reason, "", [doctoremail])
        print("Successfully booked in non patient hours for " + datestring)
    elif starttime < endtime and status[0] == 'unavailable':
        print("You already have booked time during this period, please check your timetable")
    else:
        print("You've entered an end time before a start time, please try again")

def selectreason():
    while True:
        reasondict = {1:'scheduled break',2:'admin tasks',3:'emergency',4:'other'}
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
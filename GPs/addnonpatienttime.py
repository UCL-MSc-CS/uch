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
    while True:
        print("--------------------------------------------")
        print("\t Doctor Add non-patient time")
        print("--------------------------------------------")
        print("Choose [1] to book a holiday")
        print("Choose [2] to add non-patient hours")
        print("Choose [0] to return to main menu")
        choice = input(":")
        if choice == '1':
            addholiday(doctoremail)
            continue
        elif choice == '2':
            addnonpatienthours(doctoremail)
            continue
        elif choice == '0':
            break
        else:
            print("\n\t<Invalid option chosen, Please try again>\n")
        print("********************************************")

def addholiday(doctoremail):
    startdate = uf.validatedate("Please enter a start date")
    if startdate == 'exit':
        return
    elif startdate.date() < datetime.today().date():
        print("\n\t<You cannot book a holiday in the past!>\n")
        choice = input("Press [0] to try again, or any other entry to return to menu \n:")
        if choice == '0':
            addholiday(doctoremail)
        return
    enddate = uf.validatedate("Please enter an end date")
    if enddate == 'exit':
        addholiday(doctoremail)
        return
    if enddate >= startdate:
        for single_date in uf.daterange(startdate, enddate):
            datestring = datetime.strftime(single_date,dateformatstring)
            status = db.checkslotavailable(datestring, clinicstart, clinicend, [doctoremail])
            if status[0] == "unavailable":
                print("\n\t<Sorry, you are busy during this period and cannot book your holiday>\n")
                choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
                if choice == '0':
                    addholiday(doctoremail)
                return
        reason = "holiday"
        for single_date in uf.daterange(startdate, enddate):
            datestring = datetime.strftime(single_date, dateformatstring)
            db.book_time(datestring, clinicstart, clinicend, reason, "", [doctoremail])
        print("Successfully booked holiday!!!")
    else:
        print("\n\t<You have entered an end date that is before a start date. Please try again>\n")


def addnonpatienthours(doctoremail):
    chosendate = uf.validatedate("Please enter a date")
    if chosendate == 'exit':
        return
    if chosendate.date() < datetime.today().date():
        print("\n\t<You cannot book non-patient hours in the past!>\n")
        choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
        if choice == '0':
            addnonpatienthours(doctoremail)
        return
    datestring = datetime.strftime(chosendate, dateformatstring)
    starttime = uf.validatetime("Please enter a start time")
    if starttime == 'exit':
        addnonpatienthours(doctoremail)
        return
    starttimestring = datetime.strftime(starttime, timeformatstring)
    endtime = uf.validatetime("Please enter an end time")
    if endtime == 'exit':
        addnonpatienthours(doctoremail)
        return
    endtimestring = datetime.strftime(endtime, timeformatstring)
    status = db.checkslotavailable(datestring, starttimestring, endtimestring, [doctoremail])
    if starttime < endtime and status[0] != 'unavailable':
        reason = selectreason()
        db.book_time(datestring, starttimestring, endtimestring, reason, "", [doctoremail])
        print("Successfully booked in non patient hours for " + datestring)
    elif starttime < endtime and status[0] == 'unavailable':
        print("\n\t<You already have booked time during this period, please check your timetable>\n")
        choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
        if choice == '0':
            addnonpatienthours(doctoremail)
        return
    else:
        print("\n\t<You've entered an end time before a start time, please try again>\n")

def selectreason():
    while True:
        reasondict = {1:'scheduled break',2:'admin tasks',3:'emergency',4:'other'}
        print("Please select a reason for non-patient hours: ")
        for key,value in reasondict.items():
            print("Choose [" + str(key) + "] for " + value)
        option = input(":")
        try:
            if (1 <= int(option) <= len(reasondict)):
                reason = reasondict[int(option)]
                return reason
            else:
                print("\n\t<You need to enter a value between 1 and " + len(reasondict) + ", Please try again!>\n")
        except:
            print("\n\t<You failed to enter  number try again>\n")
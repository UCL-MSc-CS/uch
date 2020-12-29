from datetime import datetime
import useful_functions as uf
import timetable_functions as db

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
starthour = 9
startmin = 0
endhour = 18
endmin = 0
clinicstart = "{:02d}".format(starthour) + ":" + "{:02d}".format(startmin)
clinicend =  "{:02d}".format(endhour) + ":" + "{:02d}".format(endmin)

def add_non_patient_time(doctoremail):
    while True:
        print("--------------------------------------------")
        print("\t Doctor Add non-patient time")
        print("--------------------------------------------")
        print("Choose [1] to book a holiday")
        print("Choose [2] to add non-patient hours")
        print("Choose [0] to return to main menu")
        choice = input(":")
        if choice == '1':
            add_holiday(doctoremail)
            continue
        elif choice == '2':
            add_non_patient_hours(doctoremail)
            continue
        elif choice == '0':
            break
        else:
            print("\n\t<Invalid option chosen, Please try again>\n")
        print("********************************************")

def add_holiday(doctoremail):
    startdate = uf.validate_date("Please enter a start date")
    if startdate == 'exit':
        return
    elif startdate.date() < datetime.today().date():
        print("\n\t<You cannot book a holiday in the past!>\n")
        choice = input("Press [0] to try again, or any other entry to return to menu \n:")
        if choice == '0':
            add_holiday(doctoremail)
        return
    enddate = uf.validate_date("Please enter an end date")
    if enddate == 'exit':
        add_holiday(doctoremail)
        return
    if enddate >= startdate:
        for single_date in uf.date_range(startdate, enddate):
            datestring = datetime.strftime(single_date,dateformatstring)
            status = db.check_slot_available(datestring, clinicstart, clinicend, [doctoremail])
            if status[0] == "unavailable":
                print("\n\t<Sorry, you are busy during this period and cannot book your holiday>\n")
                choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
                if choice == '0':
                    add_holiday(doctoremail)
                return
        reason = "holiday"
        for single_date in uf.date_range(startdate, enddate):
            datestring = datetime.strftime(single_date, dateformatstring)
            db.book_time(datestring, clinicstart, clinicend, reason, "", [doctoremail])
            declined = db.auto_decline_pending(datestring, clinicstart, clinicend, doctoremail)
            if declined:
                print("Automatically declined any pending appointments on " + datestring)
        print("Successfully booked holiday!!!")
    else:
        print("\n\t<You have entered an end date that is before a start date. Please try again>\n")


def add_non_patient_hours(doctoremail):
    chosendate = uf.validate_date("Please enter a date")
    if chosendate == 'exit':
        return
    if chosendate.date() < datetime.today().date():
        print("\n\t<You cannot book non-patient hours in the past!>\n")
        choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
        if choice == '0':
            add_non_patient_hours(doctoremail)
        return
    datestring = datetime.strftime(chosendate, dateformatstring)
    starttime = uf.validate_time("Please enter a start time")
    if starttime == 'exit':
        add_non_patient_hours(doctoremail)
        return
    starttimestring = datetime.strftime(starttime, timeformatstring)
    endtime = uf.validate_time("Please enter an end time")
    if endtime == 'exit':
        add_non_patient_hours(doctoremail)
        return
    endtimestring = datetime.strftime(endtime, timeformatstring)
    status = db.check_slot_available(datestring, starttimestring, endtimestring, [doctoremail])
    if starttime < endtime and status[0] != 'unavailable':
        reason = select_reason()
        db.book_time(datestring, starttimestring, endtimestring, reason, "", [doctoremail])
        print("Successfully booked in non patient hours for " + datestring)
        declined = db.auto_decline_pending(datestring, starttimestring, endtimestring, doctoremail)
        if declined:
            print("Automatically declined any conflicting pending appointments during this time")
    elif starttime < endtime and status[0] == 'unavailable':
        print("\n\t<You already have booked time during this period, please check your timetable>\n")
        choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
        if choice == '0':
            add_non_patient_hours(doctoremail)
        return
    else:
        print("\n\t<You've entered an end time before a start time, please try again>\n")

def select_reason():
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
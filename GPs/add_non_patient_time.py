from datetime import datetime
import useful_functions as uf
import timetable_functions as db

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"
START_HOUR = 9
START_MIN = 0
END_HOUR = 18
END_MIN = 0
CLINIC_START = "{:02d}".format(START_HOUR) + ":" + "{:02d}".format(START_MIN)
CLINIC_END = "{:02d}".format(END_HOUR) + ":" + "{:02d}".format(END_MIN)

"""
Main Menu function for booking non-patient time

These can be things such as holidays, scheduled break hours, admin hours, emergency leave etc.
Time cannot be booked in the past. Time cannot be booked that conflicts with existing time.
"""
def add_non_patient_time(doctoremail):
    while True:
        print("--------------------------------------------")
        print("\t Doctor Add non-patient time")
        print("--------------------------------------------")
        print("Choose [1] to book a holiday")
        print("Choose [2] to add non-patient hours")
        print("Choose [0] to return to main menu")
        choice = input("Please select an option: ")
        if choice == '1':
            add_holiday(doctoremail)
            continue
        elif choice == '2':
            add_non_patient_hours(doctoremail)
            continue
        elif choice == '0':
            break
        else:
            print("\n\t< Invalid option chosen, Please try again >\n")
        print("********************************************")


"""
Specific function if the user selects add-holiday.

Will ask for a start and an end date and book out a timeslot with reason = "holiday" from the clinic start and
end times on each of those days. Will auto-decline any pending appointments (ones the doctor hasn't confirmed yet)
that are during the booked holiday.
"""
def add_holiday(doctoremail):
    startdate = uf.validate_date("Please enter a start date")
    if startdate == 'exit':
        # The user wishes to exit data entry at that point.
        return
    elif startdate.date() < datetime.today().date():
        print("\n\t< You cannot book a holiday in the past! >\n")
        choice = input("Press [0] to try again, or any other entry to return to menu \n:")
        if choice == '0':
            add_holiday(doctoremail)
        return

    enddate = uf.validate_date("Please enter an end date")
    if enddate == 'exit':
        # If the user realises that they entered the start date wrong, allow them to go back
        add_holiday(doctoremail)
        return

    if enddate >= startdate:
        # If the user successfully enters valid dates without exiting.
        # Create a range between the start and end date and loop from day to day.
        # If any of the days have existing appointments do not book the holiday
        for single_date in uf.date_range(startdate, enddate):
            date_string = datetime.strftime(single_date, DATE_FORMAT_STRING)
            # Create status variable to check if the doctor is available during that time period.
            status = db.check_slot_available(date_string, CLINIC_START, CLINIC_END, [doctoremail])
            if status[0] == "unavailable":
                print("\n\t< Sorry, you are busy during this period and cannot book your holiday >\n")
                choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
                if choice == '0':
                    # Try add you holiday again.
                    add_holiday(doctoremail)
                return

        # If the user has no existing appointments on those days then book the holidays
        reason = "holiday"
        for single_date in uf.date_range(startdate, enddate):
            date_string = datetime.strftime(single_date, DATE_FORMAT_STRING)
            db.book_time(date_string, CLINIC_START, CLINIC_END, reason, "", [doctoremail])
            # Auto-decline pending appointments
            declined = db.auto_decline_pending(date_string, CLINIC_START, CLINIC_END, doctoremail)
            if declined:
                print("Automatically declined any pending appointments on " + date_string)
        print("Successfully booked holiday!!!")
    else:
        print("\n\t< You have entered an end date that is before a start date. Please try again >\n")


"""
Adding times that aren't holidays.

These aren't blocked out on a day to day basis, these are individual timeslots you can book on a given day. Here you
can book items like 'emergency leave','scheduled breaks', 'admin tasks' etc.
Will first ask for a date to book it on, and then will ask for the start and end times. 
Auto-declines and pending appointments that conflict with the booked time. 
"""
def add_non_patient_hours(doctoremail):
    chosen_date = uf.validate_date("Please enter a date")
    if chosen_date == 'exit':
        # Exits the date entry if the user wishes.
        return
    if chosen_date.date() < datetime.today().date():
        # If the start date is in the past disallow booking time.
        print("\n\t< You cannot book non-patient hours in the past! >\n")
        choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
        if choice == '0':
            add_non_patient_hours(doctoremail)
        return
    date_string = datetime.strftime(chosen_date, DATE_FORMAT_STRING)

    start_time = uf.validate_time("Please enter a start time")
    if start_time == 'exit':
        # Exit start time entry.
        add_non_patient_hours(doctoremail)
        return
    start_time_string = datetime.strftime(start_time, TIME_FORMAT_STRING)

    end_time = uf.validate_time("Please enter an end time")
    if end_time == 'exit':
        #Exit end time entry.
        add_non_patient_hours(doctoremail)
        return
    end_time_string = datetime.strftime(end_time, TIME_FORMAT_STRING)

    # Check whether the GP is available during the times selected. and that the start is before the end.
    status = db.check_slot_available(date_string, start_time_string, end_time_string, [doctoremail])
    if start_time < end_time and status[0] != 'unavailable':
        reason = select_reason()
        db.book_time(date_string, start_time_string, end_time_string, reason, "", [doctoremail])
        print("Successfully booked in non patient hours for " + date_string)
        declined = db.auto_decline_pending(date_string, start_time_string, end_time_string, doctoremail)
        if declined:
            print("Automatically declined any conflicting pending appointments during this time")
    elif start_time < end_time and status[0] == 'unavailable':
        print("\n\t< You already have booked time during this period, please check your timetable >\n")
        choice = input("Press [0] to try again, or any other entry to return to main menu \n:")
        if choice == '0':
            add_non_patient_hours(doctoremail)
        return
    else:
        print("\n\t< You've entered an end time before a start time, please try again >\n")

"""
Select a reason for adding non-patient hours.

The reasons for non-patient time are numerous and can be seen in the "reasondict" python dictionary below.
"""
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
                print("\n\t< You need to enter a value between 1 and " + len(reasondict) + ", Please try again! >\n")
        except:
            print("\n\t< You failed to enter  number try again >\n")
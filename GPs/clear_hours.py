from datetime import datetime
import useful_functions as uf
import timetable_functions as db
from GPs.print_day import print_day

DATE_FORMAT_STRING = "%Y-%m-%d"

def clearhours(doctoremail):
    """
    Clears/Declines appointments chosen by the user.

    GP enters a date they want to clear appointments from.
    All appointments on that date are displayed to the GP.
    The GP chooses from the displayed appointments and enters the ID of the appointment they wish to clear.
    The GP can cancel multiple appointments at a time by entering a comma separated list.
    If the appointment is a patient appointment, it will decline the appointment
    If the appointment is a non-patient appointment, it will completely delete that appointment from the database.
    """
    print("--------------------------------------------")
    print("\t Doctor Cancel/Decline Appointments")
    print("--------------------------------------------")
    date = uf.validate_date("Enter a date you would like to cancel an appointment.")
    if date == 'exit':
        return
    # Calls a function below to print out all the appointments for that day.
    print_day(date, doctoremail)
    date_string = datetime.strftime(date, DATE_FORMAT_STRING)
    appointments = []
    for appointment in db.timetable_block(doctoremail, date_string):
        appointments.append(appointment[4])
    if not appointments:
        # Auto exits if there are no appointments on that given day.
        print("\t< There are no appointments on "+date_string+" returning to the main menu >")
        return
    print("\n\nPlease enter the appointment ids you would like to cancel separated by commas:")
    userinput = input(":")
    ids = userinput.split(",")
    for id in ids:
        try:
            idnum = int(id)
            if idnum in appointments:
                db.clear_booked_time(idnum)
                print("Successfully deleted Appointment " + str(idnum))
            else:
                print("\t < Appointment of ID: "+str(idnum)+" doesn't exist on the given date. >")
        except ValueError:
            print("\t< "+ id + " is not a valid number >")
    choice = input("\nPress [0] to return to the Cancel Appointment menu, press any other button for the Main Menu \n:")
    print("********************************************")
    if choice == '0':
        clearhours(doctoremail)
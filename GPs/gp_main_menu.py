from GPs.clear_hours import clearhours
from GPs.print_timetable import print_timetable
from GPs.add_non_patient_time import add_non_patient_time
from GPs.confirm_appointments import confirm_appointments
from GPs.open_appointment import open_appointment
from open_past_appointments 

def gp_main_menu(gp_email, gp_full_name):
    """
    The main menu function for GPs.

    Most options will auto-return to this screen if the user chooses to exit data entry.
    From here doctors can open and confirm appointments.
    Book holidays and non-patient time.
    View their timetable on a given week.
    Cancel appointments.
    Logout.
    """
    while True:
        print("--------------------------------------------")
        print("\t Doctor Main Menu")
        print("--------------------------------------------")
        print("Welcome Dr. " + gp_full_name)
        print("Choose [1] to open today's appointments")
        print("Choose [2] to confirm pending appointments")
        print("Choose [3] to add non-patient time (including holidays)")
        print("Choose [4] to view your timetable")
        print("Choose [5] to cancel appointments")
        print("Choose [0] to logout")
        option = input("Please select an option: ")
        if option == "1":
            open_appointment(gp_email)
        elif option == "2":
            confirm_appointments(gp_email)
        elif option == "3":
            add_non_patient_time(gp_email)
        elif option == "4":
            print_timetable(gp_email)
        elif option == "5":
            clearhours(gp_email)
        elif option == "0":
            print("Logging out.....")
            print("********************************************")
            break
        else:
            print("\n\t< Invalid option chosen. Please try again >\n")
        print("********************************************")
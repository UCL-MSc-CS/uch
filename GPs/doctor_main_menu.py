from GPs.clear_hours import clearhours
from GPs.print_timetable import print_timetable
from GPs.add_non_patient_time import add_non_patient_time
from GPs.confirm_appointments import confirm_appointments
from GPs.open_appointment import open_appointment

def doctor_main_menu(dremail, drname):
    while True:
        print("--------------------------------------------")
        print("\t Doctor Main Menu")
        print("--------------------------------------------")
        print("Welcome Dr. " + drname)
        print("Choose [1] to open today's appointments")
        print("Choose [2] to confirm pending appointments")
        print("Choose [3] to add non-patient time (including holidays)")
        print("Choose [4] to view your timetable")
        print("Choose [5] to cancel appointments")
        print("Choose [0] to logout")
        option = input(":")
        if option == "1":
            open_appointment(dremail)
        elif option == "2":
            confirm_appointments(dremail)
        elif option == "3":
            add_non_patient_time(dremail)
        elif option == "4":
            print_timetable(dremail)
        elif option == "5":
            clearhours(dremail)
        elif option == "0":
            print("Logging out.....")
            print("********************************************")
            break
        else:
            print("\n\t<Invalid option chosen. Please try again>\n")
        print("********************************************")
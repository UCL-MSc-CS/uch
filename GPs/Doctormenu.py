from GPs.clearhours import clearhours
from GPs.printtimetable import printtimetable
from GPs.addnonpatienttime import addnonpatienttime
from GPs.confirmappointments import confirmappointments
from GPs.openAppointment import openappointment

def mainmenu(dremail,drname):
    while True:
        print("--------------------------------------------")
        print("\t Doctor Main Menu")
        print("--------------------------------------------")
        print("Welcome Dr. " + drname)
        print("Choose [1] to open appointment")
        print("Choose [2] to confirm pending appointments")
        print("Choose [3] to add non-patient time (including holidays)")
        print("Choose [4] to view your timetable")
        print("Choose [5] to cancel appointments")
        print("Choose [0] to exit")
        option = input(":")
        if option == "1":
            openappointment(dremail)
        elif option == "2":
            confirmappointments(dremail)
        elif option == "3":
            addnonpatienttime(dremail)
        elif option == "4":
            printtimetable(dremail)
        elif option == "5":
            clearhours(dremail)
        elif option == "0":
            print("Logging out.....")
            print("********************************************")
            break
        else:
            print("\t<Invalid option chosen. Please try again>")
        print("********************************************")
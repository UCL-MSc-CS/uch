from GPs.clearhours import clearhours
from GPs.printtimetable import printtimetable
from GPs.addnonpatienttime import addnonpatienttime
from GPs.confirmappointments import confirmappointments
from GPs.openAppointment import openappointment

def continueorexit():
    repeat = True
    while repeat:
        val = input("Do you want to remain logged in (Y/N) ?:")
        if val in ("Y","y"):
            repeat = False
            continueloop[0] = True
        elif val in ("N","n"):
            repeat = False
            continueloop[0] = False
        else:
            print("Please enter a valid response")

continueloop = [True]
#testing
def mainmenu(drdemail):
    doctoremail = drdemail

    #Todo get doctor details from query for the below print statement

    while continueloop[0]:
        print("choose [1] to open appointment")
        print("choose [2] to confirm appointments")
        print("choose [3] to add non-patient time (including holidays)")
        print("choose [4] to view your timetable")
        print("choose [5] to cancel appointments")
        option = input(":")
        if option == "1":
            openappointment(doctoremail)
        elif option == "2":
            confirmappointments(doctoremail)
        elif option == "3":
            addnonpatienttime(doctoremail)
        elif option == "4":
            printtimetable(doctoremail)
        elif option == "5":
            clearhours(doctoremail)
        else:
            print("Invalid option chosen. Try again")
        continueorexit()
        print("------------------------------------------------------------------------------------------------------")
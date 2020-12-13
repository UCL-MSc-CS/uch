from GPs.appointmentnotes import appointmentnotes
from GPs.patienthistory import patienthistory
from GPs.prescription import prescription
import timetablefunctions as db
from datetime import datetime
import usefulfunctions as uf

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformat = dateformatstring + " " + timeformatstring


def openappointment(doctoremail):

    appointmentid = printtodayappointments(doctoremail)
    if appointmentid:
        while True:
            print("--------------------------------------------")
            print("\t Appointment ID: " + str(appointmentid))
            print("--------------------------------------------")
            print("choose [1] for Appointment notes")
            print("choose [2] for Patient history")
            print("choose [3] for editing Patient prescription")
            print("choose [4] for selecting a different appointment")
            print("choose [5] to exit this appointment")
            option = input(":")
            if option == "1":
                print("\n Opening your notes for this appointment in a separate window.... \n")
                appointmentnotes(doctoremail,appointmentid)
            elif option == "2":
                patienthistory(doctoremail,appointmentid)
            elif option == "3":
                print("\n Opening the prescription editor in a separate window... \n")
                prescription(doctoremail,appointmentid)
            elif option == "4":
                print("\n Switching appointments... \n")
                openappointment(doctoremail)
                break
            elif option == "5":
                print("\n Returning to main menu...... \n")
                break
            else:
                print("\nInvalid option chosen. Try again\n")

            print("------------------------------------------------------------------------------------------------------")


def printtodayappointments(doctoremail):
    # Todo disallow user to 'stay within appointment' if they have entered wrong invalid id
    day = datetime.today()

    print("\n--------------------\n" + datetime.strftime(day, "%A %d %b %Y") + "\n--------------------")
    appointments = db.TodayAppointments(doctoremail)
    appointmentids = []
    print("id" + "\t" + "reason")
    for appointment in appointments:
        appointmentids.append(appointment[4])
        reason = appointment[0]
        start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
        end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
        patientemail = appointment[3]
        appointmentid = str(appointment[4])
        print(appointmentid + "\t" + reason + "\t" + start + "-" + end + "\t" + patientemail)
    continueSelecting = True
    while continueSelecting:
        id = input("Please enter the appointment id you wish to open: \n")

        try:
            idNum = int(id)
            if idNum in appointmentids:
                print("Opening appointment id: " + id)
                # todo connect current appointment options
                return idNum
            else:
                print("You entered an invalid id number!")
        except:
            print("That is not a integer value")

        choosecontinue = input("Would you like to try again y/n ? :")
        if choosecontinue.lower() == 'y':
            continueSelecting = True
        elif choosecontinue.lower() == 'n':
            print("Returning to main menu......")
            continueSelecting = False
        else:
            print("Invalid option chosen, exiting today's appointments....")
            continueSelecting = False
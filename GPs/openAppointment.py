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
    #ToDO query for all today's confirmed apointments, display them to the doctor and allow to select one from the id
    appointmentid = printtodayappointments(doctoremail)
    continueloop = True
    while continueloop:
        print("choose [1] for Appointment notes")
        print("choose [2] for Patient history")
        print("choose [3] for editing Patient prescription")
        print("choose [4] for selecting a different appointment")
        option = input(":")
        if option == "1":
            appointmentnotes(doctoremail,appointmentid)
        elif option == "2":
            patienthistory(doctoremail,appointmentid)
        elif option == "3":
            prescription(doctoremail,appointmentid)
        elif option == "4":
            openappointment(doctoremail)
            break
        else:
            print("Invalid option chosen. Try again")

        while True:
            val = input("Would you like to stay within the appointment (Y/N) ?:")
            if val in ("Y", "y"):
                break
            elif val in ("N", "n"):
                continueloop = False
                break
            else:
                print("Please enter a valid response")
        print("------------------------------------------------------------------------------------------------------")


def printtodayappointments(doctoremail):
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
        if choosecontinue == 'y':
            continueSelecting = True
        elif choosecontinue == 'n':
            continueSelecting = False
        else:
            print("Invalid option chosen, exiting today's appointments....")
            continueSelecting = False
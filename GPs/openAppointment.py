import timetablefunctions as db
from datetime import datetime
import usefulfunctions as uf


dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformat = dateformatstring + " " + timeformatstring

def openappointment(doctoremail):
    #ToDO query for all today's confirmed apointments, display them to the doctor and allow to select one from the id
    printtodayappointments(doctoremail)

    pass


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
                print("Opening appointment id: " + id + " ...")
                # todo connect current appointment options
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




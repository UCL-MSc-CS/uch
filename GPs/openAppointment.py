from GPs.appointmentnotes import appointmentnotes
from GPs.patienthistory import patienthistory
from GPs.prescription import prescription

continueloop = [True]

def continueorexit():
    repeat = True
    while repeat:
        val = input("Continue the appointment (Y/N) ?:")
        if val in ("Y","y"):
            repeat = False
            continueloop[0] = True
        elif val in ("N","n"):
            repeat = False
            continueloop[0] = False
        else:
            print("Please enter a valid response")

def openappointment(doctoremail):
    #ToDO query for all today's confirmed apointments, display them to the doctor and allow to select one from the id

    while continueloop:
        print("choose [1] for Appointment notes")
        print("choose [2] for Patient history")
        print("choose [3] for editing Patient prescription")
        option = input(":")
        if option == "1":
            appointmentnotes(doctoremail,appointmentid)
        elif option == "2":
            patienthistory(doctoremail,appointmentid)
        elif option == "3":
            prescription(doctoremail,appointmentid)
        else:
            print("Invalid option chosen. Try again")
        continueorexit()
        print("------------------------------------------------------------------------------------------------------")

def printtodayappointments(day,doctoremail):
    print("\n--------------------\n" + datetime.strftime(day, "%A %d %b %Y") + "\n--------------------")
    datestring = datetime.strftime(day, dateformatstring)
    appointments = db.timetableblock(doctoremail, datestring)
    print("id" + "\t" + "reason")
    for appointment in appointments:
        reason = appointment[0]
        start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
        end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
        patientemail = appointment[3]
        appointmentid = str(appointment[4])
        print(appointmentid + "\t" + reason + "\t" + start + "-" + end + "\t" + patientemail)
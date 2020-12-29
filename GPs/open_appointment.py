from GPs.appointment_notes import appointment_notes
from GPs.patient_history import patient_history
from GPs.prescription import prescription
import timetable_functions as db
from datetime import datetime
import useful_functions as uf
from patient_summary import PatientSummary

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformat = dateformatstring + " " + timeformatstring


def open_appointment(doctoremail):

    appointmentid, nhsNumber = print_todays_appointments(doctoremail)
    if appointmentid:
        while True:
            print("--------------------------------------------")
            print("\t Appointment ID: " + str(appointmentid))
            print("--------------------------------------------")
            print("Choose [1] for Appointment notes")
            print("Choose [2] for Patient history")
            print("Choose [3] for editing Patient prescription")
            print("Choose [4] for selecting a different appointment")
            print("Choose [5] to download a patient summary")
            print("Choose [0] to exit this appointment")
            option = input(":")
            if option == "1":
                print("\n Opening your notes for this appointment in a separate window.... \n")
                appointment_notes(appointmentid)
            elif option == "2":
                patient_history(nhsNumber)
            elif option == "3":
                print("\n Opening the prescription editor in a separate window... \n")
                prescription(doctoremail,appointmentid, nhsNumber)
            elif option == "4":
                print("\n Switching appointments... \n")
                open_appointment(doctoremail)
                break
            elif option == "5":
                print("\n Downloading patient summary... \n")
                PatientSummary(int(nhsNumber))
            elif option == "0":
                print("\n Returning to main menu...... \n")
                break
            else:
                print("\n\t<Invalid option chosen. Try again>\n")

            print("********************************************")


def print_todays_appointments(doctoremail):
    day = datetime.today()

    print("--------------------------------------------")
    print(datetime.strftime(day, "%A %d %b %Y"))
    print("--------------------------------------------")
    appointments = db.todays_appointments(doctoremail)
    if not appointments:
        print("\n\t<There are no confirmed appointments available on this day.>")
        print("\t<Consider confirming some pending appointments if you have any>\n")
        return "",""
    appointmentids = []
    print("id" + "\t" + "reason" + "\t\t" + "time" + "\t\t" + "nhs number" + "\t" + "patient name")
    for appointment in appointments:
        appointmentids.append(appointment[4])
        reason = appointment[0]
        start = datetime.strftime(uf.unix_to_regular_time(appointment[1]), timeformatstring)
        end = datetime.strftime(uf.unix_to_regular_time(appointment[2]), timeformatstring)
        nhsNumber = str(appointment[3]).zfill(10)
        appointmentid = str(appointment[4])
        patient_details = db.get_patient_info(appointmentid)
        full_name = patient_details[2] + " " + patient_details[3]
        print(appointmentid+"\t"+reason+"\t"+start+"-"+end+"\t"+nhsNumber+"\t"+full_name)
    while True:
        id = input("Please enter the appointment id you wish to open (press 'x' to exit): \n")

        if id == 'x':
            return "",""

        try:
            idNum = int(id)
            if idNum in appointmentids:
                print("Opening appointment id: " + id)
                for appointment in appointments:
                    if idNum == appointment[4]:
                        chosenNhsNumber = appointment[3]
                return idNum, chosenNhsNumber
            else:
                print("\n\t<You entered an invalid id number!>\n")
        except ValueError:
            print("\n\t<That is not a integer value>\n")

        choosecontinue = input("Would you like to try again y/n ? :")
        if choosecontinue.lower() == 'y':
            pass
        elif choosecontinue.lower() == 'n':
            print("Returning to main menu......")
            return "",""
        else:
            print("\n\t<Invalid option chosen, exiting today's appointments....>\n")
            return "",""
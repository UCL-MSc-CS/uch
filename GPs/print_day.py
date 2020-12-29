from datetime import datetime
import useful_functions as uf
import timetable_functions as db

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"


def printday(day,doctoremail):
    print("--------------------------------------------")
    print(datetime.strftime(day, "%A %d %b %Y"))
    print("--------------------------------------------")
    datestring = datetime.strftime(day, dateformatstring)
    appointments = db.timetableblock(doctoremail, datestring)
    print("id" + "\t" + "reason")
    for appointment in appointments:
        appointmentid = str(appointment[4])
        reason = appointment[0]
        start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
        end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
        if reason == "Appointment":
            patient_details = db.getPatientInfo(appointmentid)
            patient_email = patient_details[1]
            full_name = patient_details[2] + " " + patient_details[3]
            nhsNumber = str(appointment[3]).zfill(10)
            print(appointmentid+"\t"+reason+"\t"+start+"-"+end+"\t"+nhsNumber+"\t"+patient_email+"\t"+full_name)
        else:
            print(appointmentid+"\t"+reason+"\t"+start+"-"+end)
    print("\n")
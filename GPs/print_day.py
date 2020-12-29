from datetime import datetime
import useful_functions as uf
import timetable_functions as db

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"


def print_day(day, doctoremail):
    print("--------------------------------------------")
    print(datetime.strftime(day, "%A %d %b %Y"))
    print("--------------------------------------------")
    datestring = datetime.strftime(day, DATE_FORMAT_STRING)
    appointments = db.timetable_block(doctoremail, datestring)
    print("id" + "\t" + "reason")
    for appointment in appointments:
        appointmentid = str(appointment[4])
        reason = appointment[0]
        start = datetime.strftime(uf.unix_to_regular_time(appointment[1]), TIME_FORMAT_STRING)
        end = datetime.strftime(uf.unix_to_regular_time(appointment[2]), TIME_FORMAT_STRING)
        if reason == "Appointment":
            patient_details = db.get_patient_info(appointmentid)
            patient_email = patient_details[1]
            full_name = patient_details[2] + " " + patient_details[3]
            nhsNumber = str(appointment[3]).zfill(10)
            print(appointmentid+"\t"+reason+"\t"+start+"-"+end+"\t"+nhsNumber+"\t"+patient_email+"\t"+full_name)
        else:
            print(appointmentid+"\t"+reason+"\t"+start+"-"+end)
    print("\n")
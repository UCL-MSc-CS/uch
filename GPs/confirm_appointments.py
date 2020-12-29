from datetime import datetime
import useful_functions as uf
import timetable_functions as db

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"

def confirm_appointments(doctoremail):
    while True:
        confirmdate = uf.validate_date("Please enter a date for confirming appointments")
        if confirmdate == 'exit':
            return
        if confirmdate.date() >= datetime.today().date():
            break
        else:
            print("\n\t< You cannot confirm appointments in the past, please try again >\n")
    datestring = datetime.strftime(confirmdate, DATE_FORMAT_STRING)
    continueconfirming = True
    while continueconfirming:
        pendingappointments = db.get_all_pending_appointments(doctoremail, datestring)

        pendingids = []
        for appointment in pendingappointments:
            pendingids.append(appointment[4])

        if not pendingids:
            print("\n\t< There are no pending appointments to confirm on " + datestring + " >\n")
            break

        print("--------------------------------------------")
        print(datetime.strftime(confirmdate, "%A %d %b %Y"))
        print("--------------------------------------------")
        print("id" + "\t" + "reason" + "\t\t" + "time" + "\t\t" + "nhs number" + "\t" + "patient name")
        for appointment in pendingappointments:
            reason = appointment[0]
            start = datetime.strftime(uf.unix_to_regular_time(appointment[1]), TIME_FORMAT_STRING)
            end = datetime.strftime(uf.unix_to_regular_time(appointment[2]), TIME_FORMAT_STRING)
            nhsNumber = str(appointment[3]).zfill(10)
            appointmentid = str(appointment[4])
            patient_details = db.get_patient_info(appointmentid)
            full_name = patient_details[2] + " " + patient_details[3]
            status = db.check_slot_available(datestring, start, end, [doctoremail])
            if status[0] != 'unavailable':
                print(appointmentid+"\t"+reason+"\t"+start+"-"+end+"\t"+nhsNumber+"\t"+full_name)
            else:
                db.decline_appointment(appointmentid)
                pendingids.remove(appointment[4])

        id = input("Please enter the id of an appointment you would like to confirm (type 'x' to exit): ")
        try:
            if id.lower() == 'x':
                break
            idnum = int(id)
            if idnum in pendingids:
                db.accept_appointment(idnum)
                print("Accepted appointment with id " + id)
            else:
                print("\n\t< You entered an invalid id number! >\n")
        except ValueError:
            print("\n\t< That is not a integer value >\n")

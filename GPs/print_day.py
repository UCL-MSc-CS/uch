from datetime import datetime
import useful_functions as uf
import timetable_functions as db

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"

def print_day(day, gp_email):
    """
    For a given day print out all appointments.

    Be wary: this will only print out patient appointments that are confirmed/accepted.
    Will not print out pending/declined patient appointments as these are not considered to have been added to the
    GPs timetable.
    """
    print("--------------------------------------------")
    print(datetime.strftime(day, "%A %d %b %Y"))
    print("--------------------------------------------")
    date_string = datetime.strftime(day, DATE_FORMAT_STRING)
    appointments = db.timetable_block(gp_email, date_string)
    print("id" + "\t" + "reason")
    for appointment in appointments:
        appointment_id = str(appointment[4])
        reason = appointment[0]
        start = datetime.strftime(uf.unix_to_regular_time(appointment[1]), TIME_FORMAT_STRING)
        end = datetime.strftime(uf.unix_to_regular_time(appointment[2]), TIME_FORMAT_STRING)
        if reason == "Appointment":
            # Prints extra details if the appointment is a patient appointment.
            patient_details = db.get_patient_info(appointment_id)
            patient_email = patient_details[1]
            full_name = patient_details[2] + " " + patient_details[3]
            nhs_number = str(appointment[3]).zfill(10)
            print(appointment_id+"\t"+reason+"\t"+start+"-"+end+"\t"+nhs_number+"\t"+patient_email+"\t"+full_name)
        else:
            print(appointment_id+"\t"+reason+"\t"+start+"-"+end)
    print("\n")
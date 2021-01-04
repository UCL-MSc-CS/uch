from datetime import datetime
import useful_functions as uf
import timetable_functions as db

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"

def confirm_appointments(doctoremail):
    """
    This function is called when GPs want to confirm pending appointments that patients have booked.

    Will not allow confirming of appointments in the past.
    Auto-exits if the user enters a day there are no pending appointments booked on.
    Prints out all the pending appointments on that day for a user to select from.
    """
    # First checking for valid date entry
    while True:
        confirmdate = uf.validate_date("Please enter a date for confirming appointments")
        if confirmdate == 'exit':
            return
        if confirmdate.date() >= datetime.today().date():
            break
        else:
            print("\n\t< You cannot confirm appointments in the past, please try again >\n")
    date_string = datetime.strftime(confirmdate, DATE_FORMAT_STRING)

    # If date is valid continue to the confirming appointments stage.
    while True:
        # Gets all the pending appointments from the db.
        pending_appointments = db.get_all_pending_appointments(doctoremail, date_string)

        # Store all their ids in an array
        pending_ids = []
        for appointment in pending_appointments:
            pending_ids.append(appointment[4])

        # If no pending appointments on that day auto-exit
        if not pending_ids:
            print("\n\t< There are no pending appointments to confirm on " + date_string + " >\n")
            break

        # Print all the extracted pending appointments
        print("--------------------------------------------")
        print(datetime.strftime(confirmdate, "%A %d %b %Y"))
        print("--------------------------------------------")
        print("id" + "\t" + "reason" + "\t\t" + "time" + "\t\t" + "nhs number" + "\t" + "patient name")
        for appointment in pending_appointments:
            reason = appointment[0]
            start = datetime.strftime(uf.unix_to_regular_time(appointment[1]), TIME_FORMAT_STRING)
            end = datetime.strftime(uf.unix_to_regular_time(appointment[2]), TIME_FORMAT_STRING)
            nhs_number = str(appointment[3]).zfill(10)
            appointment_id = str(appointment[4])
            patient_details = db.get_patient_info(appointment_id)
            full_name = patient_details[2] + " " + patient_details[3]
            status = db.check_slot_available(date_string, start, end, [doctoremail])
            if status[0] == 'unavailable':
                # Auto-decline appointments that the GP is unavailable for
                db.decline_appointment(appointment_id)
                pending_ids.remove(appointment[4])
            else:
                # Only print out that appointment if the user is available during that time
                print(appointment_id+"\t"+reason+"\t"+start+"-"+end+"\t"+nhs_number+"\t"+full_name)

        # Ask user to enter an ID from those that are displayed.
        chosen_appointment_id = input("Please enter the id of an appointment you would like to confirm (type 'x' to exit): ")
        try:
            if chosen_appointment_id.lower() == 'x':
                # If user wishes to leave at this point let them.
                break
            idnum = int(chosen_appointment_id)
            if idnum in pending_ids:
                db.accept_appointment(idnum)
                print("Accepted appointment with id " + chosen_appointment_id)
            else:
                print("\n\t< You entered an invalid id number! >\n")
        except ValueError:
            print("\n\t< That is not a integer value >\n")

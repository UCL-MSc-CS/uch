import useful_functions as uf
from GPs.open_appointment import open_appointment

def print_past_appointments(doctoremail):
    """
    Prints all confirmed appointments on a given date.

    Called when the user chooses to "Open an appointment" from the main menu.
    Remember that this will only show appointments that have been "confirmed" by the GP and not "pending" appointments.
    The user can select an appointment from the list of printed out appointments.
    Will return the Appointment ID and the nhsNumber of the patient that appointment is booked by.
    """

    day = uf.validate_date("Please enter the date of the appointment: ")
    

    print("--------------------------------------------")
    print(datetime.strftime(day, "%A %d %b %Y"))
    print("--------------------------------------------")

    appointments = db.todays_appointments(doctoremail)
    if not appointments:
        # Auto-return to main menu if there are no confirmed appointments on the selected date
        print("\n\t< There are no confirmed appointments available on this day. >")
        print("\t< Consider confirming some pending appointments if you have any >\n")
        return "", ""

    # Print out the confirmed appointments. Also extract their ids to check if user input is valid.
    appointment_ids = []
    print("id" + "\t" + "reason" + "\t\t" + "time" + "\t\t" + "nhs number" + "\t" + "patient name")
    for appointment in appointments:
        appointment_ids.append(appointment[4])
        reason = appointment[0]
        start = datetime.strftime(uf.unix_to_regular_time(appointment[1]), TIME_FORMAT_STRING)
        end = datetime.strftime(uf.unix_to_regular_time(appointment[2]), TIME_FORMAT_STRING)
        nhs_number = str(appointment[3]).zfill(10)
        appointment_id = str(appointment[4])
        patient_details = db.get_patient_info(appointment_id)
        full_name = patient_details[2] + " " + patient_details[3]
        print(appointment_id + "\t" + reason + "\t" + start + "-" + end + "\t" + nhs_number + "\t" + full_name)

    # Take user input (the Appointment ID they wish to open).
    # Validate that it is in your list of ids.
    while True:
        chosen_id = input("Please enter the appointment id you wish to open (press 'x' to exit): \n")

        if chosen_id == 'x':
            # If user wishes to exit, return nothing.
            return "", ""

        try:
            chosen_id_integer = int(chosen_id)
            if chosen_id_integer in appointment_ids:
                print("Opening appointment id: " + chosen_id)
                for appointment in appointments:
                    if chosen_id_integer == appointment[4]:
                        chosen_nhs_number = appointment[3]
                return chosen_id_integer, chosen_nhs_number
            else:
                print("\n\t< You entered an invalid id number! >\n")
        except ValueError:
            print("\n\t< That is not a integer value >\n")

        choosecontinue = input("Would you like to try again y/n ? :")
        if choosecontinue.lower() == 'y':
            pass
        elif choosecontinue.lower() == 'n':
            print("Returning to main menu......")
            return "", ""
        else:
            print("\n\t< Invalid option chosen, exiting today's appointments.... >\n")
            return "", ""

def open_past_appointments(gp_email):
    appointment_id, nhs_num = print_past_appointments(gp_email)
    if appointment_id:
        
        
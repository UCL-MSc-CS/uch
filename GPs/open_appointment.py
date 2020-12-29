from GPs.appointment_notes import appointment_notes
from GPs.patient_history import patient_history
from GPs.prescription import prescription
import timetable_functions as db
from datetime import datetime
import useful_functions as uf
from patient_summary import patient_summary

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"
DATE_TIME_FORMAT = DATE_FORMAT_STRING + " " + TIME_FORMAT_STRING

def open_appointment(gp_email):
    """
    Main menu once a selected appointment has been opened.

    From here the GP can add their notes, build a prescription and check on the patients medical history through various
    means.
    """

    # Starts by printing all the appointments available for the GP to open.
    appointment_id, nhs_number = print_todays_appointments(gp_email)

    # if the user has successfully selected a valid appointment, continue.
    if appointment_id:
        while True:
            print("--------------------------------------------")
            print("\t Appointment ID: " + str(appointment_id))
            print("--------------------------------------------")
            print("Choose [1] for Appointment notes")
            print("Choose [2] for Patient history")
            print("Choose [3] for editing Patient prescription")
            print("Choose [4] for selecting a different appointment")
            print("Choose [5] to download a patient summary")
            print("Choose [0] to exit this appointment")
            option = input("Please select an option: ")
            if option == "1":
                print("\n Opening your notes for this appointment in a separate window.... \n")
                appointment_notes(appointment_id)
            elif option == "2":
                patient_history(nhs_number)
            elif option == "3":
                print("\n Opening the prescription editor in a separate window... \n")
                prescription(gp_email, appointment_id, nhs_number)
            elif option == "4":
                print("\n Switching appointments... \n")
                open_appointment(gp_email)
                break
            elif option == "5":
                print("\n Downloading patient summary... \n")
                patient_summary(int(nhs_number))
            elif option == "0":
                print("\n Returning to main menu...... \n")
                break
            else:
                print("\n\t< Invalid option chosen. Try again >\n")

            print("********************************************")

def print_todays_appointments(doctoremail):
    """
    Prints all confirmed appointments on a given date.

    Called when the user chooses to "Open an appointment" from the main menu.
    Remember that this will only show appointments that have been "confirmed" by the GP and not "pending" appointments.
    The user can select an appointment from the list of printed out appointments.
    Will return the Appointment ID and the nhsNumber of the patient that appointment is booked by.
    """

    day = datetime.today()

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

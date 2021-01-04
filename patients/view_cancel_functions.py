import sqlite3 as sql
import logging
from datetime import datetime
import pandas as pd
import patients.patient_functions as pf

"""
This module contains functions for users to view and cancel their appointments.

Error classes contain exception handling for user input in the functions.
Functions allow patients to view all their appointments, delete appointments from the database
and check an appointment exists in the database.
"""


class Error(Exception):
    """Error exception base class."""
    pass


class AppNotExistError(Error):
    """Raised when the appointment ID entered by user does not exist."""
    pass


class AppointmentPassedError(Error):
    """Raised when the appointment time has already passed, therefore cannot be cancelled."""
    pass


def view_appointments(nhs_number):
    """
    Displays all appointments for the patient which are pending, accepted or declined.

    Prints pandas dataframe of appointment information including appointment ID,
    date and time, doctor name and appointment status.

    Parameters:
        nhs_number (int): Patient's nhs number.
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute(""" SELECT A.appointmentID, A.start, P.lastName, A.appointmentStatus FROM Appointment A 
    LEFT JOIN GP P USING (gpEmail) WHERE nhsNumber =? ORDER BY A.appointmentID ASC""", [nhs_number])
    logging.info('Viewing all appointments for patient NHS number {}'.format(nhs_number))
    appointments = c.fetchall()
    # if appointment list empty, patient told they have none booked and returned to main menu
    if not appointments:
        print("\nYou currently have no appointments booked"
              "\n")
        return 0
    else:
        appointment_id = []
        date = []
        gp = []
        status = []
        for appoint in appointments:
            appointment_id.append(appoint[0])
            dt = appoint[1]
            dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
            date.append(dt)
            gp.append('Dr ' + appoint[2])
            status.append(appoint[3])
        new_status = []
        # reassign names for user-friendly display to patient
        for item in status:
            if item == 'Accepted':
                item = '    Booking Confirmed'
                new_status.append(item)
            elif item == 'Pending':
                item = '    Pending Approval'
                new_status.append(item)
            elif item == 'Declined':
                item = '    Appointment Declined'
                new_status.append(item)
        # create pandas dataframe to display appointment details
        data = pd.DataFrame({'Appointment ID': appointment_id, 'Date and Time': date,
                             'Doctor': gp, 'Status': new_status})
        print("********************************************\n")
        print(data.to_string(columns=['Appointment ID', 'Date and Time', 'Doctor',
                                      'Status'], index=False))
        print("\n********************************************")


def delete_appointment(cancel):
    """
    Deletes an appointment from the database.

    Uses appointment ID entered by patient to delete the appointment row from the 'Appointment' table,
    also deletes the related prescription row in the 'Prescription' table with the same appointment ID.

    Parameters:
        cancel (int): Appointment ID input by the patient.
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
    logging.info('Appointment ID {} deleted from Appointment table'.format(cancel))
    c.execute("DELETE FROM Prescription WHERE appointmentID =?", [cancel])
    logging.info('Appointment ID {} deleted from Prescription table'.format(cancel))
    connection.commit()
    print("You have cancelled appointment ID {}".format(cancel))


def check_app_id(nhs_number):
    """
    Checks the appointment ID exists and if the time of the appointment has already passed.

    Patient can enter the appointment ID they would like to cancel, exception handling checks if
    it exists in the database, then checks if the time and date of the appointment has passed, preventing cancellation.

    Parameters:
        nhs_number (int): Patient's nhs number.
    Returns:
        cancel (int): Appointment ID to cancel.
        or 0 (int): To return to the main menu.
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            cancel = int(input("Please enter the appointment ID you would like to cancel "
                               "(or 0 to exit to the patient menu): "))
            if cancel == 0:
                return 0
            else:
                c.execute("SELECT appointmentID FROM Appointment "
                          "WHERE nhsNumber =?", [nhs_number])
                app_ids = c.fetchall()
                id_list = []
                for app_id in app_ids:
                    id_list.append(app_id[0])
                # if the appointment id chosen does not exist in the database, exception raised
                if cancel not in id_list:
                    raise AppNotExistError
                c.execute("SELECT start FROM Appointment "
                          "WHERE nhsNumber =? and appointmentID =?", [nhs_number, cancel])
                app_time = c.fetchone()
                s_time = app_time[0]
                start_time = pf.to_regular_time(s_time)
                current = datetime.now()
                # if the appointment start time is in the past, exception raised
                if start_time < current:
                    raise AppointmentPassedError
                else:
                    return cancel
        except AppNotExistError:
            print("\n\t< This appointment does not exist, please try again >"
                  "\n")
        except AppointmentPassedError:
            print("\n\t< This appointment time has already passed and cannot be cancelled, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please enter a number >"
                  "\n")


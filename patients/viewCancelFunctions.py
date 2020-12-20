import sqlite3 as sql
from datetime import time as x, date as xyz, datetime, timedelta
import time
import pandas as pd
import patients.patientFunctions as pf


class Error(Exception):
    """Error exception class"""
    pass


class AppNotExist(Error):
    """Raised when appointmentID entered by user does not exist"""
    pass


def view_appointments(nhs_number):
    """ Displays all appointments for that user which are pending, accepted or declined
    Returns: pandas dataframe of appointment information including appointment ID, date and time, Dr name and status
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute(""" SELECT A.appointmentID, A.start, P.lastname, A.appointmentStatus FROM Appointment A 
    LEFT JOIN GP P USING (gpEmail) WHERE nhsNumber =? ORDER BY A.appointmentID ASC""", [nhs_number])
    appointments = c.fetchall()
    if not appointments:
        print("\nYou currently have no appointments"
              "\n")
        pf.return_to_main()
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
        for item in status:
            if item == 'Accepted':
                item = 'Booking Confirmed'
                new_status.append(item)
            elif item == 'Pending':
                item = 'Pending Approval'
                new_status.append(item)
            elif item == 'Declined':
                item = 'Appointment Declined'
                new_status.append(item)

        data = pd.DataFrame({'Appointment ID': appointment_id, 'Date and Time': date,
                             'Doctor': gp, 'Status': new_status})
        print("\n********************************************")
        print(data.to_string(columns=['Appointment ID', 'Date and Time', 'Doctor',
                                      'Status'], index=False))
        print("********************************************\n")


def delete_appointment(cancel):
    """ Deletes a chosen appointment from the database using appointment ID"""
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
    connection.commit()
    print("You have cancelled appointment ID {}".format(cancel))


def check_app_id(nhs_number):
    """ Checks the appointment ID entered by the user exists in the database
    :return: appointment ID to cancel (integer) """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            cancel = int(input("Please enter the appointment ID you would like to cancel: "))
            c.execute("SELECT appointmentID FROM Appointment "
                      "WHERE nhsNumber =?", [nhs_number])
            app_ids = c.fetchall()
            id_list = []
            for app_id in app_ids:
                id_list.append(app_id[0])
            if cancel not in id_list:
                raise AppNotExist
            else:
                return cancel
        except AppNotExist:
            print("\n\t< This appointment does not exist, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please enter a number >"
                  "\n")


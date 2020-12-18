import sqlite3 as sql
from datetime import time as x, date as xyz, datetime, timedelta
import time
import pandas as pd
import patients.patientFunctions as pf

class Error(Exception):
    """Error exception class"""
    pass

class appNotExist(Error):
    """Raised when appointmentID entered by user does not exist"""
    pass

def viewAppointments(nhsNumber):
    """ Displays all appointments for that user which are pending or confirmed
    Returns: pandas dataframe
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("""SELECT A.appointmentID, A.start, P.lastname, A.appointmentStatus FROM Appointment A, GP P 
    WHERE nhsNumber =? ORDER BY A.appointmentID ASC""", [nhsNumber])
    appointments = c.fetchall()
    if not appointments:
        print("\nYou currently have no appointments"
              "\n")
        pf.return_to_main()
    else:
        appointmentID = []
        date = []
        gp = []
        status = []
        for appoint in appointments:
            appointmentID.append(appoint[0])
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

        data = pd.DataFrame({'Appointment ID': appointmentID, 'Date and Time': date,
            'Doctor': gp, 'Status': new_status})
        print("********************************************")
        print(data.to_string(columns=['Appointment ID', 'Date and Time', 'Doctor',
                                      'Status'], index=False))
        print("********************************************")


def deleteAppointment(cancel):
    """ Deletes a chosen appointment from the database"""
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
    connection.commit()
    print("You have cancelled your appointment")


def checkAppID(nhsNumber):
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            cancel = int(input("Please enter the appointment ID you would like to cancel: "))
            c.execute("SELECT appointmentID FROM Appointment "
                      "WHERE nhsNumber =?", [nhsNumber])
            appids = c.fetchall()
            for item in appids[0]:
                if item == cancel:
                    return cancel
                else:
                    raise appNotExist
        except appNotExist:
            print("\n\t< This appointment does not exist, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")


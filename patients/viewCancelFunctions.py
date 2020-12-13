import sqlite3 as sql
from datetime import time as x, date as xyz, datetime, timedelta
import time
import pandas as pd

def viewAppointments(nhsNumber):
    """ Displays all appointments for that user which are pending or confirmed
    Returns: pandas dataframe
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()

    # remove, switch to nhsNumber?
    c.execute("SELECT patientEmail FROM patientDetails "
              "WHERE nhsNumber =?",
              [nhsNumber])
    patientEmails = c.fetchall()
    patientEmail = patientEmails[0]

    c.execute("SELECT appointmentID, start, gpLastName, appointmentStatus FROM Appointment "
              "WHERE patientEmail =? ", [patientEmail])
    appointments = c.fetchall()
    appointmentID = []
    date = []
    gp = []
    status = []
    for appoint in appointments:
        appointmentID.append(appoint[0])
        dt = appoint[1]
        dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
        date.append(dt)
        gp.append(appoint[2])
        status.append(appoint[3])
    new_status = []
    for item in status:
        if item == 'Unavailable':
            item = 'Confirmed Booking'
            new_status.append(item)
        else:
            new_status.append(item)

    data = pd.DataFrame({'Appointment ID': appointmentID, 'Date and Time': date,
        'Doctor': gp, 'Status': new_status})
    print(data.to_string(columns=['Appointment ID', 'Date and Time', 'Doctor',
                                  'Status'], index=False))

def deleteAppointment(cancel):
    """ Deletes a chosen appointment from the database"""
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
    connection.commit()
    print("You have cancelled your appointment")
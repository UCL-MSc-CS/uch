import sqlite3 as sql
import pandas as pd
from datetime import time as x, date as xyz, datetime, timedelta
import time


def patientNotifications(nhsNumber):
    print("********************************************"
          "\nChoose [1] to view your pending appointments"
          "\nChoose [2] to view today's appointments"
          "\nChoose [0] to exit to the main menu"
          "\n********************************************")
    options = input("Please select an option: ")

    if options == '1':
        pendingAppointments(nhsNumber)
    if options == '2':
        todaysAppointments(nhsNumber)
    else:
        print("\n\t< This is not a valid option, please try again >"
              "\t")
        patientNotifications(nhsNumber)

    # confirmed appointments
    # rejected appointments
    # today's appointments
    pass

def pendingAppointments(nhsNumber):
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    print("********************************************"
          "\nThese are your pending appointments"
          "\nYou will receive confirmation by the doctor if they are approved shortly.")

    c.execute("SELECT appointmentID, start, gpLastName, appointmentStatus FROM Appointment "
              "WHERE nhsNumber =? and appointmentStatus = 'Pending' ", [nhsNumber])
    appointments = c.fetchall()
    # display message if empty
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

    data = pd.DataFrame({'Appointment ID': appointmentID, 'Date and Time': date,
                         'Doctor': gp, 'Status': status})
    print("********************************************")
    print(data.to_string(columns=['Appointment ID', 'Date and Time', 'Doctor',
                                  'Status'], index=False))
    print("********************************************")

def todaysAppointments(nhsNumber):
    pass


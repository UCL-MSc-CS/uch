import sqlite3 as sql
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
import calendar

def toregulartime(unixtimestamp):
    """ Converts unix timestamp to datetime object"""
    return datetime.utcfromtimestamp(int(unixtimestamp))


def tounixtime(dt):
    """ Converts datetime object to unix timestamp"""
    result = int(time.mktime(dt.timetuple()))
    return result


def toDateTimeObj(string):
    """ Converts date time string to datetime object"""
    dt_object = datetime.strptime(string, '%Y-%m-%d %H:%M')
    return dt_object


def toDateObjApp00(string):
    """ Converts date string to date object with time as 00:00:00"""
    dt_object = datetime.strptime(string, '%Y-%m-%d')
    return dt_object


def generateEndTime(date):
    """Generate end for displaying available appointment times
    Creates a unix time stamp with date string input by user, of date + 23:59:59"""
    year, month, day = map(int, date.split('-'))
    dt_str_obj = xyz(year, month, day)
    dt_time = x(23, 59, 59)
    dt_end = datetime.combine(dt_str_obj, dt_time)
    end = tounixtime(dt_end)
    return end

def chooseDr(dr_names):
    """ Allows user to select a gp from list obtained from database
        returns chosen dr email and last name in a list"""
    gp_list = []
    count = 1
    for dr in dr_names:
        print("[" + str(count) + "] Dr", dr[0] + ' ' + dr[1])
        count += 1
        gp_list.append(dr)

    dr_options = int(input("**********"
                           "\nPlease choose the doctor you would "
                           "like to book an appointment with: "))
    gp_chosen_email = gp_list[dr_options - 1][2]
    gp_chosen_name = gp_list[dr_options - 1][1]
    gpDetails = [gp_chosen_email, gp_chosen_name]
    return gpDetails

def checkIfAppBooked():
    # self.c.execute("SELECT start FROM Appointment WHERE appointmentStatus = 'Pending' and gpEmail =?",
    #                [gpDetails[0]])
    # booked_times = self.c.fetchall()
    # # for i in booked_times:
    # #     if start == i[0]:
    # #         print("Appointment already booked, please try again: ") etc etc...
    pass

def printCalendar(mm):
    print("----------")
    print(calendar.month(2021, mm))
    print("----------")
    day = input("Please select a day (as dd): ")
    date = "2021-{}-{}".format(mm, day)
    return date

def displayAvailable(start, end, gpDetails):
    connection = sql.connect('UCH.db')
    c = connection.cursor()

    c.execute("SELECT start, appointmentStatus FROM Appointment WHERE start >=? and end <? and gpEmail =?",
                   [start, end, gpDetails[0]])
    appointments = c.fetchall()
    times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
             "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
    if not appointments:
        for i in times:
            print(i + " available")
    else:
        dict_time_status = {}
        for items in appointments:
            ts = toregulartime(items[0])
            string_time = ts.strftime("%H:%M")
            dict_time_status[string_time] = items[1]
        for time in times:
            if time in dict_time_status:
                print(time + ' ' + dict_time_status[time])
            else:
                print(time + ' available')

def chooseTime(start, gpDetails, patientEmail):
    connection = sql.connect('UCH.db')
    c = connection.cursor()

    end = start + (30 * 60)
    gpLastName = gpDetails[1]
    gpEmail = gpDetails[0]
    reason = 'Appointment'
    appointmentStatus = 'Pending'
    dateRequested = tounixtime(datetime.today())

    chosen = (gpEmail, gpLastName, patientEmail, start, end, reason, appointmentStatus,
              dateRequested, '', '', '', '', '', None, None)
    c.execute("INSERT INTO Appointment VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", chosen)
    connection.commit()

def viewAppointments(patientEmail):
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("SELECT appointmentID, start, gpLastName FROM Appointment "
                "WHERE patientEmail =? and appointmentStatus = 'Unavailable' ", [patientEmail])
    appointments = c.fetchall()

    for app in appointments:
        dt = app[1]
        dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
        print("Appointment ID: " + str(app[0]) + "\t" + "date and time: " + dt + "\t\t" + "with: Dr " + app[2])




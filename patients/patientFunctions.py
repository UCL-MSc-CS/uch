import sqlite3 as sql
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
import calendar
import pandas as pd


class Error(Exception):
    """Error exception class"""
    pass

class timeNotValid(Error):
    """Raised when time entered by user is not valid"""
    pass

class monthNotValid(Error):
    """Raised when month entered by user is not valid"""
    pass

class dayNotValid(Error):
    """Raised when day entered by user is not valid"""
    pass

class timeBooked(Error):
    """Raised when appointment is not available to book"""
    pass

class dateAfterCurrent(Error):
    """Raised when date chosen is in the past"""
    pass


class drChoiceNotValid(Error):
    """Raised when choice of dr not valid"""
    pass


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
    """ Generates end timestamp
    :param date: date string from user input
    :return: unix time stamp with date + 23:59:59 time"""
    year, month, day = map(int, date.split('-'))
    dt_str_obj = xyz(year, month, day)
    dt_time = x(23, 59, 59)
    dt_end = datetime.combine(dt_str_obj, dt_time)
    end = tounixtime(dt_end)
    return end


def chooseDr(dr_names):
    """ Allows user to select a gp from list obtained from database
        returns chosen dr email and last name in a list
        """
    gp_list = []
    counts = []
    count = 1
    for dr in dr_names:
        print("[" + str(count) + "] Dr", dr[0] + ' ' + dr[1])
        count += 1
        gp_list.append(dr)
        counts.append(count - 1)
    while True:
        try:
            dr_options = int(input("********************************************"
                                   "\nPlease choose the doctor you would "
                                   "like to book an appointment with: "))
            if dr_options not in counts:
                raise drChoiceNotValid
            else:
                gp_chosen_email = gp_list[dr_options - 1][2]
                gp_chosen_name = gp_list[dr_options - 1][1]
                gpDetails = [gp_chosen_email, gp_chosen_name]
                print("You have chosen Dr {}".format(gp_chosen_name))
                return gpDetails
        except drChoiceNotValid:
            print("\n\t< This is not a valid choice, please try again >"
                  "\n ")
        except ValueError:
            print("\n\t< This is not a valid choice, please try again >"
                  "\n ")


def chooseMonth():
    """ Checks month entered by user is valid:
        checks:
        if month an int
        if month between 1 to 12
        if month chosen is in the past
        :return:
        prints calendar for the month chosen
        month as string, padded with 0 if month a single number """
    currentMonth = datetime.now().month
    while True:
        try:
            mm = int(input("Please choose the month would you would like your appointment in 2021: "))
            if not 1 <= mm <= 12:
                raise monthNotValid
            else:
                print("----------")
                print(calendar.month(2021, mm))
                print("----------")
                month = '{:02}'.format(mm)
                return month
        except monthNotValid:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")


def chooseDate(month):
    """ Checks date chosen by user is in a valid form
        Checks: if input is an int
                if day entered is valid according to the month
                if date chosen is in the past
        :return: date string with days padded with 0 for single day number"""
    days_31 = ['01', '03', '05', '07', '08', '10', '12']
    days_30 = ['04', '06', '09', '11']
    days_28 = ['02']
    while True:
        try:
            day = int(input("Please choose a date in your chosen month (as D/DD): "))
            for mm in days_31:
                if mm == month:
                    if not 1 <= day <= 31:
                        raise dayNotValid
            for mm in days_30:
                if mm == month:
                    if not 1 <= day <= 30:
                        raise dayNotValid
            for mm in days_28:
                if mm == month:
                    if not 1 <= day <= 28:
                        raise dayNotValid
            else:
                date = "2021-{}-{:02}".format(str(month), day)
                date_obj = toDateObjApp00(date)
                current = datetime.now()
                if date_obj < current:
                    raise dateAfterCurrent
            return date
        except dayNotValid:
            print("\n\t< Invalid date entered, please enter a date in the correct format >"
                  "\n")
        except dateAfterCurrent:
            print("\n\t< This date has already passed, please choose another >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")


def generateStartTime(date):
    """ Generates a unix start time stamp from the date input from the user
    """
    start_obj = toDateObjApp00(date)
    start = tounixtime(start_obj)
    return start


def displayAvailable(start, end, gpDetails):
    """ Displays appointments from date and time chosen by user
    """
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
    return times

def timeMenu(date, times, gpDetails, nhsNumber):
    """ Displays menu for user to select a time, reserves appointment as 'Pending' in the database,
    or allows user to exit to main menu
    """
    print("********************************************"
          "\nChoose [1] to select a time"
          "\nChoose [0] to exit to the main menu "
          "\n********************************************")
    options = input("\nPlease select an option: ")
    if options == '1':
        time = chooseTime(date, times, gpDetails)
        start = createStart(date, time)
        insertAppointment(start, gpDetails, nhsNumber)
        print("You have requested to book an appointment on {} at {}, "
              "\nYou will receive confirmation of your appointment shortly!".format(date, time))
        returnToMain()
    elif options == '2':
        returnToMain()
    else:
        print("This is not a valid option, please try again")
        timeMenu(date, times, gpDetails, nhsNumber)

def chooseTime(date, times, gpDetails):
    """ Checks time entered by user is in valid form and present in the list of appointment times
        Checks if time entered by user has already been booked
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            time = input("Please choose a time from the available appointments (as HH:MM): ")
            start = createStart(date, time)
            c.execute("SELECT start FROM Appointment "
                      "WHERE gpEmail =? AND appointmentStatus IN ('Pending', 'Unavailable')",
                           [gpDetails[0]])
            booked_times = c.fetchall()
            for item in booked_times:
                if item[0] == start:
                    raise timeBooked
            if time not in times:
                raise timeNotValid
            else:
                return time
        except timeNotValid:
            print("\n\t< This is not a valid time option, please try again >"
                  "\n")
        except timeBooked:
            print("\n\t< This time is unavailable, please try again >"
                  "\n")


def createStart(date, time):
    """ Creates a unix timestamp from the chosen date and appointment start time by the user
    """
    day_str = date + ' ' + time
    dt_object = toDateTimeObj(day_str)
    start = tounixtime(dt_object)
    return start


def insertAppointment(start, gpDetails, nhsNumber):
    """ Inserts the appointment details into the database
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()

    end = start + (30 * 60)
    gpLastName = gpDetails[1]
    gpEmail = gpDetails[0]
    reason = 'Appointment'
    appointmentStatus = 'Pending'
    dateRequested = tounixtime(datetime.today())

    chosen = (gpEmail, gpLastName, nhsNumber, start, end, reason, appointmentStatus,
              dateRequested, '', '', '', '', '', None, None)
    c.execute("INSERT INTO Appointment VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", chosen)
    connection.commit()


def returnToMain():
    """Returns user to main patient menu when typing 'yes'
    If user types anything else, will exit the program with a goodbye message"""
    if input("Type [0] to return to the main menu: ").lower() == '0':
        pass
    else:
        print("Thank you for using the UCH e-health system! Goodbye for now!")
        exit()



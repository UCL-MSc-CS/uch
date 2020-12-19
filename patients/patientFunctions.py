import sqlite3 as sql
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
import calendar
import pandas as pd


class Error(Exception):
    """Error exception class"""
    pass


class TimeNotValid(Error):
    """Raised when time entered by user is not valid"""
    pass


class MonthNotValid(Error):
    """Raised when month entered by user is not valid"""
    pass


class MonthPassed(Error):
    """Raised when month entered by user is not valid"""
    pass


class YearPassed(Error):
    """Raised when year entered by user is not valid"""
    pass


class DayNotValid(Error):
    """Raised when day entered by user is not valid"""
    pass


class TimeBooked(Error):
    """Raised when appointment is not available to book"""
    pass


class DateAfterCurrent(Error):
    """Raised when date chosen is in the past"""
    pass


class LeapYear(Error):
    """Raised when date chosen in February is in a leap year"""
    pass


class DrChoiceNotValid(Error):
    """Raised when choice of dr not valid"""
    pass


class EmptyAnswer(Error):
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class InvalidAnswer(Error):
    def __init__(self, message="\n\t< This is not a valid answer, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


def to_regular_time(time_stamp):
    """ Converts unix timestamp to datetime object"""
    return datetime.utcfromtimestamp(int(time_stamp))


def to_unix_time(date_time):
    """ Converts datetime object to unix timestamp"""
    result = int(time.mktime(date_time.timetuple()))
    return result


def to_date_time_obj(string):
    """ Converts date time string to datetime object"""
    dt_object = datetime.strptime(string, '%Y-%m-%d %H:%M')
    return dt_object


def to_date_time_obj00(string):
    """ Converts date string to date object with time as 00:00:00"""
    dt_object = datetime.strptime(string, '%Y-%m-%d')
    return dt_object


def generate_end_time(date):
    """ Generates end timestamp
    :param date: date string from user input
    :return: unix time stamp with date + 23:59:59 time"""
    year, month, day = map(int, date.split('-'))
    dt_str_obj = xyz(year, month, day)
    dt_time = x(23, 59, 59)
    dt_end = datetime.combine(dt_str_obj, dt_time)
    end = to_unix_time(dt_end)
    return end


def choose_dr(dr_names):
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
                raise DrChoiceNotValid
            else:
                gp_chosen_email = gp_list[dr_options - 1][2]
                gp_chosen_name = gp_list[dr_options - 1][1]
                gp_details = [gp_chosen_email, gp_chosen_name]
                print("You have chosen Dr {}".format(gp_chosen_name))
                return gp_details
        except DrChoiceNotValid:
            print("\n\t< This is not a valid choice, please try again >"
                  "\n ")
        except ValueError:
            print("\n\t< This is not a valid choice, please try again >"
                  "\n ")


def choose_year():
    current_year = datetime.now().year
    while True:
        try:
            year = int(input("Please choose the year you would like your appointment (as YYYY): "))
            if year < current_year:
                raise YearPassed
            else:
                return year
        except YearPassed:
            print("\n\t< This year has already passed, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")


def choose_month(year):
    """ Checks month entered by user is valid:
        checks:
        if month an int
        if month between 1 to 12
        if month chosen is in the past
        :return:
        prints calendar for the month chosen
        month as string, padded with 0 if month a single number """
    current_month = xyz.today()
    while True:
        try:
            mm = int(input("Please choose the month would you would like your appointment: "))
            month_str = "{}-{}-28".format(year, str(mm))
            format_str = '%Y-%m-%d'
            month_obj = datetime.strptime(month_str, format_str)
            month_input = month_obj.date()
            if month_input < current_month:
                raise MonthPassed
            if not 1 <= mm <= 12:
                raise MonthNotValid
            else:
                print("--------------------------------------------")
                print(calendar.month(year, mm))
                print("--------------------------------------------")
                month = '{:02}'.format(mm)
                return month
        except MonthNotValid:
            print("\n\t< This is not a valid month, please try again >"
                  "\n")
        except MonthPassed:
            print("\n\t< This month has passed, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")


def choose_date(month, year):
    """ Checks date chosen by user is in a valid form
        Checks: if input is an int
                if day entered is valid according to the month
                if date chosen is in the past
                if date in February is in a leap year
        :return: date string with days padded with 0 for single day number"""
    days_31 = ['01', '03', '05', '07', '08', '10', '12']
    days_30 = ['04', '06', '09', '11']
    days_28 = ['02']
    while True:
        try:
            day = int(input("Please choose a date in your chosen month (as D/DD): "))
            date = "{}-{}-{:02}".format(year, str(month), day)
            date_obj = to_date_time_obj00(date)
            current = datetime.now()
            for mm in days_31:
                if mm == month:
                    if not 1 <= day <= 31:
                        raise DayNotValid
            for mm in days_30:
                if mm == month:
                    if not 1 <= day <= 30:
                        raise DayNotValid
            for mm in days_28:
                if mm == month:
                    if (year % 4) == 0:
                        if not 1 <= day <= 29:
                            raise LeapYear
                    if (year % 100) == 0:
                        if not 1 <= day <= 28:
                            raise LeapYear
                    if (year % 400) == 0:
                        if not 1 <= day <= 29:
                            raise LeapYear
            if date_obj < current:
                raise DateAfterCurrent
            else:
                return date
        except DayNotValid:
            print("\n\t< Invalid date entered, please enter a date in the correct format >"
                  "\n")
        except LeapYear:
            print("\n\t< Invalid date entered, please enter the correct date >"
                  "\n")
        except DateAfterCurrent:
            print("\n\t< This date has already passed, please choose another >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please try again >"
                  "\n")


def generate_start_time(date):
    """ Generates a unix start time stamp from the date input from the user
    """
    start_obj = to_date_time_obj00(date)
    start = to_unix_time(start_obj)
    return start


def display_available(start, end, gp_details):
    """ Displays appointments from date and time chosen by user
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("SELECT start, appointmentStatus, end FROM Appointment "
              "WHERE start >=? and end <?"
              "and gpEmail =? and appointmentStatus != 'Declined' ",
              [start, end, gp_details[0]])
    appointments = c.fetchall()
    times_str = ["09:00", "09:10", "09:20", "09:30", "09:40", "09:50",
                 "10:00", "10:10", "10:20", "10:30", "10:40", "10:50",
                 "11:00", "11:10", "11:20", "11:30", "11:40", "11:50",
                 "12:00", "12:10", "12:20", "12:30", "12:40", "12:50",
                 "13:00", "13:10", "13:20", "13:30", "13:40", "13:50",
                 "14:00", "14:10", "14:20", "14:30", "14:40", "14:50",
                 "15:00", "15:10", "15:20", "15:30", "15:40", "15:50",
                 "16:00", "16:10", "16:20", "16:30", "16:40", "16:50",
                 "17:00", "17:10", "17:20", "17:30", "17:40", "17:50"]
    times_list = []
    for times in times_str:
        format = '%H:%M'
        time_2 = datetime.strptime(times, format).time()
        times_list.append(time_2)

    times_status = {}
    if not appointments:
        for i in times_list:
            time_i = i.strftime('%H:%M')
            print(time_i, ": Available")
    else:
        for items in times_list:
            for app in appointments:
                start_time = to_regular_time(app[0])
                start_time_2 = datetime.time(start_time)
                end_time = to_regular_time(app[2] - 1)
                end_time_2 = datetime.time(end_time)
                if items >= start_time_2 and items <= end_time_2:
                    times_status[items] = ': Unavailable'
                elif items not in times_status:
                    times_status[items] = ": Available"
        for key, value in times_status.items():
            time_i = key.strftime('%H:%M')
            print(time_i, value)
        return times_str


def time_menu(date, times_list, gp_details, nhs_number):
    """ Displays menu for user to select a time, reserves appointment as 'Pending' in the database,
    or allows user to exit to main menu
    """
    while True:
        try:
            print("********************************************"
                  "\nChoose [1] to select a time"
                  "\nChoose [0] to exit to the main menu "
                  "\n********************************************")
            options = input("\nPlease select an option: ")
            if options == '':
                raise EmptyAnswer
            if options == '1':
                time_select = choose_time(date, times_list, gp_details, nhs_number)
                start = create_start(date, time_select)
                insert_appointment(start, gp_details, nhs_number)
                print("You have requested to book an appointment on {} at {}, "
                      "\nYou will receive confirmation of your appointment shortly!".format(date, time))
                return 0
            if options == '0':
                return 0
            else:
                raise InvalidAnswer()
        except InvalidAnswer:
            error = InvalidAnswer()
            print(error)
            time_menu(date, times_list, gp_details, nhs_number)
        except EmptyAnswer:
            error = EmptyAnswer()
            print(error)
            time_menu(date, times_list, gp_details, nhs_number)


def choose_time(date, times_list, gp_details, nhs_number):
    """ Checks time entered by user is in valid form and present in the list of appointment times
        Checks if time entered by user has already been booked
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            time_in = input("Please choose a time from the available appointments (as HH:MM): ")
            start = create_start(date, time_in)
            end = start + 599
            c.execute("SELECT start, appointmentStatus, end FROM Appointment "
                      "WHERE gpEmail =? and appointmentStatus != 'Declined' ",
                      [gp_details[0]])
            booked_times = c.fetchall()
            if time_in not in times_list:
                raise TimeNotValid
            for app in booked_times:
                start_time = app[0]
                end_time = app[2]
                if start >= start_time and end <= end_time:
                    raise TimeBooked
            else:
                return time_in
        except TimeNotValid:
            print("\n\t< This is not a valid time option, please try again >"
                  "\n")
        except TimeBooked:
            print("\n\t< This time is unavailable, please try again >"
                  "\n")
            time_menu(date, times_list, gp_details, nhs_number)


def create_start(date_string, time_string):
    """ Creates a unix timestamp from the chosen date (string) and appointment start time (string) by the user
    """
    day_str = date_string + ' ' + time_string
    dt_object = to_date_time_obj(day_str)
    start = to_unix_time(dt_object)
    return start


def insert_appointment(start, gp_details, nhs_number):
    """ Inserts the appointment details into the database
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("SELECT start, end FROM Appointment "
              "WHERE appointmentStatus = 'Declined' ")
    declined_times = c.fetchall()
    end = start + 599
    gp_last_name = gp_details[1]
    gp_email = gp_details[0]
    reason = 'Appointment'
    appointment_status = 'Pending'
    date_requested = to_unix_time(datetime.today())
    if not declined_times:
        chosen = (gp_email, gp_last_name, nhs_number, start, end, reason, appointment_status,
                  date_requested, '', '', '', '', '', 0, 0)
        c.execute("INSERT INTO Appointment VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", chosen)
        connection.commit()
    else:
        update = (gp_email, gp_last_name, nhs_number, date_requested)
        c.execute("UPDATE Appointment "
                  "SET gpEmail =?, gpLastName =?, nhsNumber =?, appointmentStatus = 'Pending', "
                  "dateRequested =?", update)
        connection.commit()


def return_to_main():
    """Returns user to main patient menu when typing 'yes'
    If user types anything else, will exit the program with a goodbye message"""
    if input("Type [0] to return to the main menu: ").lower() == '0':
        pass
    else:
        print("Thank you for using the UCH e-health system! Goodbye for now!")
        exit()



import sqlite3 as sql
from datetime import time as x, date as xyz, datetime
import time
import calendar
import pandas as pd


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class TimeNotValidError(Error):
    """Raised when time entered by user is not valid"""
    pass


class YearNotValidError(Error):
    """Raised when year entered by user is not valid"""
    pass


class MonthNotValidError(Error):
    """Raised when month entered by user is not valid"""
    pass


class MonthPassedError(Error):
    """Raised when month entered by user is not valid"""
    pass


class YearPassedError(Error):
    """Raised when year entered by user is not valid"""
    pass


class TimePassedError(Error):
    """Raised when time entered by user has already passed"""
    pass


class DayNotValidError(Error):
    """Raised when day entered by user is not valid"""
    pass


class TimeBookedError(Error):
    """Raised when appointment is not available to book"""
    pass


class DateAfterCurrentError(Error):
    """Raised when date chosen is in the past"""
    pass


class LeapYearError(Error):
    """Raised when date chosen in February is in a leap year"""
    pass


class DrChoiceNotValidError(Error):
    """Raised when choice of doctor not valid"""
    pass


class EmptyAnswerError(Error):
    """Raised when input left empty"""
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >\n"):
        self.message = message
        super().__init__(self.message)


class InvalidAnswerError(Error):
    """Raised when input is not valid"""
    def __init__(self, message="\n\t< This is not a valid answer, please try again >\n"):
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
        print("Choose [" + str(count) + "] Dr", dr[0] + ' ' + dr[1])
        count += 1
        gp_list.append(dr)
        counts.append(count - 1)
    while True:
        try:
            dr_options = int(input("********************************************"
                                   "\nPlease choose the doctor you would "
                                   "like to book an appointment with: "))
            if dr_options not in counts:
                raise DrChoiceNotValidError
            else:
                gp_chosen_email = gp_list[dr_options - 1][2]
                gp_chosen_name = gp_list[dr_options - 1][1]
                gp_details = [gp_chosen_email, gp_chosen_name]
                print("\nYou have chosen Dr {}".format(gp_chosen_name))
                return gp_details
        except DrChoiceNotValidError:
            print("\n\t< This is not a valid choice, please try again >"
                  "\n ")
        except ValueError:
            print("\n\t< This is not a valid choice, please enter a number >"
                  "\n ")


def choose_year():
    """ Allows user to choose the year they would like their appointment
    Checks if the year chosen is not in the past
    :return: year as an integer
    """
    current_year = datetime.now().year
    while True:
        try:
            year = int(input("********************************************"
                             "\nPlease choose the year you would like your appointment as YYYY "
                             "\nOr type 0 to go back to the appointment menu: "))
            if year == 0:
                return 0
            elif year < current_year:
                raise YearPassedError
            elif not 2020 <= year <= 2100:
                raise YearNotValidError
            else:
                return year
        except YearPassedError:
            print("\n\t< This year has already passed, please try again >"
                  "\n")
        except YearNotValidError:
            print("\n\t< This year is not valid, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please enter a number>"
                  "\n")


def choose_month(year):
    """ Allows user to choose the month they would like their appointment
        checks: if month is an integer
        If month between 1 to 12
        if month chosen is in not the past
        :return:
        prints calendar for the month chosen
        month as string, padded with 0 if month a single number """
    current_month = xyz.today()
    while True:
        try:
            print("********************************************"
                  "\n [1] January     \t[2] February      \t[3] March"
                  "\n [4] April     \t\t[5] May           \t[6] June"
                  "\n [7] July      \t\t[8] August        \t[9] September "
                  "\n [10] October    \t[11] November     \t[12] December"
                  "\n********************************************")
            mm = int(input("Please choose the month would you would like your appointment "
                           "\n(or type 0 to go back choose another date): "))
            if mm == 0:
                return 0
            month_str = "{}-{}-28".format(year, str(mm))
            format_str = '%Y-%m-%d'
            month_obj = datetime.strptime(month_str, format_str)
            month_input = month_obj.date()
            if month_input < current_month:
                raise MonthPassedError
            elif not 1 <= mm <= 12:
                raise MonthNotValidError
            else:
                print("--------------------------------------------")
                print(calendar.month(year, mm))
                print("--------------------------------------------")
                month = '{:02}'.format(mm)
                return month
        except MonthNotValidError:
            print("\n\t< This is not a valid month, please try again >"
                  "\n")
        except MonthPassedError:
            print("\n\t< This month has passed, please try again >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please enter a number >"
                  "\n")


def choose_date(month, year):
    """ Allows user to choose the day they would lieke their appointment
        Checks date chosen by user is in a valid form
        Checks: if input is an integer
                if date chosen is in the past
                if the date chosen is valid for that month
                if date in February is in a leap year
        :return: date string with days padded with 0 for single day number"""
    days_31 = ['01', '03', '05', '07', '08', '10', '12']
    days_30 = ['04', '06', '09', '11']
    days_28 = ['02']
    while True:
        try:
            day = int(input("Please choose a day in your chosen month (as D/DD)"
                            "\n(or type 0 to go back and choose another date): "))
            if day == 0:
                return 0
            date = "{}-{}-{:02}".format(year, str(month), day)
            date_obj = to_date_time_obj00(date).date()
            current = datetime.now().date()
            for mm in days_31:
                if mm == month:
                    if not 1 <= day <= 31:
                        raise DayNotValidError
            for mm in days_30:
                if mm == month:
                    if not 1 <= day <= 30:
                        raise DayNotValidError
            for mm in days_28:
                if mm == month:
                    if (year % 4) == 0:
                        if not 1 <= day <= 29:
                            raise LeapYearError
                    if (year % 100) == 0:
                        if not 1 <= day <= 28:
                            raise LeapYearError
                    if (year % 400) == 0:
                        if not 1 <= day <= 29:
                            raise LeapYearError
            if date_obj == current:
                return date
            elif date_obj < current:
                raise DateAfterCurrentError
            else:
                return date
        except DayNotValidError:
            print("\n\t< Invalid date entered, please enter a date in the correct format >"
                  "\n")
        except LeapYearError:
            print("\n\t< Invalid date entered, please enter the correct date >"
                  "\n")
        except DateAfterCurrentError:
            print("\n\t< This date has already passed, please choose another >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please enter a number >"
                  "\n")


def generate_start_time(date):
    """ Generates a unix start time stamp from the date (string) input from the user
    :return: unix start time (integer)"""
    start_obj = to_date_time_obj00(date)
    start = to_unix_time(start_obj)
    return start


def display_available(date, start, end, gp_details):
    """ Displays appointments from the date and time chosen by user
    :return: pandas dataframe of the time and availability for the day"""
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    print("\nCurrent availability for Dr {} on {}: ".format(gp_details[1], date))
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
        format_str = '%H:%M'
        time_2 = datetime.strptime(times, format_str).time()
        times_list.append(time_2)
    key_time = []
    value_status = []
    times_status = {}
    if not appointments:
        for i in times_list:
            time_i = i.strftime('%H:%M')
            key_time.append(time_i)
            value_status.append("   Available")
        data = pd.DataFrame({'Time': key_time, 'Status': value_status})
        print("********************************************\n")
        print(data.to_string(columns=['Time', 'Status'], index=False))
        print("\n********************************************")

    else:
        for items in times_list:
            for app in appointments:
                start_time = to_regular_time(app[0])
                start_time_2 = datetime.time(start_time)
                end_time = to_regular_time(app[2] - 1)
                end_time_2 = datetime.time(end_time)
                if items >= start_time_2 and items <= end_time_2:
                    times_status[items] = ' Unavailable'
                elif items not in times_status:
                    times_status[items] = " Available"
        key_time = []
        value_status = []
        for key, value in times_status.items():
            time_i = key.strftime('%H:%M')
            key_time.append(time_i)
            value_status.append('   ' + value)
        data = pd.DataFrame({'Time': key_time, 'Status': value_status})
        print("********************************************\n")
        print(data.to_string(columns=['Time', 'Status'], index=False))
        print("\n********************************************")
    return times_str


def choose_time(date, times_str, gp_details):
    """ Allows user to choose the time they would like their appointment
        Checks time entered by user is in valid form and present in the list of appointment times
        Checks if time entered by user has already been booked
        Checks if the time has already passed
        :return: time (string) """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            time_in = input("\nPlease choose a time from the available appointments (as HH:MM)"
                            "\n(or type 0 to go back and choose another date): ")
            if time_in == '0':
                return 0
            if time_in not in times_str:
                raise TimeNotValidError
            start = create_start(date, time_in)
            end = start + 599
            date_obj = to_regular_time(start)
            current = datetime.now()
            if date_obj < current:
                raise TimePassedError
            c.execute("SELECT start, appointmentStatus, end FROM Appointment "
                      "WHERE gpEmail =? and appointmentStatus != 'Declined' ",
                      [gp_details[0]])
            booked_times = c.fetchall()
            for app in booked_times:
                start_time = app[0]
                end_time = app[2]
                if start >= start_time and end <= end_time:
                    raise TimeBookedError
            else:
                return time_in
        except TimeNotValidError:
            print("\n\t< This is not a valid time option, please try again >"
                  "\n")
        except TimeBookedError:
            print("\n\t< This time is unavailable, please try again >"
                  "\n")
        except TimePassedError:
            print("\n\t< This time has already passed, please try again >"
                  "\n")


def create_start(date_string, time_string):
    """ Creates a unix timestamp from the chosen date (string) and appointment start time (string) by the user
    :return: unix timestamp (integer)"""
    day_str = date_string + ' ' + time_string
    dt_object = to_date_time_obj(day_str)
    start = to_unix_time(dt_object)
    return start


def insert_appointment(start, gp_details, nhs_number):
    """ Inserts the appointment details into the database
    Creates new row with appointment booked as 'Pending'"""
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    end = start + 599
    gp_last_name = gp_details[1]
    gp_email = gp_details[0]
    reason = 'Appointment'
    appointment_status = 'Pending'
    date_requested = to_unix_time(datetime.today())
    chosen = (gp_email, gp_last_name, nhs_number, start, end, reason, appointment_status,
              date_requested, '', '', '', '', '', 0, 0)
    c.execute("INSERT INTO Appointment VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", chosen)
    connection.commit()


def return_to_main():
    """Returns user to main patient menu when typing '0'
    If user types anything else, will exit the program with a goodbye message"""
    if input("Type [0] to return to the main menu "
             "\n(or any other key to exit the UCL e-health system): ").lower() == '0':
        pass
    else:
        print("Thank you for using the UCH e-health system! Goodbye for now!")
        exit()

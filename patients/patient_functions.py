import sqlite3 as sql
from datetime import time as x, date as xyz, datetime
import time
import calendar
import pandas as pd

"""
This module contains all functions for patients to book an appointment.

Error classes contain exception handling for user input in the functions. 
Functions allow patient to choose the doctor, year, month, day and time for the appointment 
and for the chosen information to be inserted into the database.
"""


class Error(Exception):
    """ Error exception base class. """
    pass


class TimeNotValidError(Error):
    """ Raised when time entered by patient is not in valid form or not in the pre-defined times list. """
    pass


class YearNotValidError(Error):
    """ Raised when year entered by patient is not valid. """
    pass


class MonthNotValidError(Error):
    """ Raised when month entered by patient is not valid. """
    pass


class MonthPassedError(Error):
    """ Raised when month entered by patient is in the past. """
    pass


class YearPassedError(Error):
    """ Raised when year entered by patient is in the past. """
    pass


class TimePassedError(Error):
    """ Raised when time entered by patient is in the past. """
    pass


class DayNotValidError(Error):
    """ Raised when day entered by user is not valid. """
    pass


class TimeBookedError(Error):
    """ Raised when appointment is not available to book. """
    pass


class DatePassedError(Error):
    """ Raised when date chosen by patient is in the past. """
    pass


class LeapYearError(Error):
    """ Raised when date chosen in February does not align with the 28/29th leap year. """
    pass


class DrChoiceNotValidError(Error):
    """ Raised when choice of doctor from the list is not valid. """
    pass


class EmptyAnswerError(Error):
    """
    Error class for when an input is left empty.

    Attributes:
        message (str): Message is raised when the patient presses enter with no input.
    """
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >\n"):
        """
        The constructor for EmptyAnswerError class.

        Parameters:
            message (str): Message is raised when the patient presses enter with no input.
        """
        self.message = message
        super().__init__(self.message)


class InvalidAnswerError(Error):
    """
    Error class for when an input is not valid.

    Attributes:
        message (str): Message is raised when the patient enters a string that is not valid to requirements.
    """
    def __init__(self, message="\n\t< This is not a valid answer, please try again >\n"):
        """
        The constructor for InvalidAnswerError class.

        Parameters:
            message (str): Message is raised when the patient enters a string that is not valid to requirements.
        """
        self.message = message
        super().__init__(self.message)


def to_regular_time(time_stamp):
    """
    Converts a unix timestamp to datetime object.

    Parameters:
        time_stamp (int): Unix timestamp.
    Returns:
        datetime (obj): Datetime object.
    """
    return datetime.utcfromtimestamp(int(time_stamp))


def to_unix_time(date_time):
    """
    Converts a datetime object to unix timestamp.

    Parameters:
        date_time (obj): Datetime object.
    Returns:
        time_stamp (int): Unix timestamp.
    """
    unix_stamp = int(time.mktime(date_time.timetuple()))
    return unix_stamp


def to_date_time_obj(string):
    """
    Converts datetime string to datetime object.

    Parameters:
        string (str): Datetime string.
    Returns:
        dt_object (obj): Datetime object.
    """
    dt_object = datetime.strptime(string, '%Y-%m-%d %H:%M')
    return dt_object


def to_date_time_obj00(string):
    """
    Converts date string to date object with time 00:00:00.

    Parameters:
        string (str): Date string.
    Returns:
        dt_object (obj): Datetime object (with time 00:00:00).
    """
    dt_object = datetime.strptime(string, '%Y-%m-%d')
    return dt_object


def generate_end_time(date):
    """
    Generates 'end' unix timestamp to be used for displaying available appointments within 1 day.

    Takes the date entered by the patient and converts to a datetime object with time + 23:59:59 added.
    Then converts to a unix timestamp.

    Parameters:
        date (str): Date string.
    Returns:
        end (int): unix timestamp.
    """
    year, month, day = map(int, date.split('-'))
    dt_str_obj = xyz(year, month, day)
    dt_time = x(23, 59, 59)
    dt_end = datetime.combine(dt_str_obj, dt_time)
    end = to_unix_time(dt_end)
    return end


def choose_dr(dr_names):
    """
    Function for patient to select a doctor from list.

    Prints a list of doctors (first and last name) with count for patient to select by a number.
    Exception prevents patient from choosing a number that does not exist.

    Parameters:
          dr_names (list): list of all doctors in the database, includes first, last and email address of each.
    Returns:
         gp_details (list): list of chosen doctor email and last name.
    """
    gp_list = []
    counts = []
    count = 1
    for dr in dr_names:
        # print [count] and dr first and last name for display to patient
        print("Choose [" + str(count) + "] Dr", dr[0] + ' ' + dr[1])
        count += 1
        gp_list.append(dr)
        counts.append(count - 1)
    while True:
        try:
            dr_options = int(input("********************************************"
                                   "\nPlease choose the doctor you would "
                                   "like to book an appointment with: "))
            # exception raised if input not a number in count list
            if dr_options not in counts:
                raise DrChoiceNotValidError
            else:
                gp_chosen_email = gp_list[dr_options - 1][2]
                gp_chosen_name = gp_list[dr_options - 1][1]
                # list of dr email and last name created
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
    """
    Function for patient to choose the year they would like their appointment.

    Patient inputs year, exceptions check if the year is not in the past, between 2020 - 2100 and is a number.

    Returns:
        year (int): Year chosen.
        or 0 (int): To return to the menu.
    """
    current_year = datetime.now().year
    while True:
        try:
            year = int(input("********************************************"
                             "\nPlease choose the year you would like your appointment as YYYY "
                             "\nOr type 0 to go back to the appointment menu: "))
            # return to menu
            if year == 0:
                return 0
            # exception raised if year chosen in the past
            elif year < current_year:
                raise YearPassedError
            # exception raised if year chosen not within 2020-2100
            elif not 2020 <= year <= 2100:
                raise YearNotValidError
            else:
                # chosen year returned
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
    """
    Function for patient to choose the month they would like their appointment.

    Prints months to choose from as a list of numbers, patient chooses month.
    Exceptions check if month is an integer, between 1 - 12, is in not the past.
    Prints a calendar for month chosen to show days.

    Parameters:
        year (int): Year chosen.
    Returns:
        month (int): Month chosen, padded with 0 if month a single number.
        or 0 (int): To return to the menu.
    """
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
            # to choose another date
            if mm == 0:
                return 0
            # to format month as an object
            month_str = "{}-{}-28".format(year, str(mm))
            format_str = '%Y-%m-%d'
            month_obj = datetime.strptime(month_str, format_str)
            month_input = month_obj.date()
            # exception raised if month chosen in the past
            if month_input < current_month:
                raise MonthPassedError
            # exception raised if month chosen not between 1-12
            elif not 1 <= mm <= 12:
                raise MonthNotValidError
            else:
                # print calendar for chosen month and year
                print("--------------------------------------------")
                print(calendar.month(year, mm))
                print("--------------------------------------------")
                month = '{:02}'.format(mm)
                # return chosen month
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
    """
    Function for patient to choose the month they would like their appointment.

    Patient inputs day.
    Exceptions check if day is an integer, is in not the past, if the date chosen is valid for that month,
    and if date in February is in a leap year.

    Parameters:
        month (int): Month chosen.
        year (int): Year chosen.
    Returns:
        day (int): Day chosen, padded with 0 if day a single number.
        or 0 (int): To return to the menu.
    """
    # lists of months with 31, 30 and 28/29 days
    days_31 = ['01', '03', '05', '07', '08', '10', '12']
    days_30 = ['04', '06', '09', '11']
    days_28 = ['02']
    while True:
        try:
            day = int(input("Please choose a day in your chosen month (as D/DD)"
                            "\n(or type 0 to go back and choose another date): "))
            # to choose another date
            if day == 0:
                return 0
            # to create datetime object with chosen month, day and year
            date = "{}-{}-{:02}".format(year, str(month), day)
            date_obj = to_date_time_obj00(date).date()
            current = datetime.now().date()
            for mm in days_31:
                if mm == month:
                    # if day not between 1-31
                    if not 1 <= day <= 31:
                        raise DayNotValidError
            for mm in days_30:
                if mm == month:
                    # if day not between 1-30
                    if not 1 <= day <= 30:
                        raise DayNotValidError
            # to find leap year errors in February
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
            # exception raised if day chosen in the past
            elif date_obj < current:
                raise DatePassedError
            else:
                # return date
                return date
        except DayNotValidError:
            print("\n\t< Invalid date entered, please enter a date in the correct format >"
                  "\n")
        except LeapYearError:
            print("\n\t< Invalid date entered, please enter the correct date >"
                  "\n")
        except DatePassedError:
            print("\n\t< This date has already passed, please choose another >"
                  "\n")
        except ValueError:
            print("\n\t< This is not a valid option, please enter a number >"
                  "\n")


def generate_start_time(date):
    """
    Generates 'start' unix timestamp to be used for displaying available appointments within 1 day.

    Takes the date entered by the patient and converts to a datetime object with time + 00:00:00 added.
    Then converts to a unix timestamp.

    Parameters:
        date (str): Date string.
    Returns:
        start (int): unix timestamp.
    """
    start_obj = to_date_time_obj00(date)
    start = to_unix_time(start_obj)
    return start


def display_available(date, start, end, gp_details):
    """
    Displays appointments times and availability from the date chosen by patient.

    Finds all appointments that exist in the database between 00:00:00 - 23:59:59 of the date chosen by patient.
    If an appointment/booking exists between this time and is not marked as declined, it will display as 'unavailable',
    otherwise all times will be shown as 'available'.
    Prints a pandas dataframe with all times from 09:00-18:00 (in 10 minute slots) and availability for each slot.

    Parameters:
        date (str): Date chosen.
        start (int): Unix timestamp of date chosen (with time + 00:00:00).
        end (int): Unix timestamp of date chosen (with time + 23:59:59).
        gp_details (list): Doctor chosen (email and last name).
    Returns:
        times_str (list): List of time strings 09:00-18:00 (in 10 minute slots).
    """
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
    # format all times as datetime objects and add to times_list
    for times in times_str:
        format_str = '%H:%M'
        time_2 = datetime.strptime(times, format_str).time()
        times_list.append(time_2)
    key_time = []
    value_status = []
    times_status = {}
    # if appointments list empty, display all appointments as available for that day
    if not appointments:
        for i in times_list:
            time_i = i.strftime('%H:%M')
            key_time.append(time_i)
            value_status.append("   Available")
        # create pandas dataframe
        data = pd.DataFrame({'Time': key_time, 'Status': value_status})
        print("********************************************\n")
        print(data.to_string(columns=['Time', 'Status'], index=False))
        print("\n********************************************")

    else:
        # for each time in times_list (10 min slot)
        for items in times_list:
            # for each booking in list from database
            for app in appointments:
                # convert start and end to datetime objects
                start_time = to_regular_time(app[0])
                start_time_2 = datetime.time(start_time)
                end_time = to_regular_time(app[2] - 1)
                end_time_2 = datetime.time(end_time)
                # if booking exists between start and end time
                if items >= start_time_2 and items <= end_time_2:
                    # display as unavailable
                    times_status[items] = ' Unavailable'
                # if time not in list, display as available
                elif items not in times_status:
                    times_status[items] = " Available"
        key_time = []
        value_status = []
        for key, value in times_status.items():
            time_i = key.strftime('%H:%M')
            key_time.append(time_i)
            value_status.append('   ' + value)
        # create pandas dataframe
        data = pd.DataFrame({'Time': key_time, 'Status': value_status})
        print("********************************************\n")
        print(data.to_string(columns=['Time', 'Status'], index=False))
        print("\n********************************************")
    connection.close()
    # return times_str for use in choose time exception handling
    return times_str


def choose_time(date, times_str, gp_details):
    """
    Function for patient to choose the time they would like their appointment.

    Patient inputs time. Exceptions check if time is present in the list of appointment times (times_str),
    if time entered by user has already been booked, if the time has already passed

    Parameters:
        date (str): Date chosen.
        gp_details (list): Doctor chosen (email and last name).
        times_str (list): List of time strings 09:00-18:00 (in 10 minute slots).
    Returns:
        time (str): Time chosen (in form 00:00).
        or 0 (int): To return to the menu.
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    while True:
        try:
            time_in = input("\nPlease choose a time from the available appointments (as HH:MM)"
                            "\n(or type 0 to go back and choose another date): ")
            # to choose another date
            if time_in == '0':
                return 0
            # if time chosen not in the times_str list (09:00-18:00 in 10 min slots) exception raised
            if time_in not in times_str:
                raise TimeNotValidError
            start = create_start(date, time_in)
            end = start + 599
            date_obj = to_regular_time(start)
            current = datetime.now()
            # if time has past, exception raised
            if date_obj < current:
                raise TimePassedError
            c.execute("SELECT start, appointmentStatus, end FROM Appointment "
                      "WHERE gpEmail =? and appointmentStatus != 'Declined' ",
                      [gp_details[0]])
            booked_times = c.fetchall()
            for app in booked_times:
                start_time = app[0]
                end_time = app[2]
                # if time already booked, exception raised
                if start >= start_time and end <= end_time:
                    raise TimeBookedError
            else:
                connection.close()
                # return time chosen
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
    """
    Creates a unix timestamp from the chosen date and appointment start time to insert into the database.

    Creates date and time string, converts to a datetime object and then to a unix timestamp.

    Parameters:
        date_string (str): Date chosen.
        time_string (str): Time chosen.
    Returns:
         start (int): Unix timestamp of the date and time chosen.
    """
    day_str = date_string + ' ' + time_string
    dt_object = to_date_time_obj(day_str)
    start = to_unix_time(dt_object)
    return start


def insert_appointment(start, gp_details, nhs_number):
    """
    Inserts appointment details into the database.

    Creates new row with appointment with new appointment ID, chosen gp email, gp last name, patient nhs number,
    start time of appointment, end time of appointment (start time + 599 seconds), reason as 'Appointment', appointment
    status as 'Pending', date requested as a unix timestamp for now and the remaining fields as empty strings.

    Parameters:
        start (int): Unix timestamp of the date and time chosen.
        gp_details (list): Doctor chosen (email and last name).
        nhs_number (int): The patient's nhs number.
    """
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
    connection.close()


def return_to_main():
    """
    Returns user to main patient menu when typing '0'.
    If user types anything else, will exit the program with a goodbye message.
    """
    if input("Type [0] to return to the main menu "
             "\n(or any other key to exit the UCL e-health system): ").lower() == '0':
        pass
    else:
        print("Thank you for using the UCH e-health system! Goodbye for now!")
        exit()

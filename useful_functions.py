from datetime import datetime,timedelta
import time

class EmptyValueError(Exception):
    """Exception class for if the user doesn't enter a value for date or time entry"""
    pass

DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M"
DATE_TIME_FORMAT = DATE_FORMAT_STRING + " " + TIME_FORMAT_STRING

def validate_date(string):
    """
    Call this function to validate any date entered by the user
    Is escapable. User cannot enter an invalid date or leave the field empty.
    """
    while True:
        try:
            datestring = input(string + " (YYYY-MM-DD) (enter [0]) to exit: ")
            if datestring == '0':
                return "exit"
            if datestring == '':
                raise EmptyValueError
            date = datetime.strptime(datestring, DATE_FORMAT_STRING)
            return date
        except EmptyValueError:
            print("\n\t< You need to enter a value, please try again... >\n")
        except ValueError:
            print("\n\t< Invalid date entered, please try again... >\n")


def validate_time(string):
    """
    Call this function to validate any time entered by the user
    Is escapable. User cannot enter an invalid time or leave the field empty.
    """
    while True:
        try:
            timestring = input(string + " (HH:MM) (enter [0]) to exit: ")
            if timestring == '0':
                return "exit"
            if timestring == '':
                raise EmptyValueError
            time = datetime.strptime(timestring, TIME_FORMAT_STRING)
            return time
        except EmptyValueError:
            print("\n\t< You need to enter a value, please try again... >\n")
        except ValueError:
            print("\n\t< Invalid time entered, Please try again... >\n")

def unix_to_regular_time(unixtimestamp):
    """
    Converts a unix integer time back into a python datetime object.
    """
    return datetime.utcfromtimestamp(int(unixtimestamp))

def regular_to_unix_time(dt):
    """
    Converts python datetime object into a unix time.
    Unix time is an integer value which denotes seconds since unix epoch.
    The Unix epoch is 00:00:00 UTC on 1 January 1970.
    Because of this all date-of-birth fields in our database do not use unix time.
    However it is helpful when checking for conflicts in appointments during timetabling to use unix time.
    """
    result = int(time.mktime(dt.timetuple()))
    return result

def date_range(start_date, end_date):
    """
    returns an iterable, allowing you to loop through days between a start and an end date
    use as follows:
       for single_date in daterange(start_date, end_date):
           * YOUR CODE HERE *
    """
    for n in range(int((end_date + timedelta(1) - start_date).days)):
        yield start_date + timedelta(n)

def banner(staff):
    print("--------------------------------------------")
    print("\t {} Main Menu" .format(staff))
    print("--------------------------------------------")
    print("Welcome {}" .format(staff))
from datetime import datetime,timedelta
import time
import sys

class EmptyValueError(Exception):
    pass

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformat = dateformatstring + " " + timeformatstring

#call this function to validate any date entered by the user
def validate_date(string):
    while True:
        try:
            datestring = input(string + " (YYYY-MM-DD) (enter [0]) to exit: ")
            if datestring == '0':
                return "exit"
            if datestring == '':
                raise EmptyValueError
            date = datetime.strptime(datestring,dateformatstring)
            return date
        except EmptyValueError:
            print("\n\t< You need to enter a value, please try again... >\n")
        except ValueError:
            print("\n\t< Invalid date entered, please try again... >\n")

#call this function to validate any time entered by the user
def validate_time(string):
    while True:
        try:
            timestring = input(string + " (HH:MM) (enter [0]) to exit: ")
            if timestring == '0':
                return "exit"
            if timestring == '':
                raise EmptyValueError
            time = datetime.strptime(timestring,timeformatstring)
            return time
        except EmptyValueError:
            print("\n\t< You need to enter a value, please try again... >\n")
        except ValueError:
            print("\n\t< Invalid time entered, Please try again... >\n")

#convert a unix integer time back into a datetime object
def unix_to_regular_time(unixtimestamp):
    return datetime.utcfromtimestamp(int(unixtimestamp))

#convert python datetime object into a unix timestring
def regular_to_unix_time(dt):
    result = int(time.mktime(dt.timetuple()))
    return result

#returns an iterable, allowing you to loop through days between a start and an end date
#use as follows:
#   for single_date in daterange(start_date, end_date):
#       * YOUR CODE HERE *
def date_range(start_date, end_date):
    for n in range(int((end_date + timedelta(1) - start_date).days)):
        yield start_date + timedelta(n)

def banner(staff):
    print("--------------------------------------------")
    print("\t {} Main Menu" .format(staff))
    print("--------------------------------------------")
    print("Welcome {}" .format(staff))

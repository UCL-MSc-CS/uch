from datetime import datetime,timedelta
import time
from GPs.GPExceptions import *

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformat = dateformatstring + " " + timeformatstring

#call this function to validate any date entered by the user
def validatedate(string):
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
            print("\t<You need to enter a value, please try again...>")
        except:
            print("\t<Invalid date entered, please try again...>")

#call this function to validate any time entered by the user
def validatetime(string):
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
            print("\t<You need to enter a value, please try again...>")
        except:
            print("\t<Invalid time entered, Please try again...>")

#convert a unix integer time back into a datetime object
def toregulartime(unixtimestamp):
    return datetime.utcfromtimestamp(int(unixtimestamp))

#convert python datetime object into a unix timestring
def tounixtime(dt):
    result = int(time.mktime(dt.timetuple()))
    return result

#returns an iterable, allowing you to loop through days between a start and an end date
#use as follows:
#   for single_date in daterange(start_date, end_date):
#       * YOUR CODE HERE *
def daterange(start_date, end_date):
    for n in range(int((end_date + timedelta(1) - start_date).days)):
        yield start_date + timedelta(n)

def banner(staff):
    print("--------------------------------------------")
    print("\t {} Main Menu" .format(staff))
    print("--------------------------------------------")
    print("Welcome {}" .format(staff))

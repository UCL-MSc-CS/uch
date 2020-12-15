from datetime import datetime,timedelta
import time

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformat = dateformatstring + " " + timeformatstring

#call this function to validate any date entered by the user
def validatedate(string):
    while True:
        try:
            datestring = input(string + " (YYYY-MM-DD): ")
            date = datetime.strptime(datestring,dateformatstring)
            return date
        except:
            print("\t<Invalid date entered,Please try again...>")

#call this function to validate any time entered by the user
def validatetime(string):
    while True:
        try:
            timestring = input(string + " (HH:MM): ")
            time = datetime.strptime(timestring,timeformatstring)
            return time
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

from datetime import time as x, date as xyz, datetime, timedelta
import time

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




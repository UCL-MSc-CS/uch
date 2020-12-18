from timetablefunctions import checkslotavailable
import usefulfunctions as uf
from datetime import datetime, timedelta

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"
datetimeformatstring = dateformatstring + " " + timeformatstring

times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
             "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]


def displayAvailable(start, end, gpDetails):
    """ Displays appointments from date and time chosen by user
    """
    for timeslot, timevalue in enumerate(times):
        date = datetime.strftime(uf.toregulartime(start), dateformatstring)
        result = checkslotavailable(
            date, times[timeslot], times[timeslot + 1], gpDetails[0])
        if result == "unavailable":
            print(timevalue + ' ' + "Unavailable")
        else:
            print(timevalue + ' ' + "Available")


def chooseTime(date, times, gpDetails):
    """ Checks time entered by user is in valid form and present in the list of appointment times
        Checks if time entered by user has already been booked
    """
    while True:
        time = uf.validatetime(
            "Please choose a time from the available appointments")
        timestring = datetime.strftime(time, timeformatstring)
        if timestring not in times:
            print("This is not a time listed above, please try again")
        else:
            break
    start = datetime.strftime(time, timeformatstring)
    end = datetime.strftime(time + timedelta(minutes=30), timeformatstring)
    results = checkslotavailable(date, start, end, gpDetails[0])
    if results == "unavailable":
        print("This time is unavailable, please try again")
    else:
        return timestring

# Line 20 in viewCancelFunctions
 """SELECT 
        A.appointmentID, 
        A.start, 
        P.gpLastName, 
        A.appointmentStatus
    FROM 
        Appointment A
    LEFT JOIN PatientDetail P USING (nhsNumber)
    WHERE 
        patientEmail =?, [patientEmail]
"""

# Line 35 in viewCancelFunctions
"""
for item in status:
    if item == 'Accepted':
        item = 'Confirmed Booking'
        new_status.append(item)
    elif item == 'Pending':
        item = 'Still Pending Approval'
        new_status.append(item)
    elif item == 'Declined':
        item = 'The Doctor has declined your appointment'
        new_status.append(item)
"""

""" Displays appointments from date and time chosen by user
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()
    c.execute("SELECT start, appointmentStatus, end FROM Appointment WHERE start >=? and end <? and gpEmail =?",
              [start, end, gpDetails[0]])
    appointments = c.fetchall()
    times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
             "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
#  print("appointments")
#     print(appointments)

    dict_time_status = {}
    for index, time in enumerate(times):
        print("in first loop")
        for appointment in appointments:
            print("in second loops")
            apt_start_time = toregulartime(start) + datetime.strptime(time,"%H:%M")
            apt_end_time = toregulartime(start) + datetime.strptime(times[index + 1],"%H:%M")
            print("apt_start_time, apt_end_time")
            print(apt_start_time, apt_end_time)
            pre_exist_start = toregulartime(appointment[0]).x()
            pre_exist_end = toregulartime(appointment[2]).x()
            print("pre_exist_start, pre_exist_end")
            print(pre_exist_start, pre_exist_end)
            pre_exist_status = appointment[1]
            print("pre_exist_status")
            print(pre_exist_status)
            if pre_exist_status == '':
                condition_1 = pre_exist_start <= apt_start_time < pre_exist_end
                condition_2 = pre_exist_start <= apt_end_time < pre_exist_end
                condition_3 = pre_exist_start < apt_start_time and pre_exist_end > apt_end_time
                print(condition_1,condition_2,condition_3)
                if condition_1 or condition_2 or condition_3:
                    dict_time_status[time] = " unavailable"
    # print("************")
    # print(dict_time_status)
    # print("************")

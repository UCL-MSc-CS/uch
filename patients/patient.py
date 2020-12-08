import sqlite3 as sql
from getpass import getpass
import calendar
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time


class Patient:

    def __init__(self, patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2,
                 postcode, telephoneNumber, password):
        self.patientEmail = patientEmail
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.age = age
        self.gender = gender
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.postcode = postcode
        self.telephoneNumber = telephoneNumber
        self.password = password
        self.loggedIn = 1
        self.registrationConfirm = 0
        self.connection = sql.connect('patient.db')
        self.c = self.connection.cursor()

    def register(self):
        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (self.patientEmail, self.firstName, self.lastName, self.dateOfBirth, self.age, self.gender,
                        self.addressLine1, self.addressLine2, self.postcode, self.telephoneNumber, self.password,
                        self.loggedIn, self.registrationConfirm))
        self.connection.commit()

    def registrationSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        self.c.execute("SELECT * FROM PatientDetail WHERE firstName =? AND lastName =? AND patientEmail =?",
                       [self.firstName, self.lastName, self.patientEmail])
        patientDetail = self.c.fetchall()
        for i in patientDetail:
            print("Welcome, " + i[1] + "! Thank you for registering with UCH.")
            print("First Name: " + i[1])
            print("Last Name: " + i[2])
            print("Email: " + i[0])
            print("Password: " + hash)
            self.connection.commit()

    def bookAppointment(self):
        print("**********"
              "\n[1] to book an appointment"
              "\n[2] to view your confirmed appointments"
              "\n[3] to cancel an appointment"
              "\n[4] to exit to the main menu: ")
        options = int(input("Please choose from the options above: "))
        if options == 1:
            a = self.chooseDoctor()
            if a == 1:
                y = self.chooseSpecificDr()
                x = self.chooseDate()
                self.displayAvailable(x, y)
                self.chooseTime(x, y)
            if a == 2:
                y = self.chooseAnyDr()
                x = self.chooseDate()
                self.displayAvailable(x, y)
                self.chooseTime(x, y)
            if a == 3:
                y = self.chooseDrGender()
                x = self.chooseDate()
                self.displayAvailable(x, y)
                self.chooseTime(x, y)
            if a == 4:
                self.returnToAppMenu()
        if options == 2:
            self.viewAppConfirmations()
        if options == 3:
            self.cancelAppointment()
        if options == 4:
            # exit to main menu
            pass

    def chooseDoctor(self):
        print("**********"
              "\n[1] To book an appointment with a specific doctor"
              "\n[2] To book an appointment with any doctor"
              "\n[3] To book an appointment with a doctor of a specific gender"
              "\n[4] To exit to the main menu"
              "\n**********")
        dr_options = int(input("Please choose from the options above: "))
        return dr_options

    def chooseSpecificDr(self):
        print("**********"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT gpFirstName, gpLastName, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        gp_list = []
        count = 1
        for dr in dr_names:
            print("Choose [" + str(count) + "] Dr", dr[0] + ' ' + dr[1])
            count += 1
            gp_list.append(dr)

        dr_option1 = int(input("**********"
                           "\nPlease choose the doctor you would "
                           "like to book an appointment with: "))
        gp_chosen_email = gp_list[dr_option1 - 1][2]
        gp_chosen_name = gp_list[dr_option1 - 1][1]

        # if dr_option1 not in gp_list:
        #     print("This is not a valid choice of doctor, please try again")
        return [gp_chosen_email, gp_chosen_name]

    def chooseAnyDr(self):
        self.c.execute("SELECT DISTINCT(gpLastName) FROM GP")
        dr_names = self.c.fetchall()
        gp_list = []
        for dr in dr_names:
            gp_list.append(dr[0])

        gpLastName = random.choice(gp_list)
        print("The doctor you have been assigned is Dr {}".format(gpLastName))
        return gpLastName

    def chooseDrGender(self):
        print("**********"
              "\n[1] To book an appointment with a male doctor"
              "\n[2] to book an appointment with a female doctor")
        gp_options = int(input("Please choose from the options above: "))

        if gp_options == 1:
            self.c.execute("SELECT gpLastName FROM GP WHERE gpGender = 'M'")
            dr_names = self.c.fetchall()
            gp_list = []
            for dr in dr_names:
                gp_list.append(dr[0])
            gpLastName = random.choice(gp_list)
            print("\nThe male doctor you have been assigned is Dr {}".format(gpLastName))
            return gpLastName

        if gp_options == 2:
            self.c.execute("SELECT gpLastName FROM GP WHERE gpGender = 'F' ")
            dr_names = self.c.fetchall()
            gp_list = []
            for dr in dr_names:
                gp_list.append(dr[0])
            gpLastName = random.choice(gp_list)
            print("\nThe female doctor you have been assigned is Dr {}".format(gpLastName))
            return gpLastName


    def chooseDate(self):
        print("**********"
              "\n [1] January     \t[2] February      \t[3] March"
              "\n [4] April     \t\t[5] May           \t[6] June"
              "\n [7] July      \t\t[8] August        \t[9] September "
              "\n [10] October    \t[11] November     \t[12] December")
        mm = int(input("Please choose the month would you would like your appointment in 2021: "))
        print("----------")
        print(calendar.month(2021, mm))
        print("----------")
        day = input("Please select a day (as dd): ")
        date = "2021-{}-{}".format(mm, day)
        return date

    def toregulartime(self, unixtimestamp):
        return datetime.utcfromtimestamp(int(unixtimestamp))

    def tounixtime(self, dt):
        result = int(time.mktime(dt.timetuple()))
        return result

    def toDateTimeObj(self, string):
        """ Converts date time string to datetime object"""
        dt_object = datetime.strptime(string, '%Y-%m-%d %H:%m')
        return dt_object

    def toDateObjApp00(self, string):
        """ Converts date string to date object with time as 00:00:00"""
        dt_object = datetime.strptime(string, '%Y-%m-%d')
        return dt_object

    def displayAvailable(self, date, gpLastName):
        start_obj = self.toDateObjApp00(date)
        start = self.tounixtime(start_obj)

        # dt_string = date
        # dt_object = datetime.strptime(dt_string, '%Y-%m-%d')
        # print(dt_object)
        # print(start)

        year, month, day = map(int, date.split('-'))
        dt_str_obj = xyz(year, month, day)
        dt_time = x(23, 59, 59)
        dt_end = datetime.combine(dt_str_obj, dt_time)
        end = self.tounixtime(dt_end)
        # print(end)

        print("\nThis is the current availability for Dr {} on your chosen date: ".format(gpLastName[1]))

        self.c.execute("SELECT start, appointmentStatus FROM Appointment WHERE start >=? and end <? and gpEmail =?",
                       [start, end, gpLastName[0]])
        appointments = self.c.fetchall()
        times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
                 "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
        if not appointments:
            for i in times:
                print(i + " available")
        else:
            dict_time_status = {}
            for items in appointments:
                ts = self.toregulartime(items[0])
                string_time = ts.strftime("%H:%M")
                dict_time_status[string_time] = items[1]
            for time in times:
                if time in dict_time_status:
                    print(time + ' ' + dict_time_status[time])
                else:
                    print(time + ' available')


    def chooseTime(self, date, gpLastName):
        print("**********"
              "\n[1] to select a time"
              "\n[2] to select another date"
              "\n[3] to exit to the main menu: ")
        options = int(input("**********"
                            "\nPlease choose from the options above: "))
        if options == 1:
            # # add in error handling, cannot choose time already booked

            time = input("Please choose a time from the available appointments: ")
            day_str = date + ' ' + time
            date_time_obj = datetime.strptime(day_str, '%Y-%m-%d %H:%M')
            start = self.tounixtime(date_time_obj)
            end = start + (30 * 60)

            self.c.execute("SELECT start FROM Appointment WHERE appointmentStatus = 'Pending' and gpEmail =?",
                           [gpLastName[0]])
            booked_times = self.c.fetchall()
            # for i in booked_times:
            #     if start == i[0]:
            #         print("Appointment already booked, please try again: ")

            gpLastName = gpLastName[1]
            gpEmail = gpLastName[0]
            reason = 'Appointment'
            appointmentStatus = 'Pending'
            dateRequested = self.tounixtime(datetime.today())
            patientComplaints = ''
            doctorFindings = ''
            diagnosis = ''
            furtherInspections = ''
            doctorAdvice = ''
            checkIn = None
            checkOut = None

            self.c.execute("INSERT INTO Appointment VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           ([gpEmail, gpLastName, self.patientEmail, start, end, reason, appointmentStatus,
                             dateRequested, patientComplaints, doctorFindings, diagnosis, furtherInspections,
                             doctorAdvice, checkIn, checkOut]))
            self.connection.commit()
            print("You have requested to book an appointment on {} at {}, "
                  "\nyou will receive confirmation of your appointment shortly,".format(date, time))
            if input("Type yes to return to the appointment menu: ").lower() == 'yes':
                self.bookAppointment()

        if options == 2:
            self.chooseDate()
        if options == 3:
            self.returnToAppMenu()

    def cancelAppointment(self):
        print("**********"
              "\nThese are your booked and pending appointment requests: ")
        self.c.execute("SELECT appointmentID, start, gpLastName, appointmentStatus FROM Appointment "
                       "WHERE patientEmail =? ",
                       [self.patientEmail])
        appointments = self.c.fetchall()

        for app in appointments:
            dt = app[1]
            dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
            print("Appointment ID: " + str(app[0]) + "\t" + "date & time: " + dt + "\t\t" + "with: Dr "
                  + app[2] + "\t\t" + "status: " + app[3])

        print("**********"
              "\n[1] To cancel a booked or pending appointment request"
              "\n[2] To exit to the appointment menu"
              "\n**********")
        options = int(input("Please choose from the options above: "))

        if options == 1:
            cancel = input("\nPlease enter the appointment ID you would like to cancel: ")
            self.c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
            self.connection.commit()
            print("You have cancelled your appointment")
            self.returnToAppMenu()

        if options == 2:
            self.returnToAppMenu()

    def viewAppConfirmations(self):
        print("**********"
              "\nThese are your confirmed booked appointments: ")
        self.c.execute("SELECT appointmentID, start, gpLastName FROM Appointment "
                       "WHERE patientEmail =? and appointmentStatus = 'Unavailable' ",
                       [self.patientEmail])
        appointments = self.c.fetchall()

        for app in appointments:
            dt = app[1]
            dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
            print("Appointment ID: " + str(app[0]) + "\t" + "date and time: " + dt + "\t\t" + "with: Dr " + app[2])
        self.returnToAppMenu()

    def returnToAppMenu(self):
        if input("Type yes to return to the appointment menu: ").lower() == 'yes':
            self.bookAppointment()

# ari = Patient("ariannabourke@hotmail.com", "Arianna", "Bourke", "27/04/1988", 10, "male",
#               "123 Happy", "street", "12343", "389753957", "1234")
# ari.register()
# ari.bookAppointment()
# ari.chooseTime()
# y = ari.chooseDate()
# z = ari.chooseAnyDr()
#
# ari.displayAvailable(y, z)



# def toregulartime(unixtimestamp):
#     return datetime.utcfromtimestamp(int(unixtimestamp))
#
#
# def tounixtime(dt):
#     result = int(time.mktime(dt.timetuple()))
#     return result
#
# start_str = '2021-01-01 12:30'
# dt_object = datetime.strptime(start_str, '%Y-%m-%d %H:%M')
# start = tounixtime(dt_object)
#
# end = start + (30 * 60)
# print(toregulartime(end))





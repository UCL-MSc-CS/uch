import sqlite3 as sql
from getpass import getpass
import calendar
import random
from datetime import datetime, timedelta
import time


class Patient:

    def __init__(self, patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2, postcode, telephoneNumber, password):
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
                       (self.patientEmail, self.firstName, self.lastName, self.dateOfBirth, self.age, self.gender, self.addressLine1, self.addressLine2, self.postcode, self.telephoneNumber, self.password, self.loggedIn, self.registrationConfirm))

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

    def toregulartime(self, unixtimestamp):
        return datetime.utcfromtimestamp(int(unixtimestamp))

    def tounixtime(self, dt):
        result = int(time.mktime(dt.timetuple()))
        return result

    def bookAppointment(self):
        print("**********"
              "\n[1] to book an appointment"
              "\n[2] to view your confirmed appointments"
              "\n[3] to cancel an appointment"
              "\n[4] to exit to the main menu: ")
        options = int(input("Please choose from the options above: "))
        if options == 1:
            self.chooseDoctor()

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

        if dr_options == 1:
            self.chooseSpecificDr()
        if dr_options == 2:
            self.chooseAnyDr()
        if dr_options == 3:
            self.chooseDrGender()
        if dr_options == 4:
            self.returnToAppMenu()

    def chooseSpecificDr(self):
        print("**********"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT DISTINCT(gpLastName) FROM GP")
        dr_names = self.c.fetchall()
        gp_list = []
        for dr in dr_names:
            print("Dr", dr[0])
            gp_list.append(dr)
        dr_option1 = input("**********"
                           "\nPlease enter the name of the doctor you would "
                           "like to book an appointment with: ")
        # if dr_option1 not in gp_list:
        #     print("This is not a valid choice of doctor, please try again")
        gpLastName = dr_option1
        return gpLastName

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
            self.chooseMDr()
        if gp_options == 2:
            self.chooseFDr()

    def chooseMDr(self):
        self.c.execute("SELECT gpLastName FROM GP WHERE gpGender = 'M'")
        dr_names = self.c.fetchall()
        gp_list = []
        for dr in dr_names:
            gp_list.append(dr[0])

        gpLastName = random.choice(gp_list)
        print("\nThe male doctor you have been assigned is Dr {}".format(gpLastName))
        return gpLastName

    def chooseFDr(self):
        self.c.execute("SELECT gpLastName FROM GP WHERE gpGender = 'F' ")
        dr_names = self.c.fetchall()
        gp_list = []
        for dr in dr_names:
            gp_list.append(dr[0])

        gpLastName = random.choice(gp_list)
        print("\nThe female doctor you have been assigned is Dr {}".format(gpLastName))
        return gpLastName

    def chooseDate(self, gpLastName):
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

    # def displayAvailable(self, gpLastName, date):
    #     print("\nThis is the current availability for Dr {} on your chosen date: ".format(gpLastName))
        # self.c.execute("SELECT time, bookedStatus FROM Appointment WHERE date =? and gpLastName =?", [date, gpLastName])
        # appointments = self.c.fetchall()
        # times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
        #          "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
        # array = []
        # for time in times:
        #     array.append(time)
        #     for app in appointments:
        #         time1 = (app[0])
        #         status = (app[1])
        #         if time1 == time:
        #             print(time1 + " " + status)
        #         else:
        #             print(time + " available")


    def chooseTime(self, gpLastName, date):
        print("**********"
              "\n[1] to select a time"
              "\n[2] to select another date"
              "\n[3] to exit to the main menu: ")
        options = int(input("**********"
                            "\nPlease choose from the options above: "))
        if options == 1:
            time = input("Please choose a time from the available appointments: ")

            day_str = date + ' ' + time
            date_time_obj = datetime.strptime(day_str, '%Y-%m-%d %H:%M')
            start = self.tounixtime(date_time_obj)
            end = start + (30 * 60)

            # add in error handling

            self.c.execute("SELECT gpEmail FROM GP WHERE gpLastName =?",
                           [gpLastName])
            gpEmails = self.c.fetchall()
            gpEmail = gpEmails[0][0]

            reason = 'Appointment'
            appointmentStatus = 'Pending'
            dateRequested = ''
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

ari = Patient("Arianna", "Bourke", "ariannabourke@hotmail.com", "1234")
ari.bookAppointment()



import sqlite3 as sql
from getpass import getpass
import calendar
import random


class Patient:

    def __init__(self, patientID, firstName, lastName, email, password):
        # added patientID
        self.patientID = patientID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.loggedIn = 1
        self.connection = sql.connect('patient.db')
        self.c = self.connection.cursor()

    def register(self):
        self.c.execute("INSERT INTO PatientDetail VALUES (null,?,?,?,?,?)",
                       (self.firstName, self.lastName, self.email, self.password, self.loggedIn))

    def registrationSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        self.c.execute("SELECT * FROM PatientDetail WHERE firstName =? AND lastName =? AND email =?",
                       [self.firstName, self.lastName, self.email])
        patientDetail = self.c.fetchall()
        for i in patientDetail:
            print("Welcome, " + i[1] + "! Thank you for registering with UCH.")
            print("Patient ID: " + str(i[0]))
            print("First Name: " + i[1])
            print("Last Name: " + i[2])
            print("Email: " + i[3])
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
            self.chooseDoctor()
        if options == 2:
            self.viewAppConfirmations()
        if options == 3:
            self.cancelAppointment()
        if options == 4:
            # exit to main menu
            pass

    def appointmentCalendar(self):
        global gpLastName

        print("----------")
        print(calendar.month(2021, 1))
        print("----------")
        day = int(input("Please select a day in January: "))
        # amend error handling
        if day <= 0 or day > 31:
            day = int(input("This is not a valid day."
                            "\nPlease select a day in January: "))
        date = "{:0>2}/01/2021".format(day)

        print()
        print("This is the current availability for Dr {} on your chosen date: ".format(gpLastName))
        self.c.execute("SELECT time, bookedStatus FROM Appointment WHERE date =? and gpLastName =? "
                       "and gpAvailability != 'unavailable'",
                       [date, gpLastName])
        appointments = self.c.fetchall()
        for app in appointments:
            print(app[0] + "\t\t" + app[1])

        print("**********"
              "\n[1] to select a time"
              "\n[2] to select another date"
              "\n[3] to exit to the main menu: ")
        options = int(input("**********"
                            "\nPlease choose from the options above: "))
        if options == 1:
            time = input("Please choose a time from the available appointments: ")
            # add in error handling
            chosen = [self.patientID, time, date, gpLastName]
            self.c.execute("""UPDATE Appointment SET bookedStatus = 'Booked', patientID =?
                            WHERE time =? and date=? and gpLastName =?""", chosen)
            self.connection.commit()
            print("You have requested to book an appointment on {} at {}, "
                  "you will receive confirmation of your appointment shortly.".format(date, time))
            if input("Type yes to return to the appointment menu: ").lower() == 'yes':
                self.bookAppointment()

        if options == 2:
            self.appointmentCalendar()

        if options == 3:
            self.bookAppointment()
            pass

    def chooseDoctor(self):
        global gpLastName

        print("**********"
              "\n[1] To book an appointment with a specific doctor"
              "\n[2] To book an appointment with any doctor"
              "\n[3] To book an appointment with a doctor of a specific gender"
              "\n[4] To exit to the main menu"
              "\n**********")
        dr_options = int(input("Please choose from the options above: "))

        # select specific dr
        if dr_options == 1:
            print("**********"
                  "\nThe doctors currently available at the practice are: ")
            self.c.execute("SELECT DISTINCT(gpLastName) FROM Appointment")
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
            self.appointmentCalendar()

        # random doctor
        if dr_options == 2:
            self.c.execute("SELECT DISTINCT(gpLastName) FROM Appointment")
            dr_names = self.c.fetchall()
            gp_list = []
            for dr in dr_names:
                gp_list.append(dr[0])

            gpLastName = random.choice(gp_list)
            print("The doctor you have been assigned is Dr {}".format(gpLastName))
            self.appointmentCalendar()

        # doctor of specific gender
        if dr_options == 3:
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
                print()
                print("The male doctor you have been assigned is Dr {}".format(gpLastName))
                self.appointmentCalendar()

            if gp_options == 2:
                self.c.execute("SELECT gpLastName FROM GP WHERE gpGender = 'F' ")
                dr_names = self.c.fetchall()
                gp_list = []
                for dr in dr_names:
                    gp_list.append(dr[0])

                gpLastName = random.choice(gp_list)
                print(gpLastName)
                print("The female doctor you have been assigned is Dr {}".format(gpLastName))
                self.appointmentCalendar()

        if dr_options == 4:
            self.bookAppointment()
            pass

    def cancelAppointment(self):
        print("**********"
              "\nThese are your booked appointments: ")
        self.c.execute("SELECT appointmentID, date, time, gpLastName FROM Appointment WHERE patientID =?",
                       [self.patientID])
        appointments = self.c.fetchall()
        for app in appointments:
            print("Appointment ID: " + str(app[0]) + "\t" + "date: " + app[1] + "\t"
                  + "time: " + app[2] + "\t\t" + "with: Dr " + app[3])

        print("**********"
              "\n[1] To cancel an appointment"
              "\n[2] To exit to the main menu"
              "\n**********")
        options = int(input("Please choose from the options above: "))

        print()
        if options == 1:
            cancel = input("Please enter the appointment ID you would like to cancel: ")
            self.c.execute("UPDATE Appointment SET bookedStatus = 'Available', patientID = '' "
                           "WHERE appointmentID =?", [cancel])
            self.connection.commit()
            print("You have cancelled your appointment")
            if input("Type yes to return to the appointment menu: ").lower() == 'yes':
                self.bookAppointment()
        if options == 2:
            self.bookAppointment()

    def viewAppConfirmations(self):
        print("**********"
              "\nThese are your booked appointments: ")
        self.c.execute("SELECT appointmentID, date, time, gpLastName FROM Appointment WHERE patientID =?",
                       [self.patientID])
        appointments = self.c.fetchall()
        for app in appointments:
            print("Appointment ID: " + str(app[0]) + "\t" + "date: " + app[1] + "\t"
                  + "time: " + app[2] + "\t\t" + "with: Dr " + app[3])
        if input("Type yes to return to the appointment menu: ").lower() == 'yes':
            self.bookAppointment()

    # not a real function, just sets one appointment to unavailable for testing
    def checkDrAvailable(self):
        self.c.execute("""UPDATE Appointment SET drAvailability = 'unavailable'
                        WHERE time ='11:30' and date='01/01/2021' and gpLastName ='Shepherd'""")
        self.connection.commit()
        pass



ari = Patient(1, "Arianna", "Bourke", "ariannabourke@hotmail.com", "1234")
ari.bookAppointment()
# ari.cancelAppointment()
# ari.viewAppConfirmations()
# ari.checkDrAvailable()

# conn = sql.connect('patient.db')
# c = conn.cursor()
# c.execute("SELECT * FROM Appointment WHERE patientID = '1'")
# print(c.fetchall())


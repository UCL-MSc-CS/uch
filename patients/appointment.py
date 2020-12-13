import sqlite3 as sql
import calendar
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
# import patients.patientFunctions as pf
import patientFunctions as pf


class Appointment:

    def __init__(self):
        self.connection = sql.connect('patient.db')
        self.c = self.connection.cursor()

    def bookAppointment(self, patientEmail):
        print("**********"
              "\n[1] To book an appointment with a specific doctor"
              "\n[2] To book an appointment with any doctor"
              "\n[3] To book an appointment with a doctor of a specific gender"
              "\n[0] To exit to the main menu"
              "\n**********")
        dr_options = input("Please choose from the options above: ")
        if dr_options == '1':
            y = self.chooseSpecificDr(patientEmail)
            self.chooseAppointment(patientEmail, y)
        elif dr_options == '2':
            y = self.chooseAnyDr(patientEmail)
            self.chooseAppointment(patientEmail, y)
        elif dr_options == '3':
            y = self.chooseDrGender(patientEmail)
            self.chooseAppointment(patientEmail, y)
        elif dr_options == '0':
            pf.returnToMain()
        else:
            print("This is not a valid option, please try again")
            self.bookAppointment(patientEmail)

    def chooseSpecificDr(self, patientEmail):
        print("**********"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        gpDetails = pf.chooseDr(dr_names)
        return gpDetails

    def chooseAnyDr(self, patientEmail):
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        gp_list = []
        for dr in dr_names:
            gp_list.append(dr)
        gpchoice = random.choice(gp_list)
        gp_chosen_email = gpchoice[2]
        gp_chosen_name = gpchoice[1]
        gpDetails = [gp_chosen_email, gp_chosen_name]

        print("The doctor you have been assigned is Dr {}".format(gp_chosen_name))
        return gpDetails

    def chooseDrGender(self, patientEmail):
        print("**********"
              "\n[1] To book an appointment with a male doctor"
              "\n[2] to book an appointment with a female doctor"
              "\n[3] to book an appointment with a non-binary doctor")
        gp_options = input("Please choose from the options above: ")
        if gp_options == '1':
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        elif gp_options == '2':
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        elif gp_options == '3':
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        else:
            print("This is not a valid option, please try again")
            self.chooseDrGender(patientEmail)

    def chooseAppointment(self, patientEmail, gpDetails):
        print("**********"
              "\n [1] January     \t[2] February      \t[3] March"
              "\n [4] April     \t\t[5] May           \t[6] June"
              "\n [7] July      \t\t[8] August        \t[9] September "
              "\n [10] October    \t[11] November     \t[12] December")
        month = pf.chooseMonth()
        date = pf.chooseDate(month)

        print("\nThis is the current availability for Dr {} on your chosen date: ".format(gpDetails[1]))
        start = pf.generateStartTime(date)
        end = pf.generateEndTime(date)
        times = pf.displayAvailable(start, end, gpDetails)

        print("**********"
              "\n[1] to select a time"
              "\n[2] to select another date"
              "\n[3] to exit to the main menu ")
        options = input("\nPlease choose from the options above: ")
        if options == '1':
            time = pf.chooseTime(date, times, gpDetails)
            start = pf.createStart(date, time)
            pf.InsertAppointment(start, gpDetails, patientEmail)
            print("You have requested to book an appointment on {} at {}, "
                  "\nYou will receive confirmation of your appointment shortly!".format(date, time))
            pf.returnToMain()
        elif options == '2':
            self.chooseDate(patientEmail, gpDetails)
        elif options == '3':
            pf.returnToMain()
        else:
            print("This is not a valid option, please try again")
            self.chooseAppointment(patientEmail, gpDetails)
            ## change this

    def cancelAppointment(self, patientEmail):
        print("**********"
              "\nThese are your confirmed booked appointments: ")
        pf.viewAppointments(patientEmail)
        print("**********"
              "\n[1] To cancel an appointment"
              "\n[2] To exit to the main menu"
              "\n**********")
        options = input("Please choose from the options above: ")
        if options == '1':
            cancel = input("\nPlease enter the appointment ID you would like to cancel: ")
            pf.deleteAppointment(cancel)
            pf.returnToMain()
        elif options == '2':
            pf.returnToMain()
        else:
            print("This is not a valid option, please try again")
            self.cancelAppointment(patientEmail)

    def viewAppConfirmations(self, patientEmail):
        print("**********"
              "\nThese are your confirmed booked appointments: ")
        pf.viewAppointments(patientEmail)
        pf.returnToMain()


Ari = Appointment()
Ari.bookAppointment('ariannabourke@hotmail.com')




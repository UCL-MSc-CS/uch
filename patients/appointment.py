import sqlite3 as sql
import calendar
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
import patients.patientFunctions as pf


class Appointment:

    def __init__(self):
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()

    def bookAppointment(self, patientEmail):
        print("**********"
              "\n[1] To book an appointment with a specific doctor"
              "\n[2] To book an appointment with any doctor"
              "\n[3] To book an appointment with a doctor of a specific gender"
              "\n[0] To exit to the main menu"
              "\n**********")
        dr_options = int(input("Please choose from the options above: "))

        if dr_options == 1:
            y = self.chooseSpecificDr(patientEmail)
            self.chooseDate(patientEmail, y)

        if dr_options == 2:
            y = self.chooseAnyDr(patientEmail)
            self.chooseDate(patientEmail, y)

        if dr_options == 3:
            y = self.chooseDrGender(patientEmail)
            self.chooseDate(patientEmail, y)

        if dr_options == 0:
            if input("Type yes to return to the main menu: ").lower() == 'yes':
                pass
            else:
                print("Thank you for using the UCH e-health system! Goodbye for now!")
                exit()

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
        gp_options = int(input("Please choose from the options above: "))

        if gp_options == 1:
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        if gp_options == 2:
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        if gp_options == 3:
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails

    def chooseDate(self, patientEmail, gpDetails):
        print("**********"
              "\n [1] January     \t[2] February      \t[3] March"
              "\n [4] April     \t\t[5] May           \t[6] June"
              "\n [7] July      \t\t[8] August        \t[9] September "
              "\n [10] October    \t[11] November     \t[12] December")
        mm = int(input("Please choose the month would you would like your appointment in 2021: "))
        date = pf.printCalendar(mm)

        print("\nThis is the current availability for Dr {} on your chosen date: ".format(gpDetails[1]))
        start_obj = pf.toDateObjApp00(date)
        start_t = pf.tounixtime(start_obj)
        end = pf.generateEndTime(date)

        pf.displayAvailable(start_t, end, gpDetails)

        print("**********"
              "\n[1] to select a time"
              "\n[2] to select another date"
              "\n[3] to exit to the main menu ")
        options = int(input("**********"
                            "\nPlease choose from the options above: "))
        if options == 1:
            time = input("Please choose a time from the available appointments: ")
            day_str = date + ' ' + time
            dt_object = pf.toDateTimeObj(day_str)
            start = pf.tounixtime(dt_object)

            pf.chooseTime(start, gpDetails, patientEmail)
            print("You have requested to book an appointment on {} at {}, "
                  "\nyou will receive confirmation of your appointment shortly!".format(date, time))
            if input("Type yes to return to the main menu: ").lower() == 'yes':
                pass
            else:
                print("Thank you for using the UCH e-health system! Goodbye for now!")
                exit()

        if options == 2:
            self.chooseDate(patientEmail, gpDetails)
        if options == 3:
            if input("Type yes to return to the main menu: ").lower() == 'yes':
                pass
            else:
                print("Thank you for using the UCH e-health system! Goodbye for now!")
                exit()

    def cancelAppointment(self, patientEmail):
        print("**********"
              "\nThese are your confirmed booked appointments: ")
        pf.viewAppointments(patientEmail)

        print("**********"
              "\n[1] To cancel an appointment"
              "\n[2] To exit to the main menu"
              "\n**********")
        options = int(input("Please choose from the options above: "))

        if options == 1:
            cancel = input("\nPlease enter the appointment ID you would like to cancel: ")
            self.c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
            self.connection.commit()
            print("You have cancelled your appointment")
            if input("Type yes to return to the main menu: ").lower() == 'yes':
                pass
            else:
                print("Thank you for using the UCH e-health system! Goodbye for now!")
                exit()

        if options == 2:
            if input("Type yes to return to the main menu: ").lower() == 'yes':
                pass
            else:
                print("Thank you for using the UCH e-health system! Goodbye for now!")
                exit()

    def viewAppConfirmations(self, patientEmail):
        print("**********"
              "\nThese are your confirmed booked appointments: ")
        pf.viewAppointments(patientEmail)
        if input("Type yes to return to the main menu: ").lower() == 'yes':
            pass
        else:
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()




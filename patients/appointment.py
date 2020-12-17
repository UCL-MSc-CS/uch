import sqlite3 as sql
import calendar
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
import patients.patientFunctions as pf
import patients.viewCancelFunctions as vc


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class emptyAnswer(Error):
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class invalidAnswer(Error):
    def __init__(self, message="\n\t< This is not a valid answer, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class Appointment:

    def __init__(self):
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()

    def bookAppointment(self, nhsNumber):
        """ Prints appointment menu for user to choose by doctor type"""
        try:
            print("********************************************"
                  "\nChoose [1] to book an appointment with a specific doctor"
                  "\nChoose [2] to book an appointment with any doctor"
                  "\nChoose [3] to book an appointment with a doctor of a specific gender"
                  "\nChoose [0] to exit to the main menu"
                  "\n********************************************")
            dr_options = input("Please select an option: ")
            if dr_options == '':
                raise emptyAnswer()
            elif dr_options == '1':
                y = self.chooseSpecificDr(nhsNumber)
                self.chooseAppointment(nhsNumber, y)
            elif dr_options == '2':
                y = self.chooseAnyDr(nhsNumber)
                self.chooseAppointment(nhsNumber, y)
            elif dr_options == '3':
                y = self.chooseDrGender(nhsNumber)
                self.chooseAppointment(nhsNumber, y)
            elif dr_options == '0':
                pf.returnToMain()
            else:
                raise invalidAnswer()
        except invalidAnswer:
            error = invalidAnswer()
            print(error)
            self.bookAppointment(nhsNumber)
        except emptyAnswer:
            error = emptyAnswer()
            print(error)
            self.bookAppointment(nhsNumber)

    def chooseSpecificDr(self, nhsNumber):
        """ Allows user to choose a specific doctor from a list from all doctors registered
        :return: gpDetails (list) with gp last name and email address"""
        print("**********"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        if dr_names == []:
            print("\nThere are no doctors currently available at the practice"
                  "\n")
            pf.returnToMain()
        else:
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails

    def chooseAnyDr(self, nhsNumber):
        """ Assigns user any doctor from a list from all doctors registered
        :return: gpDetails (list) with gp last name and email address"""
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        if dr_names == []:
            print("\nThere are no doctors currently available at the practice"
                  "\n")
            pf.returnToMain()
        else:
            gp_list = []
            for dr in dr_names:
                gp_list.append(dr)
            gpchoice = random.choice(gp_list)
            gp_chosen_email = gpchoice[2]
            gp_chosen_name = gpchoice[1]
            gpDetails = [gp_chosen_email, gp_chosen_name]
            print("The doctor you have been assigned is Dr {}".format(gp_chosen_name))
            return gpDetails

    def chooseDrGender(self, nhsNumber):
        """ Allows user to choose a doctor by gender from a list from all doctors registered
        :return: gpDetails (list) with gp last name and email address"""
        try:
            print("********************************************"
                  "\nChoose [1] to book an appointment with a male doctor"
                  "\nChoose [2] to book an appointment with a female doctor"
                  "\nChoose [3] to book an appointment with a non-binary doctor"
                  "\n********************************************")
            gp_options = input("Please select an option: ")
            if gp_options == '':
                raise emptyAnswer()
            if gp_options == '1':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' ")
                dr_names = self.c.fetchall()
                if dr_names == []:
                    print("\nThere are no male doctors currently available at the practice"
                          "\n")
                    self.bookAppointment(nhsNumber)
                else:
                    gpDetails = pf.chooseDr(dr_names)
                    return gpDetails
            elif gp_options == '2':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' ")
                dr_names = self.c.fetchall()
                if dr_names == []:
                    print("\nThere are no female doctors currently available at the practice"
                          "\n")
                    self.bookAppointment(nhsNumber)
                else:
                    gpDetails = pf.chooseDr(dr_names)
                    return gpDetails
            elif gp_options == '3':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' ")
                dr_names = self.c.fetchall()
                if dr_names == []:
                    print("\nThere are no non-binary doctors currently available at the practice"
                          "\n")
                    self.bookAppointment(nhsNumber)
                else:
                    gpDetails = pf.chooseDr(dr_names)
                    return gpDetails
            else:
                raise invalidAnswer()
        except invalidAnswer:
            error = invalidAnswer()
            print(error)
            self.chooseDrGender(nhsNumber)
        except emptyAnswer:
            error = emptyAnswer()
            print(error)
            self.chooseDrGender(nhsNumber)

    def chooseAppointment(self, nhsNumber, gpDetails):
        """ Allows user to to book an appointment
        User can choose the month and day
        User then presented with a list of all appointments on that day by time
        User can then choose which time they would like the appointment
        appointment details inserted into the database for chosen date and time for this user"""
        year = pf.chooseYear()
        print("********************************************"
              "\n [1] January     \t[2] February      \t[3] March"
              "\n [4] April     \t\t[5] May           \t[6] June"
              "\n [7] July      \t\t[8] August        \t[9] September "
              "\n [10] October    \t[11] November     \t[12] December"
              "\n********************************************")
        month = pf.chooseMonth(year)
        date = pf.chooseDate(month, year)
        print("\nThis is the current availability for Dr {} on your chosen date: ".format(gpDetails[1]))
        start = pf.generateStartTime(date)
        end = pf.generateEndTime(date)
        times = pf.displayAvailable(start, end, gpDetails)
        pf.timeMenu(date, times, gpDetails, nhsNumber)

    def cancelAppointment(self, nhsNumber):
        """ Presents user with all their appointments and allows them to cancel"""
        print("********************************************"
              "\nThese are your confirmed booked appointments: ")
        viewing = vc.viewAppointments(nhsNumber)
        if viewing == 0:
            print("You cannot cancel any appointments at this time")
            pf.returnToMain()
        else:
            try:
                print("********************************************"
                      "\nChoose [1] to cancel an appointment"
                      "\nChoose [0] to exit to the main menu"
                      "\n********************************************")
                options = input("Please select an option: ")
                if options == '':
                    raise emptyAnswer()
                elif options == '1':
                    cancel = vc.checkAppID(nhsNumber)
                    vc.deleteAppointment(cancel)
                    pf.returnToMain()
                elif options == '0':
                    pf.returnToMain()
                else:
                    raise invalidAnswer()
            except invalidAnswer:
                error = invalidAnswer()
                print(error)
                self.cancelAppointment(nhsNumber)
            except emptyAnswer:
                error = emptyAnswer()
                print(error)
                self.cancelAppointment(nhsNumber)


    def viewAppConfirmations(self, nhsNumber):
        """ Presents user with all their confirmed booked appointments"""
        print("********************************************"
              "\nThese are your confirmed/pending appointments: ")
        vc.viewAppointments(nhsNumber)
        # pf.returnToMain()

#
# Ari = Appointment()
# Ari.bookAppointment(1234567890)




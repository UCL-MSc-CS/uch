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


class EmptyAnswer(Error):
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class InvalidAnswer(Error):
    def __init__(self, message="\n\t< This is not a valid answer, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class Appointment:

    def __init__(self):
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()

    def book_appointment(self, nhs_number):
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
                raise EmptyAnswer()
            elif dr_options == '1':
                y = self.choose_specific_dr(nhs_number)
                self.choose_appointment(nhs_number, y)
            elif dr_options == '2':
                y = self.choose_any_dr(nhs_number)
                self.choose_appointment(nhs_number, y)
            elif dr_options == '3':
                y = self.choose_dr_gender(nhs_number)
                self.choose_appointment(nhs_number, y)
            elif dr_options == '0':
                pass
            else:
                raise InvalidAnswer()
        except InvalidAnswer:
            error = InvalidAnswer()
            print(error)
            self.book_appointment(nhs_number)
        except EmptyAnswer:
            error = EmptyAnswer()
            print(error)
            self.book_appointment(nhs_number)

    def choose_specific_dr(self, nhs_number):
        """ Allows user to choose a specific doctor from a list from all doctors registered
        :return: gp_details (list) with gp last name and email address"""
        print("********************************************"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        if dr_names == []:
            print("\nThere are no doctors currently available at the practice"
                  "\n")
            pf.return_to_main()
        else:
            gp_details = pf.choose_dr(dr_names)
            return gp_details

    def choose_any_dr(self, nhs_number):
        """ Assigns user any doctor from a list from all doctors registered
        :return: gp_details (list) with gp last name and email address"""
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        if dr_names == []:
            print("\nThere are no doctors currently available at the practice"
                  "\n")
            pf.return_to_main()
        else:
            gp_list = []
            for dr in dr_names:
                gp_list.append(dr)
            gp_choice = random.choice(gp_list)
            gp_chosen_email = gp_choice[2]
            gp_chosen_name = gp_choice[1]
            gp_details = [gp_chosen_email, gp_chosen_name]
            print("The doctor you have been assigned is Dr {}".format(gp_chosen_name))
            return gp_details

    def choose_dr_gender(self, nhs_number):
        """ Allows user to choose a doctor by gender from a list from all doctors registered
        :return: gp_details (list) with gp last name and email address"""
        try:
            print("********************************************"
                  "\nChoose [1] to book an appointment with a male doctor"
                  "\nChoose [2] to book an appointment with a female doctor"
                  "\nChoose [3] to book an appointment with a non-binary doctor"
                  "\nChoose [0] to exit to the main menu"
                  "\n********************************************")
            gp_options = input("Please select an option: ")
            if gp_options == '':
                raise EmptyAnswer()
            if gp_options == '1':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' ")
                dr_names = self.c.fetchall()
                if dr_names == []:
                    print("\nThere are no male doctors currently available at the practice"
                          "\n")
                    self.book_appointment(nhs_number)
                else:
                    gp_details = pf.choose_dr(dr_names)
                    return gp_details
            elif gp_options == '2':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' ")
                dr_names = self.c.fetchall()
                if dr_names == []:
                    print("\nThere are no female doctors currently available at the practice"
                          "\n")
                    self.book_appointment(nhs_number)
                else:
                    gp_details = pf.choose_dr(dr_names)
                    return gp_details
            elif gp_options == '3':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' ")
                dr_names = self.c.fetchall()
                if dr_names == []:
                    print("\nThere are no non-binary doctors currently available at the practice"
                          "\n")
                    self.book_appointment(nhs_number)
                else:
                    gp_details = pf.choose_dr(dr_names)
                    return gp_details
            elif gp_options == '0':
                pass
            else:
                raise InvalidAnswer()
        except InvalidAnswer:
            error = InvalidAnswer()
            print(error)
            self.choose_dr_gender(nhs_number)
        except EmptyAnswer:
            error = EmptyAnswer()
            print(error)
            self.choose_dr_gender(nhs_number)

    def choose_appointment(self, nhs_number, gp_details):
        """ Allows user to to book an appointment
        User can choose the month and day
        User then presented with a list of all appointments on that day by time
        User can then choose which time they would like the appointment
        appointment details inserted into the database for chosen date and time for this user"""
        year = pf.choose_year()
        print("********************************************"
              "\n [1] January     \t[2] February      \t[3] March"
              "\n [4] April     \t\t[5] May           \t[6] June"
              "\n [7] July      \t\t[8] August        \t[9] September "
              "\n [10] October    \t[11] November     \t[12] December"
              "\n********************************************")
        month = pf.choose_month(year)
        date = pf.choose_date(month, year)
        print("\nThis is the current availability for Dr {} on your chosen date: ".format(gp_details[1]))
        start = pf.generate_start_time(date)
        end = pf.generate_end_time(date)
        times = pf.display_available(start, end, gp_details)
        done = pf.time_menu(date, times, gp_details, nhs_number)
        if done == 0:
            pass

    def cancel_appointment(self, nhs_number):
        """ Presents user with all their appointments and allows them to cancel"""
        print("********************************************"
              "\nThese are your confirmed booked appointments: ")
        viewing = vc.view_appointments(nhs_number)
        if viewing == 0:
            print("You cannot cancel any appointments at this time")
            pf.return_to_main()
        else:
            try:
                print("\nChoose [1] to cancel an appointment"
                      "\nChoose [0] to exit to the main menu"
                      "\n********************************************")
                options = input("Please select an option: ")
                if options == '':
                    raise EmptyAnswer()
                elif options == '1':
                    cancel = vc.check_app_id(nhs_number)
                    vc.delete_appointment(cancel)
                    pf.return_to_main()
                elif options == '0':
                    pass
                else:
                    raise InvalidAnswer()
            except InvalidAnswer:
                error = InvalidAnswer()
                print(error)
                self.cancel_appointment(nhs_number)
            except EmptyAnswer:
                error = EmptyAnswer()
                print(error)
                self.cancel_appointment(nhs_number)

    def view_app_confirmations(self, nhs_number):
        """ Presents user with all their confirmed booked appointments"""
        print("********************************************"
              "\nThese are your appointments: ")
        vc.view_appointments(nhs_number)
        pf.return_to_main()




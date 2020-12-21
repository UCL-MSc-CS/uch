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
    """ Raised when input field left empty"""
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class InvalidAnswer(Error):
    """ Raised when input entered is not valid """
    def __init__(self, message="\n\t< This is not a valid answer, please try again >"
                               "\n"):
        self.message = message
        super().__init__(self.message)


class Appointment:

    def __init__(self):
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()

    def book_appointment(self, nhs_number):
        """ Prints appointment menu for user to choose a doctor
        User can choose to book with a specific doctor, any doctor chosen at random by the system
        or a doctor of a specific gender"""
        try:
            print("--------------------------------------------"
                  "\n         Patient Appointment Menu"
                  "\n--------------------------------------------"
                  "\nChoose [1] to book an appointment with a specific doctor"
                  "\nChoose [2] to book an appointment with any doctor"
                  "\nChoose [3] to book an appointment with a doctor of a specific gender"
                  "\nChoose [0] to exit to the main patient menu"
                  "\n********************************************")
            dr_options = input("Please select an option: ")
            if dr_options == '':
                raise EmptyAnswer()
            elif dr_options == '1':
                y = self.choose_specific_dr()
                if y == 0:
                    pass
                else:
                    self.choose_appointment(nhs_number, y)
            elif dr_options == '2':
                y = self.choose_any_dr()
                if y == 0:
                    pass
                else:
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

    def choose_specific_dr(self):
        """ Allows user to choose a specific doctor from a list from all doctors registered
        :return: gp_details (list) with gp last name and email address"""
        print("********************************************"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE active='1'")
        dr_names = self.c.fetchall()
        if not dr_names:
            print("\nThere are no doctors currently available at the practice"
                  "\n")
            return 0
        else:
            gp_details = pf.choose_dr(dr_names)
            return gp_details

    def choose_any_dr(self):
        """ Assigns user a doctor at random from a list from all doctors registered
        :return: gp_details (list) with gp last name and email address"""
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE active='1'")
        dr_names = self.c.fetchall()
        if not dr_names:
            print("\nThere are no doctors currently available at the practice"
                  "\n")
            return 0
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
        """ Allows user to choose a doctor by gender (male, female, non-binary) from a list from all doctors registered
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
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' and active='1'")
                dr_names = self.c.fetchall()
                if not dr_names:
                    print("\nThere are no male doctors currently available at the practice"
                          "\n")
                    self.book_appointment(nhs_number)
                else:
                    gp_details = pf.choose_dr(dr_names)
                    return gp_details
            elif gp_options == '2':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' and active='1'")
                dr_names = self.c.fetchall()
                if not dr_names:
                    print("\nThere are no female doctors currently available at the practice"
                          "\n")
                    self.book_appointment(nhs_number)
                else:
                    gp_details = pf.choose_dr(dr_names)
                    return gp_details
            elif gp_options == '3':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' and active='1'")
                dr_names = self.c.fetchall()
                if not dr_names:
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
        User can choose the year, month and day
        User then presented with a list of all appointments on that day by time and shows availability
        User can then choose which time they would like the appointment
        appointment details inserted into the database for chosen date and time for this user"""
        year = pf.choose_year()
        if year == 0:
            self.book_appointment(nhs_number)
        else:
            month = pf.choose_month(year)
            if month == 0:
                self.choose_appointment(nhs_number, gp_details)
            else:
                date = pf.choose_date(month, year)
                if date == 0:
                    self.choose_appointment(nhs_number, gp_details)
                else:
                    start = pf.generate_start_time(date)
                    end = pf.generate_end_time(date)
                    times_str = pf.display_available(date, start, end, gp_details)
                    chosen_time = pf.choose_time(date, times_str, gp_details)
                    if chosen_time == 0:
                        self.choose_appointment(nhs_number, gp_details)
                    else:
                        start = pf.create_start(date, chosen_time)
                        pf.insert_appointment(start, gp_details, nhs_number)
                        print("\nYou have requested to book an appointment on {} at {}, "
                              "\nYou will receive confirmation of your appointment "
                              "shortly!"
                              "\nYou can check all of your appointments through "
                              "'view your appointments' in the main menu\n".format(date, chosen_time))
                        pass

    def cancel_appointment(self, nhs_number):
        """ Presents user with all their appointments and allows them to choose to cancel one"""
        print("--------------------------------------------"
              "\n         Patient: Cancel Appointments"
              "\n--------------------------------------------"
              "\nYour appointments: ")
        viewing = vc.view_appointments(nhs_number)
        if viewing == 0:
            print("You cannot cancel any appointments at this time")
            pf.return_to_main()
        else:
            try:
                print("Choose [1] to cancel an appointment"
                      "\nChoose [0] to exit to the main menu"
                      "\n********************************************")
                options = input("Please select an option: ")
                if options == '':
                    raise EmptyAnswer()
                elif options == '0':
                    pass
                elif options == '1':
                    cancel = vc.check_app_id(nhs_number)
                    if cancel == 0:
                        pass
                    else:
                        vc.delete_appointment(cancel)
                        print("\nWould you like to cancel another appointment?"
                              "\nChoose [1] to cancel an appointment"
                              "\nChoose [0] to exit to the main menu"
                              "\n********************************************")
                        choice = input("Please select an option: ")
                        if choice == '1':
                            self.cancel_appointment(nhs_number)
                        elif choice == '0':
                            pass
                        else:
                            raise InvalidAnswer()
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
        """ Presents user with all their pending, accepted and declined appointments"""
        print("--------------------------------------------"
              "\n         Patient: View Appointments"
              "\n--------------------------------------------"
              "\nYour appointments: ")
        vc.view_appointments(nhs_number)
        pf.return_to_main()




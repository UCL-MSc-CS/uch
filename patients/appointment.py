import sqlite3 as sql
import random
import patients.patient_functions as pf
import patients.view_cancel_functions as vc

"""
This module contains the Appointment class for the patient to navigate to book an appointment.

Error classes contain exception handling for user input in the functions.
The Appointment class contains functions to navigate through menus, calling other functions (from patient_functions.py)
to choose a doctor, year, month, day and time for an appointment. 
Patient can also navigate to view all their booked appointments and cancel an appointment.
"""


class Error(Exception):
    """Error exception base class."""
    pass


class EmptyAnswerError(Error):
    """
    Error class for when an input is left empty.

    Attributes:
        message (str): Message is raised when the patient presses enter with no input.
    """
    def __init__(self, message="\n\t< This field cannot be left empty, please try again >\n"):
        """
        The constructor for EmptyAnswerError class.

        Parameters:
            message (str): Message is raised when the patient presses enter with no input.
        """
        self.message = message
        super().__init__(self.message)


class InvalidAnswerError(Error):
    """
    Error class for when an input is not valid.

    Attributes:
        message (str): Message is raised when the patient enters a string that is not valid to requirements.
    """
    def __init__(self, message="\n\t< This is not a valid answer, please try again >\n"):
        """
        The constructor for InvalidAnswerError class.

        Parameters:
            message (str): Message is raised when the patient enters a string that is not valid to requirements.
        """
        self.message = message
        super().__init__(self.message)


class Appointment:
    """ Class for booking appointments. """

    def __init__(self):
        """
        The constructor for Appointment class.

        Opens the connection and cursor for the UCH database.
        """
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()

    def book_appointment(self, nhs_number):
        """
        Main appointment menu for patient to choose a doctor to book an appointment with.

        Prints appointment menu for user to choose to book with a specific doctor, any doctor
        or a doctor of a specific gender. Function then links to other appropriate functions in order to
        choose a doctor name, then to choose appointment date and time.
        Exceptions prevent the input from being empty or a number which is not valid in the list of choices.

        Parameters:
            nhs_number (int): Patient's nhs number.
        """
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
                raise EmptyAnswerError()
            # to book appointment with specific dr
            elif dr_options == '1':
                y = self.choose_specific_dr()
                if y == 0:
                    pass
                else:
                    self.choose_appointment(nhs_number, y)
            # to book appointment with any dr
            elif dr_options == '2':
                y = self.choose_any_dr()
                if y == 0:
                    pass
                else:
                    self.choose_appointment(nhs_number, y)
            # to book appointment with a dr of specific gender
            elif dr_options == '3':
                y = self.choose_dr_gender(nhs_number)
                if y == 0:
                    pass
                else:
                    self.choose_appointment(nhs_number, y)
            # exit to patient menu
            elif dr_options == '0':
                pass
            else:
                raise InvalidAnswerError()
        except InvalidAnswerError:
            error = InvalidAnswerError()
            print(error)
            self.book_appointment(nhs_number)
        except EmptyAnswerError:
            error = EmptyAnswerError()
            print(error)
            self.book_appointment(nhs_number)

    def choose_specific_dr(self):
        """
        Function for patient to choose a specific doctor.

        Creates a list of all doctors first names, last names and email addresses from all that are listed as active.
        If the list is empty, prints a message to say there are no doctors available and returns 0. Otherwise,
        links to the choose_dr function for patient to choose a gp from the list and returns gp_details.

        Returns:
            gp_details (list): list of chosen doctor email and last name.
            or 0 (int): To return to the menu.
        """
        print("********************************************"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE active='1'")
        dr_names = self.c.fetchall()
        # when list returned empty, there are no doctors available, patient returned to main menu
        if not dr_names:
            print("\nI'm sorry, there are no doctors currently available at the practice,"
                  "\nplease try again another time\n")
            return 0
        else:
            gp_details = pf.choose_dr(dr_names)
            self.connection.close()
            return gp_details

    def choose_any_dr(self):
        """
        Function for patient to be assigned to any doctor.

        Creates a list of all doctors first names, last names and email addresses from all that are listed as active.
        If the list is empty, prints a message to say there are no doctors available and returns 0.
        Otherwise, one doctor is chosen at random from the list and gp_details are returned.

        Returns:
            gp_details (list): list of chosen doctor email and last name.
            or 0 (int): To return to the menu.
        """
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE active='1'")
        dr_names = self.c.fetchall()
        # when list returned empty, there are no doctors available, patient returned to main menu
        if not dr_names:
            print("\nI'm sorry, there are no doctors currently available at the practice"
                  "\n")
            return 0
        else:
            gp_list = []
            for dr in dr_names:
                gp_list.append(dr)
            # dr chosen at random from gp_list
            gp_choice = random.choice(gp_list)
            gp_chosen_email = gp_choice[2]
            gp_chosen_name = gp_choice[1]
            # list of gp email and last name created
            gp_details = [gp_chosen_email, gp_chosen_name]
            print("The doctor you have been assigned is Dr {}".format(gp_chosen_name))
            self.connection.close()
            return gp_details

    def choose_dr_gender(self, nhs_number):
        """
        Function for patient to choose a doctor by gender.

        Prints a menu for patient to choose to book with a male, female or non-binary doctor.
        Exceptions prevent the input from being empty or a number which is not valid in the list of choices.

        For chosen gender, creates a list of all doctors first names, last names and email addresses from all
        that are listed as active. If the list is empty, prints a message to say there are no doctors available
        and returns 0.
        Otherwise, links to the choose_dr function for patient to choose a gp from the list and returns gp_details.

        Parameters:
            nhs_number (int): Patient's nhs number.
        Returns:
            gp_details (list): list of chosen doctor email and last name.
            or 0 (int): To return to the menu.
        """
        try:
            print("********************************************"
                  "\nChoose [1] to book an appointment with a male doctor"
                  "\nChoose [2] to book an appointment with a female doctor"
                  "\nChoose [3] to book an appointment with a non-binary doctor"
                  "\nChoose [0] to exit to the main menu"
                  "\n********************************************")
            gp_options = input("Please select an option: ")
            if gp_options == '':
                raise EmptyAnswerError()
            if gp_options == '1':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' and active='1'")
                dr_names = self.c.fetchall()
                # when list returned empty, there are no doctors available, patient returned to main menu
                if not dr_names:
                    print("\nI'm sorry, there are no male doctors currently available at the practice"
                          "\nplease try again another time")
                    return 0
                else:
                    # choose_dr called only with male drs in list
                    gp_details = pf.choose_dr(dr_names)
                    self.connection.close()
                    return gp_details
            elif gp_options == '2':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' and active='1'")
                dr_names = self.c.fetchall()
                # when list returned empty, there are no doctors available, patient returned to main menu
                if not dr_names:
                    print("\nI'm sorry, there are no female doctors currently available at the practice"
                          "\nplease try again another time")
                    return 0
                else:
                    # choose_dr called only with female drs in list
                    gp_details = pf.choose_dr(dr_names)
                    self.connection.close()
                    return gp_details
            elif gp_options == '3':
                self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' and active='1'")
                dr_names = self.c.fetchall()
                # when list returned empty, there are no doctors available, patient returned to main menu
                if not dr_names:
                    print("\nI'm sorry, there are no non-binary doctors currently available at the practice"
                          "\nplease try again another time")
                    return 0
                else:
                    # choose_dr called only with non-binary drs in list
                    gp_details = pf.choose_dr(dr_names)
                    self.connection.close()
                    return gp_details
            # exit to patient menu
            elif gp_options == '0':
                pass
            else:
                raise InvalidAnswerError()
        except InvalidAnswerError:
            error = InvalidAnswerError()
            print(error)
            self.choose_dr_gender(nhs_number)
        except EmptyAnswerError:
            error = EmptyAnswerError()
            print(error)
            self.choose_dr_gender(nhs_number)

    def choose_appointment(self, nhs_number, gp_details):
        """
        Function for patient to input year, month, day and time to book an appointment.

        Function calls functions from the patientFunctions module for patient to choose the year, month and day of the
        appointment. Patient is then presented with a list of all appointments on that day by time and
        displays availability. The patient can then choose the appointment time.
        This patient's appointment details are inserted into the database for chosen date and time.
        At each step, the patient can choose to go back and choose another date.
        Once booked, the patient is displayed a message that they will receive appointment confirmation shortly
        and returned back to the main patient menu.

        Parameters:
            nhs_number (int): Patient's nhs number.
            gp_details (list): list of chosen doctor email and last name.
        """
        # to choose year
        year = pf.choose_year()
        if year == 0:
            self.book_appointment(nhs_number)
        else:
            # to choose month
            month = pf.choose_month(year)
            if month == 0:
                self.choose_appointment(nhs_number, gp_details)
            else:
                # to choose day
                date = pf.choose_date(month, year)
                if date == 0:
                    self.choose_appointment(nhs_number, gp_details)
                else:
                    # start and end created for chosen date
                    start = pf.generate_start_time(date)
                    end = pf.generate_end_time(date)
                    # appointments displayed for that date
                    times_str = pf.display_available(date, start, end, gp_details)
                    # to choose time
                    chosen_time = pf.choose_time(date, times_str, gp_details)
                    if chosen_time == 0:
                        self.choose_appointment(nhs_number, gp_details)
                    else:
                        # start created for chosen date to insert into database
                        start = pf.create_start(date, chosen_time)
                        # appointment details inserted into database
                        pf.insert_appointment(start, gp_details, nhs_number)
                        print("\nYou have requested to book an appointment on {} at {}, "
                              "\nYou will receive confirmation of your appointment "
                              "shortly!"
                              "\nYou can check all of your appointments through "
                              "'view your appointments' in the main menu\n".format(date, chosen_time))
                        pass

    def cancel_appointment(self, nhs_number):
        """
        Function for patient to view all of their appointments and allows them to choose to cancel one.

        Calls the view_appointments function (from viewCancelFunctions module), if empty then patient is
        displayed a message to say they have no appointments booked and are returned to the main patient menu.
        Otherwise, they can select to cancel an appointment, calling check_app_id to confirm it exists
        and is not in the past, delete_appointment is then called to delete the chosen appointment from the database.
        If they choose to cancel another appointment, the process repeats, or they return to the main menu.
        Exceptions prevent the input from being empty or a number which is not valid in the list of choices.

        Parameters:
            nhs_number (int): Patient's nhs number.
        """
        print("--------------------------------------------"
              "\n         Patient: Cancel Appointments"
              "\n--------------------------------------------"
              "\nYour appointments: ")
        viewing = vc.view_appointments(nhs_number)
        if viewing == 0:
            print("You have no appointments booked to cancel at this time")
            # exit to patient menu
            pf.return_to_main()
        else:
            try:
                print("Choose [1] to cancel an appointment"
                      "\nChoose [0] to exit to the main menu"
                      "\n********************************************")
                options = input("Please select an option: ")
                if options == '':
                    raise EmptyAnswerError()
                elif options == '0':
                    pass
                elif options == '1':
                    # to check appointment id is valid
                    cancel = vc.check_app_id(nhs_number)
                    if cancel == 0:
                        pass
                    else:
                        # delete appointment from database
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
                            raise InvalidAnswerError()
                else:
                    raise InvalidAnswerError()
            except InvalidAnswerError:
                error = InvalidAnswerError()
                print(error)
                self.cancel_appointment(nhs_number)
            except EmptyAnswerError:
                error = EmptyAnswerError()
                print(error)
                self.cancel_appointment(nhs_number)

    def view_app_confirmations(self, nhs_number):
        """
        Function for patient to view all of their pending, accepted and declined appointments.

        Calls the view_appointments function (from viewCancelFunctions module).
        Patient is then returned to the main patient menu via the return_to_main function.

        Parameters:
            nhs_number (int): Patient's nhs number.
        """
        print("--------------------------------------------"
              "\n         Patient: View Appointments"
              "\n--------------------------------------------"
              "\nYour appointments: ")
        vc.view_appointments(nhs_number)
        pf.return_to_main()




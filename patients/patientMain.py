import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.PatientRiskProfile import PatientMedical
from patients.lifeStyleQuestionnaire import RiskProfile
from patients.appointment import Appointment
import patients.patientMedicalFunctions as pf
import usefulfunctions as uf
import re

"""
This is the main patient menu.

From this file, patients can register, login, book an appointment, view their appointments, cancel an appointment, view their medical profile, 
view their personal details, update their personal details, logout, go back to the main menu, and exit the program.
"""

connection = sql.connect('UCH.db')
c = connection.cursor()


class Error(Exception):
    """
    This is the base class for exceptions in this module.
    """
    pass


class NotRegisteredError(Error):
    """
    This is a class for when the patient is not registered by an administrator.

    Attributes:
        message (string): The message raised when the patient is not registered by an administrator.
    """

    def __init__(self, message="\n   < An administrator needs to confirm your registration before you can access our services - please try logging in tomorrow > \n"):
        """
        The constructor for NotRegisteredError class.

        Parameters:
            message (string): The message raised when the patient is not registered by an administrator.
        """

        self.message = message
        super().__init__(self.message)


class EmptyAnswerError(Error):
    """
    This is a class for when the patient presses enter with no input.

    Attributes:
        message (string): The message raised when the patient presses enter with no input.
    """

    def __init__(self, message="\n   < I'm sorry, this field cannot be left empty, please try again > \n"):
        """
        The constructor for EmptyAnswerError class.

        Parameters:
            message (string): The message raised when the patient presses enter with no input.
        """

        self.message = message
        super().__init__(self.message)


class InvalidAnswerError(Error):
    """
    This is a class for when the patient types something that does not correctly meet the requirements of the question asked.

    Attributes:
        message (string): The message raised when the patient types something that does not correctly meet the requirements of the question asked.
    """

    def __init__(self, message="\n   < I'm sorry, this is not a valid answer, please try again > \n"):
        """
        The constructor for InvalidAnswerError class.

        Parameters:
            message (string): The message raised when the patient types something that does not correctly meet the requirements of the question asked.
        """

        self.message = message
        super().__init__(self.message)


class InvalidEmailError(Error):
    """
    This is a class for when the patient does not type in a correctly-formatted email address.

    Attributes:
        message (string): The message raised when the patient does not type in a correctly-formatted email address.
    """

    def __init__(self, message="\n   < I'm sorry, that is not a valid email, please try again > \n"):
        """
        The constructor for InvalidEmailError class.

        Parameters:
            message (string): The message raised when the patient does not type in a correctly-formatted email address.
        """

        self.message = message
        super().__init__(self.message)


class EmailDoesNotExistError(Error):
    """
    This is a class for when the patient tries to login with an email that has not been registered.

    Attributes:
        message (string): The message raised when the patient tries to login with an email that has not been registered.
    """

    def __init__(self, message="\n   < I'm sorry, that email is not in our system, please try again > \n"):
        """
        The constructor for EmailDoesNotExistError class.

        Parameters:
            message (string): The message raised when the patient tries to login with an email that has not been registered.
        """

        self.message = message
        super().__init__(self.message)


class EmailAlreadyExistsError(Error):
    """
    This is a class for when the patient tries to register with an email address that is already in the database.

    Attributes:
        message (string): The message raised when the patient tries to register with an email address that is already in the database.
    """

    def __init__(self, message="\n   < I'm sorry, that email is already in use, please try again > \n"):
        """
        The constructor for EmailAlreadyExistsError class.

        Parameters:
            message (string): The message raised when the patient tries to register with an email address that is already in the database.
        """

        self.message = message
        super().__init__(self.message)


class PasswordIncorrectError(Error):
    """
    This is a class for when the patient enters an incorrect password.

    Attributes:
        message (string): The message raised when the patient enters an incorrect password.
    """

    def __init__(self, message="\n   < I'm sorry, that password is not correct, please try again > \n"):
        """
        The constructor for PasswordIncorrectError class.

        Parameters:
            message (string): The message raised when the patient enters an incorrect password.
        """

        self.message = message
        super().__init__(self.message)


class NHSDoesNotExistError(Error):
    """
    This is a class for when the patient tries to login with an NHS number that has not been registered.

    Attributes:
        message (string): The message raised when the patient tries to login with an NHS number that has not been registered.
    """

    def __init__(self, message="\n   < I'm sorry, that NHS number is not in our system, please try again > \n"):
        """
        The constructor for NHSDoesNotExistError class.

        Parameters:
            message (string): The message raised when the patient tries to login with an NHS number that has not been registered.
        """

        self.message = message
        super().__init__(self.message)


class InvalidTelephoneError(Error):
    """
    This is a class for when the patient enters a telephone number that is not in the correct format.

    Attributes:
        message (string): The message raised when the patient enters a telephone number that is not in the correct format.
    """

    def __init__(self, message="\n   < I'm sorry, that is not a valid telephone number, please try again > \n"):
        """
        The constructor for InvalidTelephoneError class.

        Parameters:
            message (string): The message raised when the patient enters a telephone number that is not in the correct format.
        """

        self.message = message
        super().__init__(self.message)


class DateInvalidError(Error):
    """
    This is a class for when the patient enters a date that does not exist.

    Attributes:
        message (string): The message raised when the patient enters a date that does not exist i.e. 2020-02-30.
    """

    def __init__(self, message="\n   < I'm sorry, that is not a valid date, please try again > \n"):
        """
        The constructor for DateInvalidError class.

        Parameters:
            message (string): The message raised when the patient enters a date that does not exist i.e. 2020-02-30.
        """

        self.message = message
        super().__init__(self.message)


class DateInFutureError(Error):
    """
    This is a class for when the patient enters a date that has not happened yet.

    Attributes:
        message (string): The message raised when the patient enters a date that has not happened yet.
    """

    def __init__(self, message="\n   < I'm sorry, your date of birth cannot be in the future, please try again > \n"):
        """
        The constructor for DateInFutureError class.

        Parameters:
            message (string): The message raised when the patient enters a date that has not happened yet.
        """

        self.message = message
        super().__init__(self.message)


class DateFormatError(Error):
    """
    This is a class for when the patient enters a date in a different format to what is requested.

    Attributes:
        message (string): The message raised when the patient enters a date in a different format to what is requested.
    """

    def __init__(self, message="\n   < I'm sorry, this date is not in the proper YYYY-MM-DD format, with '-'s as separators, please try again > \n"):
        """
        The constructor for DateFormatError class.

        Parameters:
            message (string): The message raised when the patient enters a date in a different format to what is requested.
        """

        self.message = message
        super().__init__(self.message)


def summary(NHS_number):
    """ 
    Function to show all of the patient's details in the database attached to their NHS number. 

    Patients can view their NHS number, their name, their email, their date of birth, their gender, their address, 
    their telephone number, and their password (hashed for security).

    Parameters:
    NHS_number (string): the patient's NHS number. 
    """
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
    results = c.fetchall()
    hash = ""
    for i in results[0][10]:
        hash += "*"
    print("--------------------------------------------")
    print("Patient Summary of " +
          str(results[0][2]) + " " + str(results[0][3]))
    print("--------------------------------------------")
    print("Your NHS number is: ")
    x = str(results[0][0])
    one = x[0:3]
    two = x[3:6]
    three = x[6:10]
    # Seoarating the NHS number so that the format looks more realistic
    print(one, two, three)
    print("First Name: " + str(results[0][2]))
    print("Last Name: " + str(results[0][3]))
    print("Email: " + str(results[0][1]))
    print("Date of Birth: " + str(results[0][4]))
    print("Gender: " + str(results[0][5]))
    print("Address: ")
    # Printing each line of the address
    print(str(results[0][6]))
    print(str(results[0][7]))
    print(str(results[0][8]))
    print("Telephone Number: +" + str(results[0][9]))
    print("Password: " + hash)


def options(NHS_number):
    """ 
    Function which offers several options for the patient who has successfully logged in and is confirmed by an administrator. 

    Patients can book an appointment, view their appointments, cancel an appointment, see their medical profile, 
    see their personal details, update their personal details, or log out.

    Parameters:
    NHS_number (string): the patient's NHS number. 
    """
    count = 0
    while True:
        while count < 13:
            try:
                # update_patient declared here because it is used by multiple while loops in this function
                update_patient = {"address_line_1": "",
                                  "address_line_2": "",
                                  "postcode": ""}
                while count == 0:
                    uf.banner('Patient')
                    print("What would you like to do next?")
                    print("Choose [1] to book an appointment")
                    print("Choose [2] to view your appointments")
                    print("Choose [3] to cancel an appointment")
                    print("Choose [4] to see your medical profile")
                    print("Choose [5] to see your personal details")
                    print("Choose [6] to update your personal details")
                    print("Choose [0] to log out")
                    action = input("Please select an option: ")
                    if action == '':
                        raise EmptyAnswerError()
                    elif action == '1':
                        # Uses the appointment.py file to book an appointment
                        x = Appointment()
                        x.book_appointment(NHS_number)
                    elif action == '2':
                        # Uses the appointment.py file to view appointments
                        x = Appointment()
                        x.view_app_confirmations(NHS_number)
                    elif action == '3':
                        # Uses the appointment.py file to cancel an appointment
                        x = Appointment()
                        x.cancel_appointment(NHS_number)
                    elif action == '4':
                        # Redirects to a new menu
                        count = 1
                    elif action == '5':
                        # To see the patient summary
                        summary(NHS_number)
                    elif action == '6':
                        # To see the patient summary then redirects to a new menu
                        summary(NHS_number)
                        count = 3
                    elif action == '0':
                        # Redirects to task() (the main menu for patients)
                        return 0
                    else:
                        raise InvalidAnswerError()
                while count == 1:
                    print("********************************************")
                    print("Choose [1] to see your medical profile")
                    print(
                        "Choose [2] to take the lifestyle risk questionnaire")
                    print("Choose [3] to update your medical history")
                    print("Choose [0] to go back")
                    print("********************************************")
                    action = input("Please select an option: ")
                    if action == '':
                        raise EmptyAnswerError()
                    elif action == '1':
                        # Uses PatientRiskProfile.py to view medical profile
                        name = PatientMedical(NHS_number)
                        name.show_profile(NHS_number)
                    elif action == '2':
                        print(
                            "Please fill out the following lifestyle questions to assess any potential health risk")
                        # Uses lifestyleQuestionnaire.py to take the lifestyle risk questionnaire
                        x = RiskProfile(NHS_number)
                        x.questions(NHS_number)
                        x.BMI_calculator(NHS_number)
                        x.smoking(NHS_number)
                        x.drugs(NHS_number)
                        x.alcohol(NHS_number)
                        x.diet(NHS_number)
                        x.insert_to_table(NHS_number)
                    elif action == '3':
                        # Redirects to a new menu
                        count = 2
                    elif action == '0':
                        # Returns to main options menu
                        count = 0
                    else:
                        raise InvalidAnswerError()
                while count == 2:
                    x = PatientMedical(NHS_number)
                    print("********************************************")
                    print(
                        "Choose [1] to provide vaccination history for you or your children (if any)")
                    print(
                        "Choose [2] to provide cancer related medical history for you or your family (if any)")
                    print(
                        "Choose [3] to provide pre-existing conditions for you or your children (if any)")
                    print(
                        "Choose [4] to provide medicine allergies for you or your children (if any)")
                    print("Choose [0] to go back")
                    print("********************************************")
                    action = input('Please select an option: ')
                    if action == '':
                        raise EmptyAnswerError()
                    elif action == '1':
                        # Uses PatientRiskProfile.py to provide vaccination history
                        x.vaccination(NHS_number)
                    elif action == '2':
                        # Uses PatientRiskProfile.py to provide cancer related medical history
                        x.cancer(NHS_number)
                    elif action == '3':
                        # Uses PatientRiskProfile.py to provide pre-existing conditions
                        x.pre_existing_con(NHS_number)
                    elif action == '4':
                        # Uses PatientRiskProfile.py to provide medicine allergies
                        x.med_allergy(NHS_number)
                    elif action == '0':
                        # Returns to medical profile menu
                        count = 1
                    else:
                        raise InvalidAnswerError()
                while count == 3:
                    print("********************************************")
                    print("Which details would you like to update?")
                    print("Choose [1] for first name")
                    print("Choose [2] for last name")
                    print("Choose [3] for address")
                    print("Choose [4] for telephone number")
                    print("Choose [5] for email address")
                    print("Choose [6] for password")
                    print("Choose [0] to go back")
                    print("********************************************")
                    action = input("Please select an option: ")
                    if action == '':
                        raise EmptyAnswerError()
                    elif action == '1':
                        # Redirects to the update first name while loop
                        count = 4
                    elif action == '2':
                        # Redirects to the update last name while loop
                        count = 5
                    elif action == '3':
                        # Redirects to the update address line 1 while loop and reassigns blank values
                        update_patient = {"address_line_1": "",
                                          "address_line_2": "",
                                          "postcode": ""}
                        count = 9
                    elif action == '4':
                        # Redirects to the update telephone number while loop
                        count = 6
                    elif action == '5':
                        # Redirects to the update email address while loop
                        count = 7
                    elif action == '6':
                        # Redirects to the update password while loop
                        count = 8
                    elif action == '0':
                        # Returns to main options menu
                        count = 0
                    else:
                        raise InvalidAnswerError()
                while count == 4:
                    first_name = input(
                        "Please enter your new first name (press 0 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    first_name = first_name.strip().title() 
                    if first_name == '':
                        raise EmptyAnswerError()
                    elif first_name == '0':
                        # Returns to the update details menu
                        count = 3
                    else:
                        # Removes all spaces from input
                        x = first_name.replace(" ", "")
                        # Checks if there are any numbers in the input
                        if (any(str.isdigit(y) for y in x)) == True:
                            raise InvalidAnswerError()
                        else:
                            # Updates first name in the database
                            c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""",
                                      (first_name, NHS_number))
                            connection.commit()
                            print("Successfully changed first name")
                            # Shows the patient summary
                            summary(NHS_number)
                            # Returns to the update details menu
                            count = 3
                while count == 5:
                    last_name = input(
                        "Please enter your new last name (press 0 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    last_name = last_name.strip().title() 
                    if last_name == '':
                        raise EmptyAnswerError()
                    elif last_name == '0':
                        # Returns to the update details menu
                        count = 3
                    else:
                        # Removes all spaces from input
                        x = last_name.replace(" ", "")
                        # Checks if there are any numbers in the input
                        if (any(str.isdigit(y) for y in x)) == True:
                            raise InvalidAnswerError()
                        else:
                            # Updates last name in the database
                            c.execute(
                                """UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""", (last_name, NHS_number))
                            connection.commit()
                            print("Successfully changed last name")
                            # Shows the patient summary
                            summary(NHS_number)
                            # Returns to the update details menu
                            count = 3
                while count == 6:
                    telephone_number = input(
                        "Please enter your new telephone number, including country code (i.e. +447123456789)(press 0 to go back): ")
                    if telephone_number == '':
                        raise EmptyAnswerError()
                    elif telephone_number == '0':
                        # Returns to the update details menu
                        count = 3
                    else:
                        # Removes any character from input that is not a number
                        telephone_number = re.sub(
                            "[^0-9]", "", telephone_number)
                        # Checks if input is the right length for any telephone number
                        if len(telephone_number) > 17 or len(telephone_number) < 11:
                            raise InvalidTelephoneError()
                        else:
                            # Converts telephone number string into an integer
                            telephone_number = int(telephone_number)
                            # Updates telephone number in the database
                            c.execute("""UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""",
                                      (telephone_number, NHS_number))
                            connection.commit()
                            print("Successfully changed telephone number")
                            # Shows the patient summary
                            summary(NHS_number)
                            # Returns to the update details menu
                            count = 3
                while count == 7:
                    patient_email = input(
                        "Please enter your new email (press 0 to go back): ")
                    if patient_email == '':
                        raise EmptyAnswerError()
                    elif patient_email == '0':
                        # Returns to the update details menu
                        count = 3
                    # Checks that input is a valid email address
                    elif re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
                        # Checks if email already exists in the database
                        c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",
                                  [patient_email])
                        patient_emails = c.fetchall()
                        if patient_emails != []:
                            raise EmailAlreadyExistsError()
                        else:
                            # Updates email in the database
                            c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""",
                                      (patient_email, NHS_number))
                            connection.commit()
                            print("Successfully changed email address")
                            # Shows the patient summary
                            summary(NHS_number)
                            # Returns to the update details menu
                            count = 3
                    else:
                        raise InvalidEmailError()
                while count == 8:
                    # Fetches patient record from database that matches their NHS number to check password
                    c.execute(
                        "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
                    NHS_numbers = c.fetchall()
                    password = input(
                        "In order to change your password, please enter your old password (press 0 to go back): ")
                    if password == '':
                        raise EmptyAnswerError()
                    elif password == '0':
                        # Returns to the update details menu
                        count = 3
                    else:
                        # Checks if the password input matches the password in the database
                        if password != NHS_numbers[0][10]:
                            raise PasswordIncorrectError()
                        else:
                            password = input(
                                "Please enter your new password (press 0 to go back to update details menu): ")
                            if password == '':
                                raise EmptyAnswerError()
                            elif password == '0':
                                # Returns to the update details menu
                                count = 3
                            else:
                                # Updates password in the database
                                c.execute(
                                    """UPDATE PatientDetail SET password = ? WHERE nhsNumber = ?""", (password, NHS_number))
                                connection.commit()
                                print("Successfully changed password")
                                # Shows the patient summary
                                summary(NHS_number)
                                # Returns to the update details menu
                                count = 3
                while count == 9:
                    address_line_1 = input(
                        "Please enter your new address line 1 (press 0 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    address_line_1 = address_line_1.strip().title() 
                    if address_line_1 == '':
                        raise EmptyAnswerError()
                    elif address_line_1 == '0':
                        # Returns to the update details menu
                        count = 3
                    # Ensures the input length is not too long
                    elif len(address_line_1) > 400:
                        raise InvalidAnswerError()
                    else:
                        # Assigns input value to update_patient dictionary
                        update_patient["address_line_1"] = address_line_1
                        # Redirects to the update address line 2 while loop
                        count = 10
                while count == 10:
                    address_line_2 = input(
                        "Please enter your new address line 2 (press 0 to go back to update details menu, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    address_line_2 = address_line_2.strip().title()
                    if address_line_2 == '0':
                        # Returns to the update details menu
                        count = 3
                    elif address_line_2 == "1":
                        #  Returns to the update address line 1 while loop
                        count = 9
                    # Ensures the input length is not too long
                    elif len(address_line_2) > 400:
                        raise InvalidAnswerError()
                    else:
                        # Assigns input value to update_patient dictionary
                        update_patient["address_line_2"] = address_line_2
                        # Redirects to the update city while loop
                        count = 11
                while count == 11:
                    city = input(
                        "Please enter your new city (press 0 to go back to update details menu, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    city = city.strip().title() 
                    if city == '':
                        raise EmptyAnswerError()
                    elif city == '0':
                        # Returns to the update details menu
                        count = 3
                    elif city == "1":
                        #  Returns to the update address line 2 while loop
                        count = 10
                    # Ensures the input length is not too long
                    elif len(city) > 200:
                        raise InvalidAnswerError()
                    else:
                        # Removes all spaces from input
                        x = city.replace(" ", "")
                        # Checks if there are any numbers in the input
                        if (any(str.isdigit(y) for y in x)) == True:
                            raise InvalidAnswerError()
                        else:
                            address_line_2 = (
                                update_patient["address_line_2"] + " " + city).strip()
                            # Assigns input value to update_patient dictionary
                            update_patient["address_line_2"] = address_line_2
                            # Redirects to the update postcode while loop
                            count = 12
                while count == 12:
                    postcode = input(
                        "Please enter your new postcode (press 0 to go back to update details menu, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises each letter
                    postcode = postcode.strip().upper()
                    if postcode == '':
                        raise EmptyAnswerError()
                    elif postcode == '0':
                        # Returns to the update details menu
                        count = 3
                    elif postcode == "1":
                        #  Returns to the update city while loop
                        count = 11
                    # Ensures the input length is not too long
                    elif len(postcode) > 50:
                        raise InvalidAnswerError()
                    else:
                        # Assigns input value to update_patient dictionary
                        update_patient["postcode"] = postcode
                        # Updates address line 1 in the database
                        c.execute("""UPDATE PatientDetail SET addressLine1 = ? WHERE nhsNumber = ?""",
                                  (update_patient["address_line_1"], NHS_number))
                        connection.commit()
                        # Updates address line 2 in the database
                        c.execute("""UPDATE PatientDetail SET addressLine2 = ? WHERE nhsNumber = ?""",
                                  (update_patient["address_line_2"], NHS_number))
                        connection.commit()
                        # Updates the postcode in the database
                        c.execute("""UPDATE PatientDetail SET postcode = ? WHERE nhsNumber = ?""",
                                  (update_patient["postcode"], NHS_number))
                        connection.commit()
                        print("Successfully changed address")
                        # Shows the patient summary
                        summary(NHS_number)
                        # Returns to the update details menu
                        count = 3
            except InvalidAnswerError:
                error = InvalidAnswerError()
                print(error)
            except EmptyAnswerError:
                error = EmptyAnswerError()
                print(error)
            except InvalidTelephoneError:
                error = InvalidTelephoneError()
                print(error)
            except InvalidEmailError:
                error = InvalidEmailError()
                print(error)
            except EmailAlreadyExistsError:
                error = EmailAlreadyExistsError()
                print(error)
            except PasswordIncorrectError:
                error = PasswordIncorrectError()
                print(error)


def login():
    """ 
    Function to allow patients to log into their account. 

    Patients can log in using their email or their NHS number. Once they have successfully logged in, 
    they are sent to the patient option menu.

    Returns:
    string: the patient's NHS number. 
    """
    count = 0
    NHS_number = ""
    while True:
        while count < 6:
            try:
                while count == 0:
                    print("********************************************")
                    print("Choose [1] to login using your email")
                    print("Choose [2] to login using your NHS number")
                    print("Choose [0] to go back")
                    print("********************************************")
                    action = input("Please select an option: ")
                    if action == '':
                        raise EmptyAnswerError()
                    elif action == '1':
                        # Redirects to patient login with email while loop
                        count = 1
                    elif action == '2':
                        # Redirects to patient login with NHS number while loop
                        count = 3
                    elif action == '0':
                        # Redirects to task() (the main menu for patients)
                        return 0
                    else:
                        raise InvalidAnswerError()
                while count == 1:
                    patient_email = input("Email (press 0 to go back): ")
                    if patient_email == '0':
                        count = 0
                    # Checks that input is a valid email address
                    elif re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
                        # Checks if email already exists in the database
                        c.execute(
                            "SELECT * FROM PatientDetail WHERE patientEmail = ?", [patient_email])
                        patient_emails = c.fetchall()
                        if patient_emails == []:
                            raise EmailDoesNotExistError
                        else:
                            # Redirects to password while loop
                            count = 2
                    else:
                        raise InvalidEmailError()
                while count == 2:
                    c.execute(
                        "SELECT * FROM PatientDetail WHERE patientEmail = ?", [patient_email])
                    patient_emails = c.fetchall()
                    password = input("Password (press 0 to go back): ")
                    if password == '0':
                        count = 1
                    elif password != patient_emails[0][10]:
                        raise PasswordIncorrectError()
                    else:
                        NHS_number = patient_emails[0][0]
                        count = 5
                while count == 3:
                    NHS_number = input("NHS Number (press 0 to go back): ")
                    if NHS_number == '0':
                        count = 0
                    else:
                        NHS_number = int(re.sub("[^0-9]", "", NHS_number))
                        c.execute(
                            "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
                        NHS_numbers = c.fetchall()
                        if NHS_numbers == []:
                            raise NHSDoesNotExistError()
                        else:
                            # Redirects to patient login with NHS number while loop
                            count = 4
                while count == 4:
                    # Fetches patient record from database that matches their NHS number to check password
                    c.execute(
                        "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
                    NHS_numbers = c.fetchall()
                    password = input("Password (press 0 to go back): ")
                    if password == '0':
                        count = 3
                    # Checks if the password input matches the password in the database
                
                        raise PasswordIncorrectError()
                    else:
                        NHS_number = NHS_numbers[0][0]
                        count = 5
                while count == 5:
                    c.execute(
                        "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
                    results = c.fetchall()
                    if results[0][11] == 0:
                        raise NotRegisteredError()
                        return 0
                    else:
                        count = 6
            except InvalidAnswerError:
                error = InvalidAnswerError()
                print(error)
            except EmptyAnswerError:
                error = EmptyAnswerError()
                print(error)
            except InvalidEmailError:
                error = InvalidEmailError()
                print(error)
            except EmailDoesNotExistError:
                error = EmailDoesNotExistError()
                print(error)
            except PasswordIncorrectError:
                error = PasswordIncorrectError()
                print(error)
            except NHSDoesNotExistError:
                error = NHSDoesNotExistError()
                print(error)
            except NotRegisteredError:
                error = NotRegisteredError()
                print(error)
        options(NHS_number)
        return 0


def register():
    """ 
    Function to register new patients. 

    Allows new patients to provide their first name, last name, date of birth, gender, address, telephone number, email, 
    and password. Once they submit their details, they are sent back to the main menu for patients. 
    """
    new_patient = {"first_name": "",
                   "last_name": "",
                   "date_of_birth": "",
                   "gender": "",
                   "address_line_1": "",
                   "address_line_2": "",
                   "postcode": "",
                   "telephone_number": 0,
                   "patient_email": "",
                   "password": ""}
    count = 0
    while True:
        while count < 11:
            try:
                while count == 0:
                    first_name = input(
                        "Please enter your first name (press 0 to exit registration): ")
                    first_name = first_name.strip().title() 
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    if first_name == '':
                        raise EmptyAnswerError()
                    elif first_name == '0':
                        return 0
                    x = first_name.replace(" ", "")
                    # Removes all spaces from input
                    # Checks if there are any numbers in the input
                    if (any(str.isdigit(y) for y in x)) == True:
                        raise InvalidAnswerError()
                    else:
                        new_patient["first_name"] = first_name
                        count = 1
                while count == 1:
                    last_name = input(
                        "Please enter your last name (press 0 to exit registration, press 1 to go back): ")
                    last_name = last_name.strip().title() 
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    if last_name == '':
                        raise EmptyAnswerError()
                    elif last_name == '0':
                        return 0
                    elif last_name == '1':
                        count = 0
                    else:
                        x = last_name.replace(" ", "")
                        # Removes all spaces from input
                        # Checks if there are any numbers in the input
                        if (any(str.isdigit(y) for y in x)) == True:
                            raise InvalidAnswerError()
                        else:
                            new_patient["last_name"] = last_name
                            count = 2
                while count == 2:
                    date_of_birth = input(
                        'Please enter your birthday in YYYY-MM-DD format (press 0 to exit registration, press 1 to go back): ')
                    if date_of_birth == '':
                        raise EmptyAnswerError()
                    elif date_of_birth == '0':
                        return 0
                    elif date_of_birth == '1':
                        count = 1
                    else:
                        x = date_of_birth.replace(" ", "")
                        # Removes all spaces from input
                        x = x.replace("-", "")
                        if (len(date_of_birth) != 10) or (date_of_birth[4] != '-' or date_of_birth[7] != '-') or (x.isdigit() == False):
                            raise DateFormatError()
                        else:
                            day = date_of_birth[8:10]
                            month = date_of_birth[5:7]
                            year = date_of_birth[0:4]
                            if (day.isdigit() == False) or (month.isdigit() == False) or (year.isdigit() == False):
                                raise DateInvalidError()
                            else:
                                day = int(date_of_birth[8:10])
                                month = int(date_of_birth[5:7])
                                year = int(date_of_birth[0:4])
                                if month > 12 or month < 1:
                                    raise DateInvalidError()
                                elif (month == 9 or month == 4 or month == 6 or month == 11) and day > 30:
                                    raise DateInvalidError()
                                elif month == 2 and year % 4 != 0 and day > 28:
                                    raise DateInvalidError()
                                elif month == 2 and year % 4 == 0 and day > 29:
                                    raise DateInvalidError()
                                elif day > 31 or day < 1:
                                    raise DateInvalidError()
                                else:
                                    date_of_birth = datetime.date(
                                        year, month, day)
                                    today = date.today()
                                    if date_of_birth > today:
                                        raise DateInFutureError()
                                    else:
                                        new_patient["date_of_birth"] = date_of_birth
                                        count = 3
                while count == 3:
                    print("********************************************")
                    print("Choose [1] for female")
                    print("Choose [2] for male")
                    print("Choose [3] for non-binary")
                    print("Choose [4] to exit registration")
                    print("Choose [5] to go back")
                    print("********************************************")
                    choice = input("Please select an option: ")
                    if choice == '':
                        raise EmptyAnswerError()
                    elif choice == '1':
                        gender = "Female"
                        new_patient["gender"] = gender
                        count = 4
                    elif choice == "2":
                        gender = "Male"
                        new_patient["gender"] = gender
                        count = 4
                    elif choice == "3":
                        gender = "Non-Binary"
                        new_patient["gender"] = gender
                        count = 4
                    elif choice == "4":
                        return 0
                    elif choice == "5":
                        count = 2
                    else:
                        raise InvalidAnswerError()
                while count == 4:
                    address_line_1 = input(
                        "Address Line 1 (press 0 to exit registration, press 1 to go back): ")
                    address_line_1 = address_line_1.strip().title() 
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    if address_line_1 == '':
                        raise EmptyAnswerError()
                    elif address_line_1 == '0':
                        return 0
                    elif address_line_1 == "1":
                        count = 3
                    elif len(address_line_1) > 400:
                        # Ensures the input length is not too long
                        raise InvalidAnswerError()
                    else:
                        new_patient["address_line_1"] = address_line_1
                        count = 5
                while count == 5:
                    address_line_2 = input(
                        "Address Line 2 (press 0 to exit registration, press 1 to go back): ")
                    address_line_2 = address_line_2.strip().title() 
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    if address_line_2 == '0':
                        return 0
                    elif address_line_2 == "1":
                        count = 4
                    elif len(address_line_2) > 400:
                        # Ensures the input length is not too long
                        raise InvalidAnswerError()
                    else:
                        new_patient["address_line_2"] = address_line_2
                        count = 6
                while count == 6:
                    city = input(
                        "City (press 0 to exit registration, press 1 to go back): ")
                    city = city.strip().title() 
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    if city == '':
                        raise EmptyAnswerError()
                    elif city == '0':
                        return 0
                    elif city == "1":
                        count = 5
                    elif len(city) > 200:
                        # Ensures the input length is not too long
                        raise InvalidAnswerError()
                    else:
                        x = city.replace(" ", "")
                        # Removes all spaces from input
                        # Checks if there are any numbers in the input
                        if (any(str.isdigit(y) for y in x)) == True:
                            raise InvalidAnswerError()
                        else:
                            address_line_2 = (
                                new_patient["address_line_2"] + " " + city).strip()
                            new_patient["address_line_2"] = address_line_2
                            count = 7
                while count == 7:
                    postcode = input(
                        "Postcode (press 0 to exit registration, press 1 to go back): ")
                    postcode = postcode.strip().upper()
                    if postcode == '':
                        raise EmptyAnswerError()
                    elif postcode == '0':
                        return 0
                    elif postcode == "1":
                        count = 6
                    elif len(postcode) > 50:
                        # Ensures the input length is not too long
                        raise InvalidAnswerError()
                    else:
                        new_patient["postcode"] = postcode
                        count = 8
                while count == 8:
                    telephone_number = input(
                        "Telephone number, including country code (i.e. +447123456789)(press 0 to exit registration, press 1 to go back): ")
                    if telephone_number == '':
                        raise EmptyAnswerError()
                    elif telephone_number == '0':
                        return 0
                    elif telephone_number == "1":
                        count = 7
                    else:
                        # Removes any character from input that is not a number
                        telephone_number = re.sub(
                            "[^0-9]", "", telephone_number)
                        # Checks if input is the right length for any telephone number
                        if len(telephone_number) > 17 or len(telephone_number) < 11:
                            raise InvalidTelephoneError()
                        else:
                            # Converts telephone number string into an integer
                            telephone_number = int(telephone_number)
                            new_patient["telephone_number"] = telephone_number
                            count = 9
                while count == 9:
                    patient_email = input(
                        "Email (press 0 to exit registration, press 1 to go back): ")
                    if patient_email == '':
                        raise EmptyAnswerError()
                    elif patient_email == '0':
                        return 0
                    elif patient_email == "1":
                        count = 8
                    # Checks that input is a valid email address
                    elif re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
                        # Checks if email already exists in the database
                        c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",
                                  [patient_email])
                        patient_emails = c.fetchall()
                        if patient_emails != []:
                            raise EmailAlreadyExistsError()
                        else:
                            new_patient["patient_email"] = patient_email
                            count = 10
                    else:
                        raise InvalidEmailError()
                while count == 10:
                    password = input(
                        "Password (press 0 to exit registration, press 1 to go back): ")
                    if password == '':
                        raise EmptyAnswerError()
                    elif password == '0':
                        return 0
                    elif password == "1":
                        count = 9
                    else:
                        new_patient["password"] = password
                        count = 11
            except EmptyAnswerError:
                error = EmptyAnswerError()
                print(error)
            except InvalidAnswerError:
                error = InvalidAnswerError()
                print(error)
            except DateFormatError:
                error = DateFormatError()
                print(error)
            except DateInvalidError:
                error = DateInvalidError()
                print(error)
            except DateInFutureError:
                error = DateInFutureError()
                print(error)
            except InvalidTelephoneError:
                error = InvalidTelephoneError()
                print(error)
            except InvalidEmailError:
                error = InvalidEmailError()
                print(error)
            except EmailAlreadyExistsError:
                error = EmailAlreadyExistsError()
                print(error)
        x = Patient(new_patient["patient_email"], new_patient["first_name"], new_patient["last_name"], new_patient["date_of_birth"], new_patient["gender"],
                    new_patient["address_line_1"], new_patient["address_line_2"], new_patient["postcode"], new_patient["telephone_number"], new_patient["password"])
        x.register()
        print("Thank you, " + x.first_name +
              ", for submitting your details to our practice. An administrator will confirm your registration within 1-3 working days.")
        summary(x.NHS_number)
        return 0


def task():
    """ 
    Main menu for patients. 

    Allows patients to either register, login, return to the main menu, or exit the program. 
    """
    try:
        print("********************************************")
        print("Choose [1] to register for a new account")
        print("Choose [2] to login")
        print("Choose [3] to go back to the main menu")
        print("Choose [0] to exit")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise EmptyAnswerError()
        elif action == '1':
            register()
        elif action == '2':
            login()
        elif action == '3':
            return 0
        elif action == '0':
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        task()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        task()

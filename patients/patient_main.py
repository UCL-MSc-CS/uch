import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.patient_risk_profile import PatientMedical
from patients.lifestyle_questionnaire import RiskProfile
from patients.appointment import Appointment
# import patients.patient_medical_functions as pf
import useful_functions as uf
import re
import logging

"""
This is the main patient menu.

From this file, patients can register, login, book an appointment, view their appointments, cancel an appointment, view their medical profile, 
view their personal details, update their personal details, logout, go back to the main menu, and exit the program.
"""

connection = sql.connect("UCH.db")
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

    def __init__(self,message="\n   < An administrator needs to confirm your registration before you can access our services - please try logging in tomorrow > \n"):
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

    def __init__(self,message="\n   < I'm sorry, this field cannot be left empty, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, this is not a valid answer, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that is not a valid email, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that email is not in our system, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that email is already in use, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that password is not correct, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that NHS number is not in our system, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that is not a valid telephone number, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, that is not a valid date, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, your date of birth cannot be in the future, please try again > \n"):
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

    def __init__(self,message="\n   < I'm sorry, this date is not in the proper YYYY-MM-DD format, with '-'s as separators, please try again > \n"):
        """
        The constructor for DateFormatError class.

        Parameters:
            message (string): The message raised when the patient enters a date in a different format to what is requested.
        """

        self.message = message
        super().__init__(self.message)

def summary(nhs_number):
    """ 
    Function to show all of the patient's details in the database attached to their NHS number. 

    Patients can view their NHS number, their name, their email, their date of birth, their gender, their address, 
    their telephone number, and their password (hashed for security).

    Parameters:
    nhs_number (string): the patient's NHS number. 
    """
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?",[nhs_number])
    results = c.fetchall()
    hash = ""
    for i in results[0][10]:
        hash += "*"
    print("--------------------------------------------")
    print("Patient Summary of %s %s"%(results[0][2],results[0][3]))
    print("--------------------------------------------")
    print("Your NHS number is: ")
    # Separating the NHS number so that the format looks more realistic
    print("%s %s %s"%(str(results[0][0])[0:3],str(results[0][0])[3:6],str(results[0][0])[6:10]))
    print("First Name: %s"%(results[0][2]))
    print("Last Name: %s"%(results[0][3]))
    print("Email: %s"%(results[0][1]))
    print("Date of Birth: %s"%(results[0][4]))
    print("Gender: %s"%(results[0][5]))
    print("Address:\n%s\n%s\n%s"%(results[0][6],results[0][7],results[0][8]))
    print("Telephone Number: +%s"%(results[0][9]))
    print("Password: %s"%(hash))

def options(nhs_number):
    """ 
    Function which offers several options for the patient who has successfully logged in and is confirmed by an administrator. 

    Patients can book an appointment, view their appointments, cancel an appointment, see their medical profile, 
    see their personal details, update their personal details, or log out.

    Parameters:
    nhs_number (string): the patient's NHS number. 
    """
    count = 0
    while True:
        while count < 12:
            try:
                while count == 0:
                    uf.banner("Patient")
                    print("What would you like to do next?")
                    print("Choose [1] to book an appointment")
                    print("Choose [2] to view your appointments")
                    print("Choose [3] to cancel an appointment")
                    print("Choose [4] to see your medical profile")
                    print("Choose [5] to see your personal details")
                    print("Choose [6] to update your personal details")
                    print("Choose [0] to log out")
                    action = input("Please select an option: ")
                    if action == "":raise EmptyAnswerError()
                    elif action == "1":
                        # Uses the appointment.py file to book an appointment
                        x = Appointment()
                        x.book_appointment(nhs_number)
                    elif action == "2":
                        # Uses the appointment.py file to view appointments
                        x = Appointment()
                        x.view_app_confirmations(nhs_number)
                    elif action == "3":
                        # Uses the appointment.py file to cancel an appointment
                        x = Appointment()
                        x.cancel_appointment(nhs_number)
                    # Redirects to a new menu
                    elif action == "4":count = 1
                    # To see the patient summary
                    elif action == "5":summary(nhs_number)
                    elif action == "6":
                        # To see the patient summary then redirects to a new menu
                        summary(nhs_number)
                        count = 3
                    # Redirects to task() (the main menu for patients)
                    elif action == "0":return 0
                    else:raise InvalidAnswerError()
                while count == 1:
                    print("********************************************")
                    print("Choose [1] to see your medical profile")
                    print("Choose [2] to take the lifestyle risk questionnaire")
                    print("Choose [3] to update your medical history")
                    print("Choose [0] to go back")
                    print("********************************************")
                    action = input("Please select an option: ")
                    if action == "":raise EmptyAnswerError()
                    elif action == "1":
                        # Uses PatientRiskProfile.py to view medical profile
                        name = PatientMedical(nhs_number)
                        name.show_profile(nhs_number)
                    elif action == "2":
                        print("Please fill out the following lifestyle questions to assess any potential health risk")
                        # Uses lifestyleQuestionnaire.py to take the lifestyle risk questionnaire
                        x = RiskProfile(nhs_number)
                        x.questions(nhs_number)
                        x.bmi_calculator(nhs_number)
                        x.smoking(nhs_number)
                        x.drugs(nhs_number)
                        x.alcohol(nhs_number)
                        x.diet(nhs_number)
                        x.insert_to_table(nhs_number)
                    # Redirects to a new menu
                    elif action == "3":count = 2
                    # Returns to main options menu
                    elif action == "0":count = 0
                    else:raise InvalidAnswerError()
                while count == 2:
                    x = PatientMedical(nhs_number)
                    print("********************************************")
                    print("Choose [1] to provide vaccination history for you or your children (if any)")
                    print("Choose [2] to provide cancer related medical history for you or your family (if any)")
                    print("Choose [3] to provide pre-existing conditions for you or your children (if any)")
                    print("Choose [4] to provide medicine allergies for you or your children (if any)")
                    print("Choose [0] to go back")
                    print("********************************************")
                    action = input("Please select an option: ")
                    if action == "":raise EmptyAnswerError()
                    # Uses PatientRiskProfile.py to provide vaccination history
                    elif action == "1":x.vaccination(nhs_number)
                    # Uses PatientRiskProfile.py to provide cancer related medical history
                    elif action == "2":x.cancer(nhs_number)
                    # Uses PatientRiskProfile.py to provide pre-existing conditions
                    elif action == "3":x.pre_existing_con(nhs_number)
                    # Uses PatientRiskProfile.py to provide medicine allergies
                    elif action == "4":x.med_allergy(nhs_number)
                    # Returns to medical profile menu
                    elif action == "0":count = 1
                    else:raise InvalidAnswerError()
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
                    if action == "":raise EmptyAnswerError()
                    # Redirects to the update first name while loop
                    elif action == "1":count = 4
                    # Redirects to the update last name while loop
                    elif action == "2":count = 5
                    # Redirects to the update address line 1 while loop
                    elif action == "3":count = 9
                    # Redirects to the update telephone number while loop
                    elif action == "4":count = 6
                    # Redirects to the update email address while loop
                    elif action == "5":count = 7
                    # Redirects to the update password while loop
                    elif action == "6":count = 8
                    # Returns to main options menu
                    elif action == "0":count = 0
                    else:raise InvalidAnswerError()
                while count == 4:
                    first_name = input("Please enter your new first name (press 0 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    first_name = first_name.strip().title()
                    # Removes all spaces from input
                    x = first_name.replace(" ","")
                    if first_name == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif first_name == "0":count = 3
                    # Checks if there are any numbers in the input
                    elif (any(str.isdigit(y) for y in x)) == True:raise InvalidAnswerError()
                    else:
                        # Updates first name in the database
                        c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""",(first_name,nhs_number))
                        connection.commit()
                        print("Successfully changed first name")
                        # Shows the patient summary
                        summary(nhs_number)
                        # Returns to the update details menu
                        count = 3
                while count == 5:
                    last_name = input("Please enter your new last name (press 0 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    last_name = last_name.strip().title()
                    # Removes all spaces from input
                    x = last_name.replace(" ","")
                    if last_name == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif last_name == "0":count = 3
                    # Checks if there are any numbers in the input
                    elif (any(str.isdigit(y) for y in x)) == True:raise InvalidAnswerError()
                    else:
                        # Updates last name in the database
                        c.execute("""UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""",(last_name,nhs_number))
                        connection.commit()
                        print("Successfully changed last name")
                        # Shows the patient summary
                        summary(nhs_number)
                        # Returns to the update details menu
                        count = 3
                while count == 6:
                    telephone_number = input("Please enter your new telephone number, including country code (i.e. +447123456789)(press 0 to go back): ")
                    # Removes any character from input that is not a number
                    x = re.sub("[^0-9]","",telephone_number)
                    if telephone_number == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif telephone_number == "0":count = 3
                    # Checks if input is the right length for any telephone number
                    elif len(x) > 17 or len(x) < 11:raise InvalidTelephoneError()
                    else:
                        # Converts telephone number string into an integer
                        x = int(x)
                        # Updates telephone number in the database
                        c.execute("""UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""",(x,nhs_number))
                        connection.commit()
                        print("Successfully changed telephone number")
                        # Shows the patient summary
                        summary(nhs_number)
                        # Returns to the update details menu
                        count = 3
                while count == 7:
                    patient_email = input("Please enter your new email (press 0 to go back): ")
                    if patient_email == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif patient_email == "0":
                        count = 3
                        break
                    # Checks that input is a valid email address
                    elif not re.match(r"[^@]+@[^@]+\.[^@]+",patient_email):raise InvalidEmailError()
                    # Checks if email already exists in the database
                    c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",[patient_email])
                    patient_emails = c.fetchall()
                    if patient_emails != []:raise EmailAlreadyExistsError()
                    else: 
                        # Updates email in the database
                        c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""",(patient_email,nhs_number))
                        connection.commit()
                        print("Successfully changed email address")
                        # Shows the patient summary
                        summary(nhs_number)
                        # Returns to the update details menu
                        count = 3
                while count == 8:
                    password = input("Please enter your new password (press 0 to go back): ")
                    if password == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif password == "0":count = 3
                    else: 
                        # Updates password in the database
                        c.execute("""UPDATE PatientDetail SET password = ? WHERE nhsNumber = ?""",(password,nhs_number))
                        connection.commit()
                        print("Successfully changed password")
                        # Shows the patient summary
                        summary(nhs_number)
                        # Returns to the update details menu
                        count = 3
                while count == 9:
                    address_line_1 = input("Please enter your new address line 1 (press 0 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    address_line_1 = address_line_1.strip().title()
                    if address_line_1 == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif address_line_1 == "0":count = 3
                    # Ensures the input length is not too long
                    elif len(address_line_1) > 400:raise InvalidAnswerError()
                    else:
                        # Assigns input value to update_patient dictionary
                        global update_patient
                        update_patient = {}
                        update_patient["address_line_1"] = address_line_1
                        # Redirects to the update address line 2 while loop
                        count = 10
                while count == 10:
                    address_line_2 = input("Please enter your new address line 2, including city (press 0 to go back to update details menu, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    address_line_2 = address_line_2.strip().title()
                    # Returns to the update details menu
                    if address_line_2 == "0":count = 3
                    #  Returns to the update address line 1 while loop
                    elif address_line_2 == "1":count = 9
                    # Ensures the input length is not too long
                    elif len(address_line_2) > 400:raise InvalidAnswerError()
                    else:
                        # Assigns input value to update_patient dictionary
                        update_patient["address_line_2"] = address_line_2
                        # Redirects to the update postcode while loop
                        count = 11
                while count == 11:
                    postcode = input("Please enter your new postcode (press 0 to go back to update details menu, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises each letter
                    postcode = postcode.strip().upper()
                    if postcode == "":raise EmptyAnswerError()
                    # Returns to the update details menu
                    elif postcode == "0":count = 3
                    # Returns to the update address line 2 while loop
                    elif postcode == "1":count = 10
                    # Ensures the input length is not too long
                    elif len(postcode) > 50:raise InvalidAnswerError()
                    else:
                        # Assigns input value to update_patient dictionary
                        update_patient["postcode"] = postcode
                        # Updates address line 1 in the database
                        c.execute("""UPDATE PatientDetail SET addressLine1 = ? WHERE nhsNumber = ?""",(update_patient["address_line_1"],nhs_number))
                        connection.commit()
                        # Updates address line 2 in the database
                        c.execute("""UPDATE PatientDetail SET addressLine2 = ? WHERE nhsNumber = ?""",(update_patient["address_line_2"],nhs_number))
                        connection.commit()
                        # Updates the postcode in the database
                        c.execute("""UPDATE PatientDetail SET postcode = ? WHERE nhsNumber = ?""",(update_patient["postcode"],nhs_number))
                        connection.commit()
                        print("Successfully changed address")
                        # Shows the patient summary
                        summary(nhs_number)
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
    # nhs_number declared here because it is assigned later in various while loops in this function
    nhs_number = ""
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
                    if (action == ""):raise EmptyAnswerError()
                    # Redirects to patient login with email while loop
                    elif action == "1":count = 1
                    # Redirects to patient login with NHS number while loop
                    elif action == "2":count = 3
                    # Redirects to task() (the main menu for patients)
                    elif action == "0":return 0
                    else:raise InvalidAnswerError()
                while count == 1: 
                    patient_email = input("Email (press 0 to go back): ")
                    if patient_email =="":raise EmptyAnswerError()
                    # Returns to the login menu
                    if patient_email == "0":
                        count = 0
                        break
                    # Checks that input is a valid email address
                    elif not re.match(r"[^@]+@[^@]+\.[^@]+",patient_email):raise InvalidEmailError()
                    # Checks if email exists in the database
                    c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",[patient_email])
                    patient_emails = c.fetchall()
                    if patient_emails == []:raise EmailDoesNotExistError()
                    # Redirects to password while loop
                    else:count = 2
                while count == 2:
                    # Fetches patient record from database that matches their email to check password
                    c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",[patient_email])
                    patient_emails = c.fetchall()
                    password = input("Password (press 0 to go back): ")
                    # Returns to the email while loop
                    if password == "0":count = 1
                    elif password != patient_emails[0][10]:raise PasswordIncorrectError()
                    else:
                        # Assigns this patient's NHS number
                        nhs_number = patient_emails[0][0]
                        # Redirects to the check registration while loop
                        count = 5
                while count == 3:
                    nhs_number = input("NHS Number (press 0 to go back): ")
                    # Returns to the login menu
                    if nhs_number == "0":count = 0
                    else:
                        # Removes any character from input that is not a number
                        nhs_number = int(re.sub("[^0-9]","",nhs_number))
                        # Checks if NHS number exists in the database
                        c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?",[nhs_number])
                        nhs_numbers = c.fetchall()
                        if nhs_numbers == []:raise NHSDoesNotExistError()
                        # Redirects to patient login with NHS number while loop
                        else:count = 4
                while count == 4:
                    # Fetches patient record from database that matches their NHS number to check password
                    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?",[nhs_number])
                    nhs_numbers = c.fetchall()
                    password = input("Password (press 0 to go back): ")
                    # Returns to the NHS number while loop
                    if password == "0":count = 3
                    # Checks if the password input matches the password in the database
                    elif password != nhs_numbers[0][10]:raise PasswordIncorrectError()
                    else:
                        # Assigns this patient's NHS number
                        nhs_number = nhs_numbers[0][0]
                        # Redirects to the check registration while loop
                        count = 5
                while count == 5:
                    # Fetches patient record from database that matches the nhs_number global variable to check registration
                    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?",[nhs_number])
                    results = c.fetchall()
                    if results[0][11] == 0:
                        count = 6
                        raise NotRegisteredError()
                        # Redirects to task() (the main menu for patients)
                        return 0
                    else:
                        # count = 6 to break the outer while loop
                        count = 6
                        # Redirects to options(nhs_number) only when the patient successfully logs in and is registered
                        options(nhs_number)
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
        # Redirects to task() (the main menu for patients)
        return 0

def register():
    """ 
    Function to register new patients. 

    Allows new patients to provide their first name, last name, date of birth, gender, address, telephone number, email, 
    and password. Once they submit their details, they are sent back to the main menu for patients. 
    """
    # Uses patient.py to create new patient
    new_patient = Patient()
    count = 0
    while True:
        while count < 10:
            try:
                while count == 0:
                    first_name = input("Please enter your first name (press 0 to exit registration): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    first_name = first_name.strip().title()
                    # Removes all spaces from input
                    x = first_name.replace(" ","")
                    if first_name == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif first_name == "0":return 0
                    # Checks if there are any numbers in the input
                    elif (any(str.isdigit(y) for y in x)) == True:raise InvalidAnswerError()
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.first_name = first_name
                        # Redirects to the last name while loop
                        count = 1
                while count == 1:
                    last_name = input("Please enter your last name (press 0 to exit registration, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    last_name = last_name.strip().title()
                    # Removes all spaces from input
                    x = last_name.replace(" ","")
                    if last_name == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif last_name == "0":return 0
                    # Returns to the first name while loop
                    elif last_name == "1":count = 0
                    # Checks if there are any numbers in the input
                    elif (any(str.isdigit(y) for y in x)) == True:raise InvalidAnswerError()
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.last_name = last_name
                        # Redirects to the date of birth while loop
                        count = 2
                while count == 2:
                    date_of_birth = input("Please enter your birthday in YYYY-MM-DD format (press 0 to exit registration, press 1 to go back): ")
                    if date_of_birth == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif date_of_birth == "0":return 0
                    # Returns to last name the while loop
                    elif date_of_birth == "1":
                        count = 1
                        break
                    # Removes all spaces and hyphens from input
                    x = date_of_birth.replace(" ","")
                    x = x.replace("-","")
                    # Checks if the input is the right length, if the hyphens are in the right place, and all characters besides the hyphens are numbers
                    if (len(date_of_birth) != 10) or (date_of_birth[4] != "-" or date_of_birth[7] != "-") or (x.isdigit() == False):raise DateFormatError()
                    # Separates day, month, and year to check them individually
                    day = date_of_birth[8:10]
                    month = date_of_birth[5:7]
                    year = date_of_birth[0:4]
                    # Checks that the day, month, and year are all digits i.e. no hyphens for negative inputs
                    if (day.isdigit() == False) or (month.isdigit() == False) or (year.isdigit() == False):raise DateInvalidError()
                    # Converts day, month, and year into integers to check they exist in the calendar
                    int_day = int(day)
                    int_month = int(month)
                    int_year = int(year)
                    # Checks int_month input is 1 - 12
                    if int_month > 12 or int_month < 1:raise DateInvalidError()
                    # Checks int_day input does not exceed 30 for September, April, June, and November
                    elif (int_month == 9 or int_month == 4 or int_month == 6 or int_month == 11) and int_day > 30:raise DateInvalidError()
                    # Checks int_day input does not exceed 28 for February for a int_year that is not a leap year
                    elif int_month == 2 and int_year % 4 != 0 and int_day > 28:raise DateInvalidError()
                    # Checks int_day input does not exceed 29 for February for a int_year that is a leap year
                    elif int_month == 2 and int_year % 4 == 0 and int_day > 29:raise DateInvalidError()
                    # Checks int_day input is 1 - 31
                    elif int_day > 31 or int_day < 1:raise DateInvalidError()
                    # Converts date of birth input into a date object
                    final_date_of_birth = datetime.date(int_year,int_month,int_day)
                    today = date.today()
                    # Checks date of birth input is not in the future
                    if final_date_of_birth > today:raise DateInFutureError()
                    else:
                        # Assigns date object to new_patient instance
                        new_patient.date_of_birth = final_date_of_birth
                        # Redirects to the gender while loop
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
                    if choice == "":raise EmptyAnswerError()
                    elif choice == "1":
                        # Assigns input value to new_patient instance
                        new_patient.gender = "Female"
                        # Redirects to the address line 1 while loop
                        count = 4
                    elif choice == "2":
                        # Assigns input value to new_patient instance
                        new_patient.gender = "Male"
                        # Redirects to the address line 1 while loop
                        count = 4
                    elif choice == "3":
                        # Assigns input value to new_patient instance
                        new_patient.gender = "Non-Binary"
                        # Redirects to the address line 1 while loop
                        count = 4
                    # Redirects to task() (the main menu for patients)
                    elif choice == "4":return 0
                    # Returns to the date of birth while loop
                    elif choice == "5":count = 2
                    else:raise InvalidAnswerError()
                while count == 4:
                    address_line_1 = input("Address Line 1 (press 0 to exit registration, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    address_line_1 = address_line_1.strip().title()
                    if address_line_1 == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif address_line_1 == "0":return 0
                    # Returns to the gender while loop
                    elif address_line_1 == "1":count = 3
                    # Ensures the input length is not too long
                    elif len(address_line_1) > 400:raise InvalidAnswerError()
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.address_line_1 = address_line_1
                        # Redirects to the address line 2 while loop
                        count = 5
                while count == 5:
                    address_line_2 = input("Address Line 2, including city (press 0 to exit registration, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises the first letter of each word
                    address_line_2 = address_line_2.strip().title()
                    # Redirects to task() (the main menu for patients)
                    if address_line_2 == "0":return 0
                    # Returns to the address line 1 while loop
                    elif address_line_2 == "1":count = 4
                    # Ensures the input length is not too long
                    elif len(address_line_2) > 400:raise InvalidAnswerError()
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.address_line_2 = address_line_2
                        # Redirects to the postcode while loop
                        count = 6
                while count == 6:
                    postcode = input("Postcode (press 0 to exit registration, press 1 to go back): ")
                    # Removes preceding and trailing spaces and capitalises each letter
                    postcode = postcode.strip().upper()
                    if postcode == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif postcode == "0":return 0
                    # Returns to the city while loop
                    elif postcode == "1":count = 5
                    # Ensures the input length is not too long
                    elif len(postcode) > 50:raise InvalidAnswerError()
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.postcode = postcode
                        # Redirects to the telephone number while loop
                        count = 7
                while count == 7:
                    telephone_number = input("Telephone number, including country code (i.e. +447123456789)(press 0 to exit registration, press 1 to go back): ")
                    # Removes any character from input that is not a number
                    x = re.sub("[^0-9]","",telephone_number)
                    if (telephone_number == ""):raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif telephone_number == "0":return 0
                    # Returns to the postcode while loop
                    elif telephone_number == "1":count = 6
                    # Checks if input is the right length for any telephone number
                    elif len(x) > 17 or len(x) < 11:raise InvalidTelephoneError()
                    else:
                        # Converts telephone number string into an integer
                        x = int(x)
                        # Assigns input value to new_patient instance
                        new_patient.telephone_number = x
                        # Redirects to the email while loop
                        count = 8
                while count == 8:
                    patient_email = input("Email (press 0 to exit registration, press 1 to go back): ")
                    if patient_email == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif patient_email == "0":return 0
                    # Returns to the telephone number while loop
                    elif patient_email == "1":
                        count = 7
                        break
                    # Checks that input is a valid email address
                    elif not re.match(r"[^@]+@[^@]+\.[^@]+",patient_email):raise InvalidEmailError() 
                    # Checks if email already exists in the database
                    c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",[patient_email])
                    patient_emails = c.fetchall()
                    if patient_emails != []:raise EmailAlreadyExistsError()
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.patient_email = patient_email
                        # Redirects to the password while loop
                        count = 9
                while count == 9:
                    password = input("Password (press 0 to exit registration, press 1 to go back): ")
                    if password == "":raise EmptyAnswerError()
                    # Redirects to task() (the main menu for patients)
                    elif password == "0":return 0
                    # Returns to the email while loop
                    elif password == "1":count = 8
                    else:
                        # Assigns input value to new_patient instance
                        new_patient.password = password
                        # count = 10 to break the outer while loop
                        count = 10
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
        # Inserts new patient into the database
        new_patient.register()
        logging.info("Registered Patient: %s, %s\nNHS number: %s %s %s"%(new_patient.last_name.upper(),new_patient.first_name.upper(),new_patient.nhs_number[0:3],new_patient.nhs_number[3:6],new_patient.nhs_number[6:10]))
        print("Thank you, %s, for submitting your details to our practice. An administrator will confirm your registration within 1-3 working days."%(new_patient.first_name))
        # To see the patient summary
        summary(new_patient.nhs_number)
        # Redirects to task() (the main menu for patients)
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
        if action == "":raise EmptyAnswerError()
        # Redirects to register function
        elif action == "1":register()
        # Redirects to login function
        elif action == "2":login()
        # Redirects to root.py (the program main menu)
        elif action == "3":return 0
        elif action == "0":
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            # Exits program
            exit()
        else:raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        task()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        task()

import sqlite3 as sql
# Hipp, R.D., 2020. SQLite, Available at: https://www.sqlite.org/index.html.
from datetime import datetime as dt
from datetime import date 
import useful_functions as uf
import pandas as pd
# McKinney, W. & others, 2010. Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference. pp. 51–56.
import logging

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class FieldEmptyError(Error):
    """
    Exception raised when the user provides a blank input

    :param: message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Field cannot be left empty, please provide an input > \n"):
        self.message = message
        super().__init__(self.message)

class OutOfBounds(Error):
    """ Exception raised when the input is out of bounds """
    def __init__(self, message = "\n   < Please enter either 1, 2, or 3 > \n"):
        self.message = message
        super().__init__(self.message)

class EmailInUseError(Error):
    """
    Exception raised when the email is already in use

    :param: email - input email which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Email already in use > \n"):
        self.message = message
        super().__init__(self.message)

class EmailInvalidError(Error):
    """
    Exception raised when the email does not contain @ or .co

    :param: email - input email which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, email, message = "\n   < Please enter a valid email > \n"):
        self.email = email
        self.message = message
        super().__init__(self.message)

class NhsNotExistsError(Error):
    """Exception raised when NHS does not exist

    :param: NHS Number - input NHS Number which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Please enter an existing NHS number > \n"):
        self.message = message
        super().__init__(self.message)

class DateInvalidError(Error):
    """
    Exception raised when the date is not in the correct format (dd/mm/yyyy)

    :param: date - input date which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Date does not exist, please enter a valid date > \n"):
        self.message = message
        super().__init__(self.message)

class DateInFutureError(Error):
    """
    Exception raised when the date of birth is in the future

    :param: date - input date which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Date of birth cannot be in the future > \n"):
        self.message = message
        super().__init__(self.message)

class DateFormatError(Error):
    """
    Exception raised when the date of birth is not in the format dd/mm/yyyy

    :param: date - input date which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Please enter the date in the correct format, with '-'s as separators > \n"):
        self.message = message
        super().__init__(self.message)

class TeleNoFormatError(Error):
    """
    Exception raised when the inputted phone number is not in the format +<country code>xxxxxxxxxx

    :param: message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Please enter the phone number in the correct format > \n"):
        self.message = message
        super().__init__(self.message)

class IncorrectInputLengthError(Error):
    """
    Exception raised when the input length is incorrect

    :param: correct_length - input length that the input should be
            message - explanation of the error to the user
    """
    def __init__(self, correct_length):
        self.correct_length = str(correct_length)
        self.message = "\n   < Please enter the correct input length, input should be {} characters long > \n" .format(correct_length)
        super().__init__(self.message)

class GenderError(Error):
    """
    Exception raised when the input gender is incorrect

    :param: message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Please enter one of the options shown > \n"):
        self.message = message
        super().__init__(self.message)


class InvalidAddError(Error):
    """exception raised when address is not valid

    :param: address - input address which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "\n   < Please input an address containing number and street > \n"):
        self.message = message
        super().__init__(self.message)

class IntegerError(Error):
    """exception raised when integer is not in choice range"""
    def __init__(self, message = "\n   < Please input a valid number > \n"):
        self.message = message
        super().__init__(self.message)

class YNError(Error):
    """exception raised when input is not in Y/N"""
    def __init__(self, message = "\n   < Please enter Y/N > \n"):
        self.message = message
        super().__init__(self.message)


class AdminFunctions():
    """This is a class containing functions used in the Admin side of the program."""

    def __init__(self): 
        """The constructor for the AdminFunctions class."""
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()  

    def admin_login(self):
        """
        The function to request login details from the user and verify them to allow the user to login.

        Returns: 
            'restart' if the user enters 0 to go back.
            True if the user enters correct details.
        """
        email = input('Email: (press 0 to go back) ')
        if email == '0':
            return "restart"
        self.c.execute("SELECT * FROM Admin WHERE email = ?", (email,))
        items = self.c.fetchall()
        while len(items) == 0:
            print("\n   < I'm sorry, that email is not in our system, please try again >\n")
            email = input('Email: (press 0 to go back) ')
            if email == '0':
                return "restart"
            self.c.execute("SELECT * FROM Admin WHERE email = ?", (email,))
            items = self.c.fetchall()
        password = input('Password: (press 0 to go back) ')
        self.c.execute("SELECT * FROM Admin WHERE email=? AND password =?", (email, password))
        items = self.c.fetchall()
        while len(items) == 0:
            print("\n   < I'm sorry, that password is not correct, please try again > \n")
            password = input('Password: (press 0 to go back) ')
            if password == '0':
                return "restart"
            self.c.execute("SELECT * FROM Admin WHERE email=? AND password =?", (email, password))
            items = self.c.fetchall()
        else:
            return True

    def add_doctor(self):
        """
        The function to carry out the process of adding a new GP to the database.

        Returns:
            0 if the user enters 0 to go back.
        """
        question_num = 0
        print("Press 0 to return to the main menu at any stage")
        while True:
            try:
                while question_num == 0:
                    a = input("Email: ")
                    if a == '0':
                        print('Going back')
                        return 0
                    if not a:
                        raise FieldEmptyError()
                    if "@" not in a or (".co" not in a and ".ac" not in a and ".org" not in a and ".gov" not in a):
                        raise EmailInvalidError(a)
                    self.c.execute("SELECT * FROM GP WHERE gpEmail = ?", (a,))
                    items = self.c.fetchall()
                    if len(items) != 0:
                        raise EmailInUseError()
                    question_num = 1
                while question_num == 1:
                    pw = input("Password: ")
                    if pw == '0':
                        print('Going back')
                        return 0
                    if not pw:
                        raise FieldEmptyError()
                    question_num = 2
                while question_num == 2:
                    b = input("First name: ")
                    if b == '0':
                        print('Going back')
                        return 0
                    if not b:
                        raise FieldEmptyError()
                    question_num = 3
                while question_num == 3:
                    c = input("Last name: ")
                    if c == '0':
                        print('Going back')
                        return 0
                    if not c:
                        raise FieldEmptyError()
                    question_num = 4
                while question_num == 4:
                    dateOfBirth = (input("Enter date of birth as YYYY-MM-DD: "))
                    if dateOfBirth == '0':
                        print('Going back')
                        return 0
                    if not dateOfBirth:
                        raise FieldEmptyError()
                    if len(dateOfBirth) != 10:
                        correct_length = 10
                        raise IncorrectInputLengthError(10)
                    if dateOfBirth[4] != '-' or dateOfBirth[7] != '-':
                        raise DateFormatError
                    day = int(dateOfBirth[8:10])
                    month = int(dateOfBirth[5:7])
                    year = int(dateOfBirth[0:4])
                    if month == 9 or month == 4 or month == 6 or month == 11 and day > 30:
                        raise DateInvalidError
                    elif month == 2 and year % 4 != 0 and day > 28:
                        raise DateInvalidError
                    elif year % 4 == 0 and day > 29:
                        raise DateInvalidError
                    elif day > 31:
                        raise DateInvalidError
                    if month > 12:
                        raise DateInvalidError
                    date_entered = date(year,month,day)
                    date_today = date.today()
                    if date_entered > date_today:
                        raise DateInFutureError
                    dateOfBirth = date_entered.isoformat()
                    question_num = 5
                while question_num == 5:
                    department = input("Department: ")
                    if department == '0':
                        print('Going back')
                        return 0
                    if not department:
                        raise FieldEmptyError()
                    question_num = 6
                while question_num == 6:
                    teleNo = input("Telephone number (no spaces, with country code. E.g. +4471234123123): ")
                    if teleNo == '0':
                        print('Going back')
                        return 0
                    if not teleNo:
                        raise FieldEmptyError()
                    if '+' not in teleNo or ' ' in teleNo:
                        raise TeleNoFormatError()
                    teleNo = teleNo.replace('+', '')
                    input_list = [i for i in teleNo]
                    if len(input_list) != 11 and len(input_list) != 12 and len(input_list) != 13 and len(input_list) != 14 and len(input_list) != 15 and len(input_list) != 16 and len(input_list) != 17:
                        #input lengths from 11 to 17 are permitted, as country code lenghts range from 1 character to 7 characters.
                        correct_length = '12 to 18'
                        raise IncorrectInputLengthError(correct_length)
                    question_num = 7
                while question_num == 7:
                    gender = input("Gender (enter male/female/non-binary/prefer not to say): ")
                    gender = gender.lower()
                    if gender == '0':
                        print('Going back')
                        return 0
                    if not gender:
                        raise FieldEmptyError()
                    if gender != 'male' and gender != 'female' and gender != 'non-binary' and gender != 'prefer not to say':
                        raise GenderError()
                    active = 1
                    question_num = 8
                while question_num == 8:
                    addressL1 = input("Address Line 1: ")
                    if addressL1 == '0':
                        print('Going back')
                        return 0
                    if not addressL1:
                        raise FieldEmptyError()
                    addressL2 = input("Address Line 2: ")
                    if addressL2 == '0':
                        print('Going back')
                        return 0
                    if not addressL2:
                        raise FieldEmpty()
                    question_num = 9
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except EmailInvalidError:
                error = EmailInvalidError(a)
                print(error)
            except EmailInUseError:
                error = EmailInUseError()
                print(error)
            except ValueError:
                print("\n   < Please provide a numerical input > \n")
            except TeleNoFormatError:
                error = TeleNoFormatError()
                print(error)
            except IncorrectInputLengthError:
                error = IncorrectInputLengthError(correct_length)
                print(error)
            except GenderError:
                error = GenderError()
                print(error)
            except DateInvalidError:
                error = DateInvalidError()
                print(error)
            except DateInFutureError:
                error = DateInFutureError()
                print(error)
            except DateFormatError:
                error = DateFormatError()
                print(error)
            else:
                gp = [a, pw, b, c, gender, dateOfBirth, addressL1, addressL2, teleNo, department, active]
                self.c.execute("""INSERT INTO GP VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", gp)
                print("Details entered successfully")
                logging.info("Added new a GP to the database. Details as follows: ")
                logging.info("Email: " + str(gp[0]))
                logging.info("Password: " + str(gp[1]))
                logging.info("First Name: " + str(gp[2]))
                logging.info("Last Name: " + str(gp[3]))
                logging.info("Gender: " + str(gp[4]))
                logging.info("Date of Birth: " + str(gp[5]))
                logging.info("Address Line 1: " + str(gp[6]))
                logging.info("Address Line 2: " + str(gp[7]))
                logging.info("Telephone Number: " + str(gp[8]))
                logging.info("Department: " + str(gp[9]))
                logging.info("Active: " + str(gp[10]))
                self.connection.commit()
                return 0

    def check_registrations(self):
        """The function to check the number of new patient accounts that have pending registration confirmations."""

        self.c.execute("""SELECT COUNT(patientEmail) FROM PatientDetail WHERE registrationConfirm = 0 """)
        items = self.c.fetchall()
        count = items[0][0]
        print("   < You have {} patient registrations to confirm >" .format(count))

    def confirm_registrations(self):
        """
        The function to show the admin each patient account registration that needs to be confirmed and
        allow the admin to confirm the registration. 

        Returns:
            0 if there are no registrations to confirm.
            3 if there are registrations to confirm, and the user has gone through all of them.
        """

        print("********************************************")
        self.c.execute("""SELECT * FROM PatientDetail WHERE registrationConfirm = 0 """)
        items = self.c.fetchall()
        if len(items) == 0:
            print("No patient registrations to confirm")
            return 0
        else:
            for i in items:
                print("NHS Number: {}".format(i[0]))
                print("Email: {}".format(i[1]))
                print("First name: {}".format(i[2]))
                print("Last name: {}".format(i[3]))
                print("Date of birth: {}".format(i[4]))
                print("Gender: {}".format(i[5]))
                print("Address line 1: {}".format(i[6]))
                print("Addresss line 2: {}".format(i[7]))
                print("Postcode: {}".format(i[8]))
                tele_no = '+' + str(i[9])
                print("Telephone number: {}".format(tele_no))
                print("********************************************")
                change = ''
                while change != 'Y' and change != 'N':
                    try:
                        change = input("Do you want to confirm this registration?: (Y/N) ")
                        if change == 'Y':
                            self.c.execute("""UPDATE PatientDetail SET registrationConfirm = 1 WHERE nhsNumber = ? """,
                                        (i[0],))
                            print("Registration confirmed successfully")
                            print(" ")
                            logging.info("Registration of patient " + str(i[0]) + " set to 1")
                        elif change == 'N':
                            print("Registration not confirmed")
                            print(" ")
                        else:
                            raise YNError
                    except YNError:
                        print("Please enter Y/N")
            self.connection.commit()
            return 3

    def unconfirm_registrations(self):
        """
        The function to allow the admin to unconfirm the registration of a patient account that was
        previously confirmed. 

        Returns:
            3 if the user presses 0 to go back or successfully unconfirms an account using the account's 
            NHS number. 
        """
        while True:
            try:
                print("********************************************")
                nhs_num = input("Type in the patients NHS Number (press 0 to go back): ")
                if nhs_num == '0':
                    return 3
                if not nhs_num:
                    raise FieldEmptyError()
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            else:
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhs_num,))
                items = self.c.fetchall()
                if len(items) == 0:
                    print("No record exists with this nhsNumber")
                elif items[0][11] == 0:
                    print("\n   < This patient's registration is already unconfirmed > \n")
                else:
                    self.c.execute("""UPDATE PatientDetail SET registrationConfirm = 0 WHERE nhsNumber = ?""", (nhs_num,))
                    print("Registration unconfirmed successfully")
                    self.connection.commit()
                    logging.info("Registration of patient " + str(nhs_num) + " set to 0")
                    return 3

    def deactivate_doctor(self):
        """
        The function to allow an admin to deactivate a GP's account.

        Returns:
            2 if the user presses 0 to go back and if the user successfully deactivates an account using
            the account's email.
        """
        while True:
            try:
                print("********************************************")
                email = input("Type in the practitioner's email (press 0 to go back): ")
                if email == '0':
                    return 2
                if not email:
                    raise FieldEmptyError()
                if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                    raise EmailInvalidError(email)
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except EmailInvalidError:
                error = EmailInvalidError(email)
                print(error)
            else:
                self.c.execute("SELECT active FROM GP WHERE gpEmail = ?", (email,))
                items = self.c.fetchall()
                if len(items) == 0:
                    print("\n   < No record exists with this email> \n")
                elif items[0][0] == 0:
                    print("\n   < This practitioner has already been deactivated > \n")
                else:
                    self.c.execute("""UPDATE GP SET active = 0 WHERE gpEmail = ?""", (email,))
                    self.connection.commit()
                    logging.info("Practitioner " + str(email) + " activity status set to 0")
                    print("Record deactivated successfully")
                    return 2

    def reactivate_doctor(self):
        """
        The function to allow an admin to reactivate a GP's account.

        Returns:
            2 if the user presses 0 to go back and if the user successfully reactivates an account using
            the account's email.
        """
        while True:
            try:
                print("********************************************")
                email = input("Type in the practitioner's email (press 0 to go back): ")
                if email == '0':
                    return 2
                if not email:
                    raise FieldEmptyError()
                if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                    raise EmailInvalidError(email)
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except EmailInvalidError:
                error = EmailInvalidError(email)
                print(error)
            else:
                self.c.execute("SELECT active FROM GP WHERE gpEmail = ?", (email,))
                items = self.c.fetchall()
                if len(items) == 0:
                    print("\n   < No record exists with this email> \n")
                elif items[0][0] == 1:
                    print("\n   < This practitioner is already active > \n")
                else:
                    self.c.execute("""UPDATE GP SET active = 1 WHERE gpEmail = ?""", (email,))
                    self.connection.commit()
                    logging.info("Practitioner " + str(email) + " activity status set to 1")
                    print("Record reactivated successfully")
                    return 2

    def delete_doctor(self):
        """
        The function to allow an admin to delete a GP's account.

        Returns:
            2 if the user presses 0 to go back and if the user successfully deletes an account using
            the account's email.
        """
        while True:
            try:
                print("********************************************")
                email = input("Type in the practitioner's email (press 0 to go back): ")
                if email == "0":
                    return 2
                if not email:
                    raise FieldEmptyError()
                if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                    raise EmailInvalidError(email)
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except EmailInvalidError:
                error = EmailInvalidError(email)
                print(error)
            else:
                self.c.execute("SELECT * FROM GP WHERE gpEmail = ?", (email,))
                items = self.c.fetchall()
                if len(items) == 0:
                    print("\n   < No record exists with this email > \n")
                else:
                    self.c.execute("DELETE FROM GP WHERE gpEmail = ?", (email,))
                    self.connection.commit()
                    print("Record deleted successfully")
                    logging.info("Practitioner " + str(email) + " deleted")
                    return 2

    def c_in(self):
        """Entering patient NHS number allows admin to check-in patient from existing
        appointments

        The appointments that are available to a specific NHS number are only those that
        have been confirmed.  Invalid NHS numbers and no confirmed appointments will prompt errors.
        """

        master_back = 1
        while master_back == 1:
            try:
                print("********************************************")
                nhs_number = input("Enter patient NHS number (press 0 to go back): ")  # Will be 10 digits
                self.c.execute("""SELECT appointmentID, start FROM Appointment 
                    WHERE nhsNumber =? and AppointmentStatus = "Accepted" ORDER BY appointmentID ASC""", [nhs_number])
                appointments = self.c.fetchall()
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhs_number,))
                nhsq = self.c.fetchall()  # list of patients with matching NHS number
                if nhs_number == "0":
                    master_back = 2
                    break
                elif not nhs_number:
                    raise FieldEmptyError()
                elif len(nhsq) < 1:
                    raise NhsNotExistsError  # Check if NHS number exists in database
                elif len(appointments) == 0:  # Check if appointments is empty
                    raise DateInvalidError
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except DateInvalidError:
                print("\n   <This person has no booked appointments> \n")
            except NhsNotExistsError:
                error = NhsNotExistsError()
                print(error)
            else:
                print("********************************************")
                print("AppointmentID".ljust(15, ' '), "Start Time")
                for i in appointments:
                    print(str(i[0]).ljust(15, " "), uf.unix_to_regular_time(i[1]))
                back1 = 1
                while back1 == 1:
                    try:
                        intime = dt.now()
                        print("********************************************")
                        In = str(input("Type in appointment id to check in (press 0 to go back): "))
                        if In == "0":
                            back1 = 2
                            break
                            #return 0
                        if not In:
                            raise FieldEmptyError()
                        check_number = int(In)
                    except FieldEmptyError:
                        error = FieldEmptyError()
                        print(error)
                    except ValueError:
                        print("\n   < Please provide a numerical input >\n")
                    else:
                        self.c.execute("""SELECT * FROM Appointment WHERE appointmentID = ? and nhsNumber = ?
                                    and appointmentStatus = "Accepted" """, (check_number, nhs_number))
                        items = self.c.fetchall()
                        if len(items) == 0:
                            print("< No record exists with this appointmentID >")
                            return 1
                        self.c.execute("SELECT checkIn FROM Appointment WHERE appointmentID = ?", (check_number,))
                        items = self.c.fetchall()
                        if items[0][0] != 0:
                            print("< A check-in time has already been provided for that appointment >")
                            return 1
                        else:
                            unix_d = dt.utcnow().timestamp()  # Finding current timestamp in unix format
                            self.c.execute("""SELECT PatientDetail.firstName FROM PatientDetail INNER JOIN
                            Appointment ON PatientDetail.nhsNumber = Appointment.nhsNumber WHERE
                            appointmentID = ?""", (check_number,))  #  Selecting patient name
                            firstsel = self.c.fetchall()
                            self.c.execute("""UPDATE Appointment SET checkIn = ? WHERE appointmentID = ? """, (unix_d, check_number))
                            self.connection.commit()
                            logging.info("Adding check-in time for appointment ID: " + str(check_number) + " to database")
                            x = dt.now().hour
                            y = dt.now().minute
                            if y < 10:
                                print("Successfully checked in {} at {a}:{c}{b}".format(firstsel[0][0], a=x,c=0, b=y))
                            else:
                                print("Successfully checked in {} at {a}:{b}".format(firstsel[0][0], a=x, b=y))
                            return 0

    def c_out(self):
        """
        Entering patient NHS number allows admin to check-out patient from existing
        appointments

        The appointments that are available to a specific NHS number are only those that
        have been confirmed.  Invalid NHS numbers and no confirmed appointments will prompt errors.
        """

        master_back = 1
        while master_back == 1:
            try:
                print("********************************************")
                nhs_number = input("Enter patient NHS number (press 0 to go back): ")
                self.c.execute("""SELECT appointmentID, start FROM Appointment 
                    WHERE nhsNumber =? and appointmentStatus = "Accepted" ORDER BY appointmentID ASC""", [nhs_number])
                appointments = self.c.fetchall()  # Fetching all appointments with inputted NHS number
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhs_number,))
                nhsq = self.c.fetchall()
                if nhs_number == "0":
                    master_back = 2
                    break
                elif not nhs_number:
                    raise FieldEmptyError()
                elif len(nhsq) < 1:
                    raise NhsNotExistsError
                elif len(appointments) == 0:
                    raise DateInvalidError
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except DateInvalidError:
                print("\n   <This person has no booked appointments> \n")
            except NhsNotExistsError:
                error = NhsNotExistsError()
                print(error)
            else:
                print("********************************************")
                print("AppointmentID".ljust(15, ' '), "Start Time")  # Separating appointment information
                for i in appointments:
                    print(str(i[0]).ljust(15, " "), uf.unix_to_regular_time(i[1]))
                back1 = 1
                while back1 == 1:
                    try:
                        in_time = dt.now()
                        print("********************************************")
                        In = str(input("Type in appointment id to check out (press 0 to go back): "))
                        if In == "0":
                            back1 = 2
                            break
                            #return 0
                        if not In:
                            raise FieldEmptyError()
                        check_number = int(In)
                    except FieldEmptyError:
                        error = FieldEmptyError()
                        print(error)
                    except ValueError:
                        print("\n   < Please provide a numerical input >\n")
                    else:
                        self.c.execute("""SELECT * FROM Appointment WHERE appointmentID = ? and nhsNumber = ?
                         and appointmentStatus = "Accepted" """, (check_number, nhs_number))
                        items = self.c.fetchall()
                        if len(items) == 0:
                            print("< No record exists with this appointmentID >")
                            return 1
                        self.c.execute("SELECT checkOut FROM Appointment WHERE appointmentID = ?", (check_number,))
                        items = self.c.fetchall()
                        if items[0][0] != 0:  # Appointment table initializes check-in/out with a zero
                            print("< A check-out time has already been provided for that appointment >")
                            return 1
                        else:
                            unix_d = dt.utcnow().timestamp()
                            self.c.execute("""SELECT PatientDetail.firstName FROM PatientDetail INNER JOIN
                            Appointment ON PatientDetail.nhsNumber = Appointment.nhsNumber WHERE
                            appointmentID = ?""", (check_number,))
                            firstsel = self.c.fetchall()
                            self.c.execute("""UPDATE Appointment SET checkOut = ? WHERE appointmentID = ? """, (unix_d, check_number))
                            self.connection.commit()
                            logging.info(
                                "Adding check-out time for appointment ID: " + str(check_number) + " to database")
                            x = dt.now().hour
                            y = dt.now().minute
                            if y < 10:
                                print("Successfully checked out {} at {a}:{c}{b}".format(firstsel[0][0], a=x,c=0, b=y))
                            else:
                                print("Successfully checked out {} at {a}:{b}".format(firstsel[0][0], a=x, b=y))
                            return 0

    def manage_det(self):
        """
        Changing every patient detail of a specific NHS number.

        Only information from existing NHS numbers can be changed.
        Admin does not have the ability to change security information such as password.
        Nested while loops allow for logical menu navigation
        """

        master_back = 0
        while master_back == 0:
            try:
                print("********************************************")
                nhs_num = input("Enter patient NHS number (press 0 to go back): ")
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhs_num,))
                nhsq = self.c.fetchall()  # Selecting patient with inputted NHS number
                if nhs_num == '0':
                    master_back = 1
                    break
                elif not nhs_num:
                    raise FieldEmptyError()
                elif len(nhsq) < 1:
                    raise NhsNotExistsError
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            except NhsNotExistsError:
                error = NhsNotExistsError()
                print(error)
            else:
                pat_back = 0
                question_num = 1
                while pat_back == 0:
                    # Creating menu to allow easier user navigation
                    print("********************************************")
                    print("Press [0] to re-enter NHS number: ")
                    print("Press [1] to go back to update patient details menu")
                    try:
                        while question_num == 1:
                            emails = input("New email: ")
                            self.c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?", (emails,))
                            email_check = self.c.fetchall()
                            if emails == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif emails == '1':
                                return master_back
                                break
                            elif len(email_check) > 0:
                                raise EmailInUseError
                            elif "@" not in emails or ".com" not in emails:
                                raise EmailInvalidError(emails)
                            elif not emails:
                                raise FieldEmptyError
                            question_num = 2

                        while question_num == 2:
                            first = input("New first name: ")
                            if first == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif first == '1':
                                return master_back
                                break
                            elif not first:
                                raise FieldEmptyError
                            question_num = 3

                        while question_num == 3:
                            last = input("New last name: ")
                            if last == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif last == '1':
                                return master_back
                                break
                            elif not last:
                                raise FieldEmptyError
                            question_num = 4

                        while question_num == 4:
                            date_of_birth = (input("New date of birth as YYYY-MM-DD: "))
                            if date_of_birth == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif date_of_birth == '1':
                                return master_back
                                break
                            elif not date_of_birth:
                                raise FieldEmptyError()
                            elif len(date_of_birth) != 10:
                                correct_length = 10
                                raise IncorrectInputLengthError(10)
                            elif date_of_birth[4] != '-' or date_of_birth[7] != '-':
                                raise DateFormatError
                            day = int(date_of_birth[8:10])
                            month = int(date_of_birth[5:7])
                            year = int(date_of_birth[0:4])
                            if month == 9 or month == 4 or month == 6 or month == 11:
                                if day > 30:
                                    raise DateInvalidError
                            elif month == 2:
                                if year % 4 != 0:
                                    if day > 28:
                                        raise DateInvalidError
                                elif year % 4 == 0:
                                    if day > 29:
                                        raise DateInvalidError
                            else:
                                if day > 31:
                                    raise DateInvalidError
                            if month > 12:
                                raise DateInvalidError

                            # Checking if inputted date of birth is before current date.
                            date_entered = date(year, month, day)
                            date_today = date.today()
                            if date_entered > date_today:
                                raise DateInFutureError
                            date_of_birth = date_entered.isoformat()
                            question_num = 6

                        while question_num == 6:
                            gender = input("Gender (enter male/female/non-binary/prefer not to say): ")
                            if gender == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif gender == '1':
                                return master_back
                                break
                            elif not gender:
                                raise FieldEmptyError()
                            # Checking if inputted gender matches accepted values.
                            if gender != "male" and gender != "female" and gender != "non-binary" and gender != "prefer not to say":
                                raise GenderError()
                            question_num = 7

                        while question_num == 7:
                            addl1 = input("New address line 1: ")
                            if addl1 == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif addl1 == '1':
                                return master_back
                                break
                            elif not addl1:
                                raise FieldEmptyError()
                            # Address line 1 must contain a street number
                            elif any(chr.isdigit() for chr in addl1) == False:
                                raise InvalidAddError
                            question_num = 8

                        while question_num == 8:
                            addl2 = input("New address line 2: ")
                            if addl2 == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif addl2 == '1':
                                return master_back
                                break
                            elif not addl2:
                                raise FieldEmptyError()
                            question_num = 9

                        while question_num == 9:
                            postcode = input("New postcode: ")
                            if postcode == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif postcode == '1':
                                return master_back
                                break
                            elif not postcode:
                                raise FieldEmptyError()
                            question_num = 10

                        while question_num == 10:
                            # Telephone number takes in country codes of different lengths
                            tel = (input("New telephone number (no spaces, with country code. E.g. +4471234123123): "))
                            if tel == '0':
                                return adminFunctions.manage_det(self)
                                break
                            elif tel == '1':
                                return master_back
                                break
                            elif not tel:
                                raise FieldEmptyError()
                            if '+' not in tel or ' ' in tel:
                                raise TeleNoFormatError()
                            tel = tel.replace('+', '')
                            input_list = [i for i in tel]
                            if len(input_list) != 11 and len(input_list) != 12 and len(input_list) != 13 and len(input_list) != 14 and len(
                                    input_list) != 15 and len(input_list) != 16 and len(input_list) != 17 and len(input_list) != 18:
                                correct_length = '11 to 18'
                                raise IncorrectInputLengthError(correct_length)
                            question_num = 11

                    except EmailInUseError:
                        error = EmailInUseError()
                        print(error)
                    except NhsNotExistsError:
                        error = NhsNotExistsError()
                        print(error)
                    except FieldEmptyError:
                        error = FieldEmptyError()
                        print(error)
                    except IncorrectInputLengthError:
                        error = IncorrectInputLengthError(correct_length)
                        print(error)
                    except GenderError:
                        error = GenderError()
                        print(error)
                    except InvalidAddError:
                        error = InvalidAddError()
                        print(error)
                    except EmailInvalidError:
                        error = EmailInvalidError(emails)
                        print(error)
                    except TeleNoFormatError:
                        error = TeleNoFormatError()
                        print(error)
                    except ValueError:
                        print("< Please provide a numerical input >")
                    except DateInvalidError:
                        error = DateInvalidError()
                        print(error)
                    except DateInFutureError:
                        error = DateInFutureError()
                        print(error)
                    except DateFormatError:
                        error = DateFormatError()
                        print(error)
                    else:
                        self.c.execute("""UPDATE PatientDetail SET patientEmail = ?, firstName = ?, lastName = ?, dateOfBirth = ?
                        , gender = ?, addressLine1 = ?, addressLine2 = ?, postcode = ?,
                        telephoneNumber = ? WHERE nhsNumber = ?""",
                        (emails, first, last, date_of_birth, gender, addl1, addl2, postcode, tel, nhs_num))
                        self.connection.commit()
                        logging.info("Update patient record with NHS number: " + nhs_num + " to database")
                        print("Successfully updated entire patient record")
                        return master_back

    def del_pat(self):
        """Deleting the entire row of a patient record"""

        del_back = 0
        while del_back == 0:
            try:
                print("********************************************")
                nhs_num = input("Enter patient NHS number (press 0 to go back): ")
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhs_num,))
                nhsq = self.c.fetchall()
                if nhs_num == "0":
                    del_back = 1
                    break
                elif not nhs_num:
                    raise FieldEmptyError
                elif len(nhsq) < 1:
                    raise NhsNotExistsError
            except NhsNotExistsError:
                error = NhsNotExistsError()
                print(error)
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)

            else:
                self.c.execute("""DELETE FROM PatientDetail WHERE nhsNumber = ?""", (nhs_num,))
                self.connection.commit()
                print("Successfully deleted patient record")
                logging.info("Delete patient record with NHS number: " + nhs_num + " from database")
                del_back = 1

    def man_ind_det(self):
        """
        Entering an NHS number allows admin to change individual details.

        This allows user to navigate a menu and change details from that menu.
        Invalid inputs will raise errors prompting another user input.
        Options to go back to certain aspects of the function are available.
        Nested while loops allow for logical menu navigation
        """
        master_back = 0
        while master_back == 0:
            try:
                print("********************************************")
                nhs_num = input("Enter patient NHS number (press 0 to go back): ")
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhs_num,))
                nhsq = self.c.fetchall()
                if nhs_num == "0":
                    master_back = 1
                    break
                if not nhs_num:
                    raise FieldEmptyError
                elif len(nhsq) < 1:
                    raise NhsNotExistsError
            except NhsNotExistsError:
                error = NhsNotExistsError()
                print(error)
            except FieldEmptyError:
                error = FieldEmptyError()
                print(error)
            else:
                c_again = 0
                while c_again == 0:
                    # Menu of options that the user selects from in the below code
                    print("********************************************")
                    print("Choose [1] to go back to update patient details menu")
                    print("Choose [2] to update email")
                    print("Choose [3] to update first name")
                    print("Choose [4] to update last name")
                    print("Choose [5] to update date of birth")
                    print("Choose [6] to update gender")
                    print("Choose [7] to update address line 1")
                    print("Choose [8] to update address line 2")
                    print("Choose [9] to update post code")
                    print("Choose [10] to update telephone number")
                    print("********************************************")
                    try:
                        print("Press [0] to re-enter NHS number")
                        det_inp = input("Choose which detail to change: ")
                        if det_inp == '0':
                            c_again = 1
                            break
                        elif det_inp == '1':
                            master_back = 1  # User inputs a "1" to return to update patients menu
                            break
                        elif det_inp.isdigit() == False:
                            raise IntegerError
                        ind_inp = int(det_inp)
                        if ind_inp > 10:
                            raise IntegerError
                        elif not ind_inp:
                            raise FieldEmptyError
                    except FieldEmptyError:
                        error = FieldEmptyError()
                        print(error)
                    except IntegerError:
                        error = IntegerError()
                        print(error)
                    else:
                        # Menu for easier user navigation
                        print("********************************************")
                        print("Press [0] to re-enter NHS number")
                        print("Press [1] to go back to options")
                        if ind_inp == 2:
                            back = 0
                            while back == 0:
                                try:
                                    c_email = input("New email: ")
                                    self.c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?", (c_email,))
                                    email_check = self.c.fetchall()
                                    if c_email == '0':
                                        c_again = 1  # Inputting a "1" returns user to re-enter NHS number
                                        break
                                    elif c_email == '1':
                                        back = 0  # Returns user back to options menu
                                        break
                                    elif len(email_check) > 0:
                                        raise EmailInUseError
                                    elif "@" not in c_email or ".com" not in c_email:
                                        raise EmailInvalidError(c_email)
                                    elif not c_email:
                                        raise FieldEmptyError
                                except EmailInUseError:
                                    error = EmailInUseError()
                                    print(error)
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                except EmailInvalidError:
                                    error = EmailInvalidError(c_email)
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""",
                                                   (c_email, nhs_num))
                                    self.connection.commit()
                                    print("Successfully changed email")
                                    logging.info("Update patient's email to " + str(c_email) + " for NHS number: "
                                                 + nhs_num + " to database")
                                    back = 1

                        elif ind_inp == 3:
                            back2 = 0
                            while back2 == 0:
                                try:
                                    c_fn = input("New first name: ")
                                    if c_fn == '0':
                                        c_again = 1
                                        break
                                    elif c_fn == '1':
                                        back2 = 1
                                        break
                                    elif not c_fn:
                                        raise FieldEmptyError
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""",
                                                   (c_fn, nhs_num))
                                    self.connection.commit()
                                    print("Successfully changed first name")
                                    logging.info("Update patient's first name to " + str(c_fn) + " for NHS number: "
                                                 + nhs_num + " to database")
                                    back2 = 1

                        elif ind_inp == 4:
                            back3 = 0
                            while back3 == 0:
                                try:
                                    c_Ln = input("New last name: ")
                                    if c_Ln == '0':
                                        c_again = 1
                                        break
                                    elif c_Ln == '1':
                                        back3 = 1
                                        break
                                    elif not c_Ln:
                                        raise FieldEmptyError
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""",
                                                   (c_Ln, nhs_num))
                                    self.connection.commit()
                                    logging.info("Update patient's last name to " + str(c_Ln) + " for NHS number: "
                                                 + nhs_num + " to database")
                                    print("Successfully changed last name")
                                    back3 = 1

                        elif ind_inp == 5:
                            back4 = 0
                            while back4 == 0:
                                try:
                                    date_of_birth = (input("New date of birth as YYYY-MM-DD: "))
                                    if date_of_birth == '0':
                                        c_again = 1
                                        break
                                    elif date_of_birth == '1':
                                        back4 = 1
                                        break
                                    elif not date_of_birth:
                                        raise FieldEmptyError()
                                    elif len(date_of_birth) != 10:
                                        correct_length = 10
                                        raise IncorrectInputLengthError(10)
                                    elif date_of_birth[4] != '-' or date_of_birth[7] != '-':
                                        raise DateFormatError
                                    # Formatting date of birth for input checks
                                    day = int(date_of_birth[8:10])
                                    month = int(date_of_birth[5:7])
                                    year = int(date_of_birth[0:4])
                                    if month == 9 or month == 4 or month == 6 or month == 11:
                                        if day > 30:
                                            raise DateInvalidError
                                    elif month == 2:
                                        if year % 4 != 0:
                                            if day > 28:
                                                raise DateInvalidError
                                        elif year % 4 == 0:
                                            if day > 29:
                                                raise DateInvalidError
                                    else:
                                        if day > 31:
                                            raise DateInvalidError
                                    if month > 12:
                                        raise DateInvalidError

                                    # input_list = [int(i) for i in str(dateOfBirth)]
                                    # Checking if date of birth is before current date
                                    date_entered = date(year, month, day)
                                    date_today = date.today()
                                    if date_entered > date_today:
                                        raise DateInFutureError
                                    date_of_birth = date_entered.isoformat()
                                    print(date_of_birth)
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                except IncorrectInputLengthError:
                                    error = IncorrectInputLengthError(correct_length)
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
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET dateOfBirth = ? WHERE nhsNumber = ?""",
                                                   (date_of_birth, nhs_num))
                                    self.connection.commit()
                                    logging.info("Update patient's date of birth to " + str(date_of_birth)
                                                 + " for NHS number: " + nhs_num + " to database")
                                    print("Successfully changed date of birth")
                                    back4 = 1

                        elif ind_inp == 6:
                            back6 = 0
                            while back6 == 0:
                                try:
                                    c_gen = input("New gender (enter male/female/non-binary/prefer not to say): ")
                                    if c_gen == '0':
                                        c_again = 1
                                        break
                                    elif c_gen == '1':
                                        back6 = 1
                                        break
                                    elif not c_gen:
                                        raise FieldEmptyError()
                                    elif c_gen != "male" and c_gen != "female" and c_gen != "non-binary" \
                                            and c_gen != "prefer not to say":
                                        raise GenderError()
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                except GenderError:
                                    error = GenderError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET gender = ? WHERE nhsNumber = ?""",
                                                   (c_gen, nhs_num))
                                    self.connection.commit()
                                    logging.info("Update patient's gender to " + str(c_gen) + " for NHS number: "
                                                 + nhs_num + " to database")
                                    print("Successfully changed gender")
                                    back6 = 1

                        elif ind_inp == 7:
                            back7 = 0
                            while back7 == 0:
                                try:
                                    c_ad1 = input("New address line 1: ")
                                    if c_ad1 == '0':
                                        c_again = 1
                                        break
                                    elif c_ad1 == '1':
                                        back7 = 1
                                        break
                                    elif not c_ad1:
                                        raise FieldEmptyError()
                                    elif any(chr.isdigit() for chr in c_ad1) == False:
                                        raise InvalidAddError
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                except InvalidAddError:
                                    error = InvalidAddError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET addressLine1 = ? WHERE nhsNumber = ?""",
                                                   (c_ad1, nhs_num))
                                    self.connection.commit()
                                    logging.info("Update patient's address line 1 to " + str(c_ad1) +
                                                 " for NHS number: " + nhs_num + " to database")
                                    print("Successfully changed address line 1")
                                    back7 = 1

                        elif ind_inp == 8:
                            back8 = 0
                            while back8 == 0:
                                try:
                                    c_ad2 = input("new address line 2: ")
                                    if c_ad2 == '0':
                                        c_again = 1
                                        break
                                    elif c_ad2 == '1':
                                        back8 = 1
                                        break
                                    elif not c_ad2:
                                        raise FieldEmptyError()
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET addressLine2 = ? WHERE nhsNumber = ?""",
                                                   (c_ad2, nhs_num))
                                    self.connection.commit()
                                    print("Successfully changed address line 2")
                                    logging.info("Update patient's address line 2 to " + str(c_ad2)
                                                 + " for NHS number: " + nhs_num + " to database")
                                    back8 = 1

                        elif ind_inp == 9:
                            back9 = 0
                            while back9 == 0:
                                try:
                                    c_post = input("New postcode: ")
                                    if c_post == '0':
                                        c_again = 1
                                        break
                                    elif c_post == '1':
                                        back9 = 1
                                        break
                                    elif not c_post:
                                        raise FieldEmptyError()
                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET postcode = ? WHERE nhsNumber = ?""",
                                                   (c_post, nhs_num))
                                    self.connection.commit()
                                    print("Successfully changed post code")
                                    logging.info("Update patient's postcode to " + str(c_post) + " for NHS number: "
                                                 + nhs_num + " to database")
                                    back9 = 1

                        elif ind_inp == 10:
                            back10 = 0
                            while back10 == 0:
                                try:
                                    # Telephone accepts input with different country cods of a range of lengths
                                    c_tel = (
                                        input("Telephone number (no spaces, with country code. E.g. +4471234123123): "))
                                    if c_tel == '0':
                                        c_again = 1
                                        break
                                    elif c_tel == '1':
                                        back10 = 1
                                        break
                                    elif not c_tel:
                                        raise FieldEmptyError()
                                    if '+' not in c_tel or ' ' in c_tel:
                                        raise TeleNoFormatError()
                                    c_tel = c_tel.replace('+', '')
                                    input_list = [i for i in c_tel]
                                    if len(input_list) != 11 and len(input_list) != 12 and len(input_list) != 13 and \
                                            len(input_list) != 14 and len(
                                            input_list) != 15 and len(input_list) != 16 and len(
                                        input_list) != 17 and len(
                                        input_list) != 18:
                                        correct_length = '11 to 18'
                                        raise IncorrectInputLengthError(correct_length)

                                except FieldEmptyError:
                                    error = FieldEmptyError()
                                    print(error)
                                except IncorrectInputLengthError:
                                    error = IncorrectInputLengthError(correct_length)
                                    print(error)
                                except IntegerError:
                                    error = IntegerError()
                                    print(error)
                                except TeleNoFormatError:
                                    error = TeleNoFormatError()
                                    print(error)
                                else:
                                    self.c.execute(
                                        """UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""",
                                        (c_tel, nhs_num))
                                    self.connection.commit()
                                    print("Successfully changed telephone number")
                                    logging.info("Update patient telephone number to " + str(c_tel) +
                                                 " for NHS number: " + nhs_num + " to database")
                                    back10 = 1

    def commit_and_close(self):
        """Function to commit changes to the database and close the connection."""
        self.connection.commit()
        self.connection.close()

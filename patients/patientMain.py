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

""" This is the main patient menu"""

connection = sql.connect('UCH.db')
c = connection.cursor()

# All Errors


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class NotRegisteredError(Error):
    def __init__(self, message="\n   < An administrator needs to confirm your registration before you can access our services - please try logging in tomorrow > \n"):
        self.message = message
        super().__init__(self.message)


class EmptyAnswerError(Error):
    def __init__(self, message="\n   < I'm sorry, this field cannot be left empty, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class InvalidAnswerError(Error):
    def __init__(self, message="\n   < I'm sorry, this is not a valid answer, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class InvalidEmailError(Error):
    def __init__(self, message="\n   < I'm sorry, that is not a valid email, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class EmailDoesNotExistError(Error):
    def __init__(self, message="\n   < I'm sorry, that email is not in our system, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class EmailAlreadyExistsError(Error):
    def __init__(self, message="\n   < I'm sorry, that email is already in use, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class PasswordIncorrectError(Error):
    def __init__(self, message="\n   < I'm sorry, that password is not correct, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class NHSDoesNotExistError(Error):
    def __init__(self, message="\n   < I'm sorry, that NHS number is not in our system, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class InvalidTelephoneError(Error):
    def __init__(self, message="\n   < I'm sorry, that is not a valid telephone number, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class DateInvalidError(Error):
    def __init__(self, message="\n   < I'm sorry, that is not a valid date, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class DateInFutureError(Error):
    def __init__(self, message="\n   < I'm sorry, your date of birth cannot be in the future, please try again > \n"):
        self.message = message
        super().__init__(self.message)


class DateFormatError(Error):
    def __init__(self, message="\n   < I'm sorry, this date is not in the proper YYYY-MM-DD format, with '-'s as separators, please try again > \n"):
        self.message = message
        super().__init__(self.message)

# Patient Functions


def summary(NHS_number):
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
    print(one, two, three)
    print("First Name: " + str(results[0][2]))
    print("Last Name: " + str(results[0][3]))
    print("Email: " + str(results[0][1]))
    print("Date of Birth: " + str(results[0][4]))
    print("Gender: " + str(results[0][5]))
    print("Address: ")
    print(str(results[0][6]))
    print(str(results[0][7]))
    print(str(results[0][8]))
    print("Telephone Number: +" + str(results[0][9]))
    print("Password: " + hash)


def login():
    count = 0
    while True:
        try:
            while count == 0:
                print("********************************************")
                print("Choose [1] to login using your email")
                print("Choose [2] to login using your NHS number")
                print("********************************************")
                action = input("Please select an option: ")
                if action == '':
                    raise EmptyAnswerError()
                elif action == '1':
                    count = 1
                elif action == '2':
                    count = 2
                else:
                    raise InvalidAnswerError()
            while count == 1:
                return 0
            while count == 2:
                return 0
        except InvalidAnswerError:
            error = InvalidAnswerError()
            print(error)
        except EmptyAnswerError:
            error = EmptyAnswerError()
            print(error)


def register():
    new_patient = {"first_name": "",
                   "last_name": "",
                   "date_of_birth": "",
                   "gender": "",
                   "address_line_1": "",
                   "address_line_2": "",
                   "postcode": "",
                   "telephone_number": "",
                   "patient_email": "",
                   "password": ""}
    count = 0
    while True:
        try:
            while count == 0:
                first_name = input(
                    "Please enter your first name (press 0 to exit registration): ")
                first_name = first_name.strip().title()
                if first_name == '':
                    raise EmptyAnswerError()
                elif first_name == '0':
                    return 0
                x = first_name.replace(" ", "")
                if (any(str.isdigit(y) for y in x)) == True:
                    raise InvalidAnswerError()
                else:
                    new_patient["first_name"] = first_name
                    count = 1
            while count == 1:
                last_name = input(
                    "Please enter your last name (press 0 to exit registration, press 1 to go back): ")
                last_name = last_name.strip().title()
                if last_name == '':
                    raise EmptyAnswerError()
                elif last_name == '0':
                    return 0
                # elif last_name == '1':
                #     count = 0
                else:
                    x = last_name.replace(" ", "")
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
                # elif date_of_birth == '1':
                #     count = 1
                x = date_of_birth.replace(" ", "")
                x = x.replace("-", "")
                if (len(date_of_birth) != 10) or (date_of_birth[4] != '-' or date_of_birth[7] != '-') or (x.isdigit() == False):
                    raise DateFormatError()
                day = date_of_birth[8:10]
                month = date_of_birth[5:7]
                year = date_of_birth[0:4]
                if (day.isdigit() == False) or (month.isdigit() == False) or (year.isdigit() == False):
                    raise DateInvalidError()
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
                    date_of_birth = datetime.date(year, month, day)
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
                # elif choice == "5":
                #     count = 2
                else:
                    raise InvalidAnswerError()
            while count == 4:
                address_line_1 = input(
                    "Address Line 1 (press 0 to exit registration, press 1 to go back): ")
                address_line_1 = address_line_1.strip().title()
                if address_line_1 == '':
                    raise EmptyAnswerError()
                elif address_line_1 == '0':
                    return 0
                # elif address_line_1 == "1":
                #     count = 3
                elif len(address_line_1) > 100:
                    raise InvalidAnswerError()
                else:
                    new_patient["address_line_1"] = address_line_1
                    count = 5
            while count == 5:
                address_line_2 = input(
                    "Address Line 2 (press 0 to exit registration, press 1 to go back): ")
                address_line_2 = address_line_2.strip().title()
                if address_line_2 == '0':
                    return 0
                # elif address_line_2 == "1":
                #     count = 4
                elif len(address_line_2) > 100:
                    raise InvalidAnswerError()
                else:
                    new_patient["address_line_2"] = address_line_2
                    count = 6
            while count == 6:
                city = input(
                    "City (press 0 to exit registration, press 1 to go back): ")
                city = city.strip().title()
                if city == '':
                    raise EmptyAnswerError()
                elif city == '0':
                    return 0
                # elif city == "1":
                #     count = 5
                elif len(city) > 100:
                    raise InvalidAnswerError()
                else:
                    x = city.replace(" ", "")
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
                # elif postcode == "1":
                #     count = 6
                elif len(postcode) > 100:
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
                # elif telephone_number == "1":
                #     count = 7
                else:
                    telephone_number = re.sub("[^0-9]", "", telephone_number)
                    if len(telephone_number) > 17 or len(telephone_number) < 11:
                        raise InvalidTelephoneError()
                    else:
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
                # elif patient_email == "1":
                #     count = 8
                elif re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
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
                # elif password == "1":
                #     count = 9
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
        else:
            x = Patient(new_patient["patient_email"], new_patient["first_name"], new_patient["last_name"], new_patient["date_of_birth"], new_patient["gender"],
                        new_patient["address_line_1"], new_patient["address_line_2"], new_patient["postcode"], new_patient["telephone_number"], new_patient["password"])
            x.register()
            print("Thank you, " + x.first_name +
                  ", for submitting your details to our practice. An administrator will confirm your registration within 1-3 working days.")
            summary(x.NHS_number)
            return 0

# Main Patient Function


def task():
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

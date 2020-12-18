import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.PatientRiskProfile import PatientMedical
from patients.lifeStyleQuestionnaire import RiskProfile
from patients.appointment import Appointment
import re
import string
import usefulfunctions as uf

""" This is the main patient menu"""

connection = sql.connect('UCH.db')
c = connection.cursor()

# All Errors


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class NotRegisteredError(Error):
    def __init__(self, message="\n   < A GP needs to confirm your registration before you can access our services - please try logging in tomorrow > \n"):
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
    def __init__(self, message="\n   < I'm sorry, this date in not in the proper YYYY-MM-DD format, with '-'s as separators, please try again > \n"):
        self.message = message
        super().__init__(self.message)

# Patient Functions

def summary(nhsNumber):
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
    results = c.fetchall()
    dateOfBirth = uf.toregulartime(results[0][4])
    dateOfBirth = str(dateOfBirth)[0:10]
    hash = ""
    for i in results[0][10]:
        hash += "*"
    print("--------------------------------------------")
    print("Patient Summary of " + str(results[0][2]) + " " + str(results[0][3]))
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
    print("Date of Birth: " + str(dateOfBirth))
    print("Gender: " + str(results[0][5]))
    print("Address: ")
    print(str(results[0][6]))
    print(str(results[0][7]))
    print(str(results[0][8]))
    print("Telephone Number: +" + str(results[0][9]))
    print("Password: " + hash)

def check_NHS(nhsNumber):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        results = c.fetchall()
        if results[0][11] == 0:
            raise NotRegisteredError()
    except NotRegisteredError:
        error = NotRegisteredError()
        print(error)
        exit()
    else:
        options(nhsNumber)


def quest_options(nhsNumber):
    try:
        print("********************************************")
        print("Choose [1] to see your medical profile")
        print("Choose [2] to take the lifestyle risk questionnaire")
        print("Choose [3] to update your medical history")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise EmptyAnswerError()
        elif action == '1':
            name = PatientMedical(nhsNumber)
            name.show_profile(nhsNumber)
            options(nhsNumber)
        elif action == '2':
            print("Please fill out the following risk profile")
            x = RiskProfile(nhsNumber)
            x.questions(nhsNumber)
            x.BMI_calculator(nhsNumber)
            x.smoking(nhsNumber)
            x.drugs(nhsNumber)
            x.alcohol(nhsNumber)
            x.diet(nhsNumber)
            x.insert_to_table(nhsNumber)
            options(nhsNumber)
        elif action == '3':
            x = PatientMedical(nhsNumber)
            x.vaccination(nhsNumber)
            x.cancer(nhsNumber)
            options(nhsNumber)
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        quest_options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        quest_options(nhsNumber)

def logout():
    from root.py import Menus
    x = Menu()
    x.MasterMenu()

def options(nhsNumber):
    try:
        uf.banner('Patient')
        print("What would you like to do next?")
        print("Choose [1] to book an appointment")
        print("Choose [2] to view your confirmed appointments")
        print("Choose [3] to cancel an appointment")
        print("Choose [4] to see your medical profile")
        print("Choose [5] to see your contact details")
        print("Choose [6] to update your contact details")
        print("Choose [0] to log out")
        action = input("Please select an option: ")
        if action == '':
            raise EmptyAnswerError()
        elif action == '1':
            x = Appointment()
            x.bookAppointment(nhsNumber)
            options(nhsNumber)
        elif action == '2':
            x = Appointment()
            x.viewAppConfirmations(nhsNumber)
            options(nhsNumber)
        elif action == '3':
            x = Appointment()
            x.cancelAppointment(nhsNumber)
            options(nhsNumber)
        elif action == '4':
            quest_options(nhsNumber)
        elif action == '5':
            summary(nhsNumber)
            options(nhsNumber)
        elif action == '6':
            summary(nhsNumber)
            update_options(nhsNumber)
        elif action == '0':
            logout()
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        options(nhsNumber)

def update_options(nhsNumber):
    try:
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
            update_first_name(nhsNumber)
        elif action == '2':
            update_last_name(nhsNumber)
        elif action == '3':
            updatePatient = {"addressLine1": "",
                  "addressLine2": "",
                  "postcode": ""}
            update_address_line_1(nhsNumber,updatePatient)
        elif action == '4':
            update_telephone_number(nhsNumber)
        elif action == '5':
            update_patient_email(nhsNumber)
        elif action == '6':
            update_password_check(nhsNumber)
        elif action == '0':
            options(nhsNumber)
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_options(nhsNumber)

def update_first_name(nhsNumber):
    try:
        firstName = input("Please enter your new first name (press 0 to go back): ")
        firstName = string.capwords(firstName.strip())
        if firstName == '':
            raise EmptyAnswerError()
        elif firstName == '0':
            update_options(nhsNumber)
        x = firstName.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""", (firstName, nhsNumber))
            connection.commit()
            print("Successfully changed first name")
            summary(nhsNumber)
            options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_first_name(nhsNumber)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_first_name(nhsNumber)

def update_last_name(nhsNumber):
    try:
        lastName = input("Please enter your new last name (press 0 to go back): ")
        lastName = string.capwords(lastName.strip())
        if lastName == '':
            raise EmptyAnswerError()
        elif lastName == '0':
            update_options(nhsNumber)
        x = lastName.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            c.execute("""UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""", (lastName, nhsNumber))
            connection.commit()
            print("Successfully changed last name")
            summary(nhsNumber)
            options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_last_name(nhsNumber)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_last_name(nhsNumber)

def update_address_line_1(nhsNumber, updatePatient):
    try:
        addressLine1 = input("Please enter your new address line 1 (press 0 to go back): ")
        addressLine1 = string.capwords(addressLine1.strip())
        if addressLine1 == '':
            raise EmptyAnswerError()
        elif addressLine1 == '0':
            update_options(nhsNumber)
        elif len(addressLine1) > 100:
            raise InvalidAnswerError()
        else:
            updatePatient["addressLine1"] = addressLine1
            update_address_line_2(nhsNumber,updatePatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_address_line_1(nhsNumber, updatePatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_address_line_1(nhsNumber, updatePatient)

def update_address_line_2(nhsNumber, updatePatient):
    try:
        addressLine2 = input("Please enter your new address line 2 (press 0 to go back to update details menu, press 1 to go back): ")
        addressLine2 = string.capwords(addressLine2.strip())
        if addressLine2 == '0':
            update_options(nhsNumber)
        elif addressLine2 == "1":
            update_address_line_1(nhsNumber, updatePatient)
        elif len(addressLine2) > 100:
            raise InvalidAnswerError()
        else:
            updatePatient["addressLine2"] = addressLine2
            update_city(nhsNumber, updatePatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_address_line_2(nhsNumber, updatePatient)

def update_city(nhsNumber, updatePatient):
    try:
        city = input("Please enter your new city (press 0 to go back to update details menu, press 1 to go back): ")
        city = string.capwords(city.strip())
        if city == '':
            raise EmptyAnswerError()
        elif city == '0':
            update_options(nhsNumber)
        elif city == "1":
            update_address_line_2(nhsNumber, updatePatient)
        elif len(city) > 100:
            raise InvalidAnswerError()
        x = city.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            addressLine2 = (updatePatient["addressLine2"] + " " + city).strip()
            updatePatient["addressLine2"] = addressLine2
            update_postcode(nhsNumber, updatePatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_city(nhsNumber, updatePatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_city(nhsNumber, updatePatient)

def update_postcode(nhsNumber, updatePatient):
    try:
        postcode = input("Please enter your new postcode (press 0 to go back to update details menu, press 1 to go back): ")
        postcode = postcode.strip().upper()
        if postcode == '':
            raise EmptyAnswerError()
        elif postcode == '0':
            update_options(nhsNumber)
        elif postcode == "1":
            update_city(nhsNumber, updatePatient)
        elif len(postcode) > 100:
            raise InvalidAnswerError()
        else:
            updatePatient["postcode"] = postcode
            c.execute("""UPDATE PatientDetail SET addressLine1 = ? WHERE nhsNumber = ?""", (updatePatient["addressLine1"], nhsNumber))
            connection.commit()
            c.execute("""UPDATE PatientDetail SET addressLine2 = ? WHERE nhsNumber = ?""", (updatePatient["addressLine2"], nhsNumber))
            connection.commit()
            c.execute("""UPDATE PatientDetail SET postcode = ? WHERE nhsNumber = ?""", (updatePatient["postcode"], nhsNumber))
            connection.commit()
            print("Successfully changed address")
            summary(nhsNumber)
            options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_postcode(nhsNumber, updatePatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_postcode(nhsNumber, updatePatient)

def update_telephone_number(nhsNumber):
    try:
        telephoneNumber = input("Please enter your new telephone number, including country code (i.e. +447123456789)(press 0 to go back): ")
        if telephoneNumber == '':
            raise EmptyAnswerError()
        elif telephoneNumber == '0':
            update_options(nhsNumber)
        telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
        if len(telephoneNumber) > 12 or len(telephoneNumber) < 11:
            raise InvalidTelephoneError()
        else:
            telephoneNumber = int(telephoneNumber)
            c.execute("""UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""", (telephoneNumber, nhsNumber))
            connection.commit()
            print("Successfully changed telephone number")
            summary(nhsNumber)
            options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_telephone_number(nhsNumber)
    except InvalidTelephoneError:
        error = InvalidTelephoneError()
        print(error)
        update_telephone_number(nhsNumber)

def update_patient_email(nhsNumber):
    try:
        patientEmail = input("Please enter your new email (press 0 to go back): ")
        if patientEmail == '':
            raise EmptyAnswerError()
        elif patientEmail == '0':
            update_options(nhsNumber)
        elif re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            update_patient_email_check(nhsNumber, patientEmail)
        else:
            raise InvalidEmailError()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_patient_email(nhsNumber)
    except InvalidEmailError:
        error = InvalidEmailError()
        print(error)
        update_patient_email(nhsNumber)

def update_patient_email_check(nhsNumber, patientEmail):
    try:
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?",
              [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails != []:
            raise EmailAlreadyExistsError()
        else:
            c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""", (patientEmail, nhsNumber))
            connection.commit()
            print("Successfully changed email address")
            summary(nhsNumber)
            options(nhsNumber)
    except EmailAlreadyExistsError:
        error = EmailAlreadyExistsError()
        print(error)
        update_patient_email(nhsNumber)

def update_password_check(nhsNumber):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = c.fetchall()
        password = input("In order to change your password, please enter your old password (press 0 to go back): ")
        if password == '':
            raise EmptyAnswerError()
        elif password == '0':
            update_options(nhsNumber)
        else:
            if password != nhsNumbers[0][10]:
                raise PasswordIncorrectError()
            else:
                update_password(nhsNumber)
    except PasswordIncorrectError:
        error = PasswordIncorrectError()
        print(error)
        update_password_check(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_password_check(nhsNumber)

def update_password(nhsNumber):
    try:
        password = input("Please enter your new password (press 0 to go back to update details menu): ")
        if password == '':
            raise EmptyAnswerError()
        elif password == '0':
            update_options(nhsNumber)
        else:
            c.execute("""UPDATE PatientDetail SET password = ? WHERE nhsNumber = ?""", (password, nhsNumber))
            connection.commit()
            print("Successfully changed password")
            summary(nhsNumber)
            options(nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_password(nhsNumber)

def email_password_check(patientEmail):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        password = input("Password: ")
        if password != patientEmails[0][10]:
            raise PasswordIncorrectError()
        else:
            check_NHS(patientEmails[0][0])
    except PasswordIncorrectError:
        error = PasswordIncorrectError()
        print(error)
        email_password_check(patientEmail)


def email_check(patientEmail):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails == []:
            raise EmailDoesNotExistError
        else:
            email_password_check(patientEmail)
    except EmailDoesNotExistError:
        error = EmailDoesNotExistError()
        print(error)
        patientEmail = input("Email: ")
        email_check(patientEmail)


def email_login():
    try:
        patientEmail = input("Email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            email_check(patientEmail)
        else:
            raise InvalidEmailError()
    except InvalidEmailError:
        error = InvalidEmailError()
        print(error)
        email_login()


def NHS_password_check(nhsNumber):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = c.fetchall()
        password = input("Password: ")
        if password != nhsNumbers[0][10]:
            raise PasswordIncorrectError()
        else:
            check_NHS(nhsNumbers[0][0])
    except PasswordIncorrectError:
        error = PasswordIncorrectError()
        print(error)
        NHS_password_check(nhsNumber)


def NHS_login():
    try:
        nhsNumber = input("NHS Number: ")
        nhsNumber = int(re.sub("[^0-9]", "", nhsNumber))
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = c.fetchall()
        if nhsNumbers == []:
            raise NHSDoesNotExistError()
        else:
            NHS_password_check(nhsNumber)
    except NHSDoesNotExistError:
        error = NHSDoesNotExistError()
        print(error)
        NHS_login()


def login():
    try:
        print("********************************************")
        print("Choose [1] to login using your email")
        print("Choose [2] to login using your NHS number")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise EmptyAnswerError
        elif action == '1':
            email_login()
        elif action == '2':
            NHS_login()
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        login()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        login()

def first_name_q(newPatient):
    try:
        firstName = input("Please enter your first name (press 0 to exit registration): ")
        firstName = string.capwords(firstName.strip())
        if firstName == '':
            raise EmptyAnswerError()
        elif firstName == '0':
            task()
        x = firstName.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            newPatient["firstName"] = firstName
            last_name_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        first_name_q(newPatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        first_name_q(newPatient)

def last_name_q(newPatient):
    try:
        lastName = input("Please enter your last name (press 0 to exit registration, press 1 to go back): ")
        lastName = string.capwords(lastName.strip())
        if lastName == '':
            raise EmptyAnswerError()
        elif lastName == '0':
            task()
        elif lastName == '1':
            first_name_q(newPatient)
        x = lastName.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            newPatient["lastName"] = lastName
            date_of_birth_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        last_name_q(newPatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        last_name_q(newPatient)
    
def date_of_birth_q(newPatient):
    try:
        dateOfBirth = input('Please enter your birthday in YYYY-MM-DD format (press 0 to exit registration, press 1 to go back): ')
        if dateOfBirth == '':
            raise EmptyAnswerError()
        elif dateOfBirth == '0':
            task()
        elif dateOfBirth == '1':
            last_name_q(newPatient)
        x = dateOfBirth.replace(" ", "")
        x = x.replace("-", "")
        if (len(dateOfBirth) != 10) or (dateOfBirth[4] != '-' or dateOfBirth[7] != '-') or (x.isdigit() == False):
            raise DateFormatError()
        day = dateOfBirth[8:10]
        month = dateOfBirth[5:7]
        year = dateOfBirth[0:4]
        if (day.isdigit() == False) or (month.isdigit() == False) or (year.isdigit() == False):
            raise DateInvalidError()
        day = int(dateOfBirth[8:10])
        month = int(dateOfBirth[5:7])
        year = int(dateOfBirth[0:4])
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
            dateOfBirth = datetime.date(year, month, day)
            today = date.today()
            if dateOfBirth > today:
                raise DateInFutureError()
            else:
                dateOfBirth = uf.tounixtime(dateOfBirth)
                newPatient["dateOfBirth"] = dateOfBirth
                print(newPatient)
                gender_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        date_of_birth_q(newPatient)
    except DateFormatError:
        error = DateFormatError()
        print(error)
        date_of_birth_q(newPatient)
    except DateInvalidError:
        error = DateInvalidError()
        print(error)
        date_of_birth_q(newPatient)
    except DateInFutureError:
        error = DateInFutureError()
        print(error)
        date_of_birth_q(newPatient)

def gender_q(newPatient):
    try:
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
            newPatient["gender"] = gender
            address_line_1_q(newPatient)
        elif choice == "2":
            gender = "Male"
            newPatient["gender"] = gender
            address_line_1_q(newPatient)
        elif choice == "3":
            gender = "Non-Binary"
            newPatient["gender"] = gender
            address_line_1_q(newPatient)
        elif choice == "4":
            task()
        elif choice == "5":
            date_of_birth_q(newPatient)
        else:
            raise InvalidAnswerError()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        gender_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        gender_q(newPatient)

def address_line_1_q(newPatient):
    try:
        addressLine1 = input("Address Line 1 (press 0 to exit registration, press 1 to go back): ")
        addressLine1 = string.capwords(addressLine1.strip())
        if addressLine1 == '':
            raise EmptyAnswerError()
        elif addressLine1 == '0':
            task()
        elif addressLine1 == "1":
            gender_q(newPatient)
        elif len(addressLine1) > 100:
            raise InvalidAnswerError()
        else:
            newPatient["addressLine1"] = addressLine1
            address_line_2_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        address_line_1_q(newPatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        address_line_1_q(newPatient)

def address_line_2_q(newPatient):
    try:
        addressLine2 = input("Address Line 2 (press 0 to exit registration, press 1 to go back): ")
        addressLine2 = string.capwords(addressLine2.strip())
        if addressLine2 == '0':
            task()
        elif addressLine2 == "1":
            address_line_1_q(newPatient)
        elif len(addressLine2) > 100:
            raise InvalidAnswerError()
        else:
            newPatient["addressLine2"] = addressLine2
            city_q(newPatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        address_line_2_q(newPatient)

def city_q(newPatient):
    try:
        city = input("City (press 0 to exit registration, press 1 to go back): ")
        city = string.capwords(city.strip())
        if city == '':
            raise EmptyAnswerError()
        elif city == '0':
            task()
        elif city == "1":
            address_line_2_q(newPatient)
        elif len(city) > 100:
            raise InvalidAnswerError()
        x = city.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            addressLine2 = (newPatient["addressLine2"] + " " + city).strip()
            newPatient["addressLine2"] = addressLine2
            postcode_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        city_q(newPatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        city_q(newPatient)

def postcode_q(newPatient):
    try:
        postcode = input("Postcode (press 0 to exit registration, press 1 to go back): ")
        postcode = postcode.strip().upper()
        if postcode == '':
            raise EmptyAnswerError()
        elif postcode == '0':
            task()
        elif postcode == "1":
            city_q(newPatient)
        elif len(postcode) > 100:
            raise InvalidAnswerError()
        else:
            newPatient["postcode"] = postcode
            telephone_number_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        postcode_q(newPatient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        postcode_q(newPatient)

def telephone_number_q(newPatient):
    try:
        telephoneNumber = input("Telephone number, including country code (i.e. +447123456789)(press 0 to exit registration, press 1 to go back): ")
        if telephoneNumber == '':
            raise EmptyAnswerError()
        elif telephoneNumber == '0':
            task()
        elif telephoneNumber == "1":
            postcode_q(newPatient)
        telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
        if len(telephoneNumber) > 12 or len(telephoneNumber) < 11:
            raise InvalidTelephoneError()
        else:
            telephoneNumber = int(telephoneNumber)
            newPatient["telephoneNumber"] = telephoneNumber
            patient_email_q(newPatient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        telephone_number_q(newPatient)
    except InvalidTelephoneError:
        error = InvalidTelephone()
        print(error)
        telephone_number_q(newPatient)

def patient_email_q(newPatient):
    try:
        patientEmail = input("Email (press 0 to exit registration, press 1 to go back): ")
        if patientEmail == '':
            raise EmptyAnswerError()
        elif patientEmail == '0':
            task()
        elif patientEmail == "1":
            telephone_number_q(newPatient)
        elif re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            patient_email_q_check(newPatient, patientEmail)
        else:
            raise InvalidEmailError()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        patient_email_q(newPatient)
    except InvalidEmailError:
        error = InvalidEmailError()
        print(error)
        patient_email_q(newPatient)

def patient_email_q_check(newPatient, patientEmail):
    try:
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?",
              [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails != []:
            raise EmailAlreadyExistsError()
        else:
            newPatient["patientEmail"] = patientEmail
            password_q(newPatient)
    except EmailAlreadyExistsError:
        error = EmailAlreadyExistsError()
        print(error)
        patient_email_q(newPatient)

def password_q(newPatient):
    try:
        password = input("Password (press 0 to exit registration, press 1 to go back): ")
        if password == '':
            raise EmptyAnswerError()
        elif password == '0':
            task()
        elif password == "1":
            patient_email_q(newPatient)
        else:
            newPatient["password"] = password
            x = Patient(newPatient["patientEmail"], newPatient["firstName"], newPatient["lastName"], newPatient["dateOfBirth"], newPatient["gender"], newPatient["addressLine1"], newPatient["addressLine2"], newPatient["postcode"], newPatient["telephoneNumber"], newPatient["password"])
            x.register()
            ps.summary(x.nhsNumber)
            options(x.nhsNumber)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        password_q(newPatient)

def register():
    newPatient = {"firstName": "",
                  "lastName": "",
                  "dateOfBirth": "",
                  "gender": "",
                  "addressLine1": "",
                  "addressLine2": "",
                  "postcode": "",
                  "telephoneNumber": "",
                  "patientEmail": "",
                  "password": ""}
    first_name_q(newPatient)


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
            logout()
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

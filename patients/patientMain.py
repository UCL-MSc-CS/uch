import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.PatientRiskProfile import PatientMedical
from patients.lifeStyleQuestionnaire import RiskProfile
from patients.appointment import Appointment
import usefulfunctions as uf
import re
import patients.patientMedicalFunctions as pf

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

def summary(NHS_number):
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
    results = c.fetchall()
    date_of_birth = uf.toregulartime(results[0][4])
    date_of_birth = str(date_of_birth)[0:10]
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
    print("Date of Birth: " + str(date_of_birth))
    print("Gender: " + str(results[0][5]))
    print("Address: ")
    print(str(results[0][6]))
    print(str(results[0][7]))
    print(str(results[0][8]))
    print("Telephone Number: +" + str(results[0][9]))
    print("Password: " + hash)

def check_NHS(NHS_number):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
        results = c.fetchall()
        if results[0][11] == 0:
            raise NotRegisteredError()
    except NotRegisteredError:
        error = NotRegisteredError()
        print(error)
        exit()
    else:
        options(NHS_number)


def quest_options(NHS_number):
    try:
        print("********************************************")
        print("Choose [1] to see your medical profile")
        print("Choose [2] to take the lifestyle risk questionnaire")
        print("Choose [3] to update your medical history")
        print("Choose [0] to exit")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise EmptyAnswerError()
        elif action == '1':
            name = PatientMedical(NHS_number)
            name.show_profile(NHS_number)
            options(NHS_number)
        elif action == '2':
            print("Please fill out the following risk profile")
            x = RiskProfile(NHS_number)
            x.questions(NHS_number)
            x.BMI_calculator(NHS_number)
            x.smoking(NHS_number)
            x.drugs(NHS_number)
            x.alcohol(NHS_number)
            x.diet(NHS_number)
            x.insert_to_table(NHS_number)
            options(NHS_number)
        elif action == '3':
            x = PatientMedical(NHS_number)
            pf.medical_history_menu()
            select_medi = input('Please select an option: ')
            if select_medi == '0':
                return 0
            elif select_medi == '1':
                x.vaccination(NHS_number)
            elif select_medi == '2':
                x.cancer(NHS_number)
            elif select_medi == '3':
                x.pre_existing_con(NHS_number)
            elif select_medi == '4':
                x.med_allergy(NHS_number)
            options(NHS_number)
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        quest_options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        quest_options(NHS_number)

def logout():
    from root.py import Menus
    x = Menu()
    x.MasterMenu()

def options(NHS_number):
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
            x.bookAppointment(NHS_number)
            options(NHS_number)
        elif action == '2':
            x = Appointment()
            x.viewAppConfirmations(NHS_number)
            options(NHS_number)
        elif action == '3':
            x = Appointment()
            x.cancelAppointment(NHS_number)
            options(NHS_number)
        elif action == '4':
            quest_options(NHS_number)
        elif action == '5':
            summary(NHS_number)
            options(NHS_number)
        elif action == '6':
            summary(NHS_number)
            update_options(NHS_number)
        elif action == '0':
            logout()
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        options(NHS_number)

def update_options(NHS_number):
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
            update_first_name(NHS_number)
        elif action == '2':
            update_last_name(NHS_number)
        elif action == '3':
            update_patient = {"address_line_1": "",
                  "address_line_2": "",
                  "postcode": ""}
            update_address_line_1(NHS_number,update_patient)
        elif action == '4':
            update_telephone_number(NHS_number)
        elif action == '5':
            update_patient_email(NHS_number)
        elif action == '6':
            update_password_check(NHS_number)
        elif action == '0':
            options(NHS_number)
        else:
            raise InvalidAnswerError()
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_options(NHS_number)

def update_first_name(NHS_number):
    try:
        first_name = input("Please enter your new first name (press 0 to go back): ")
        first_name = first_name.strip().title()
        if first_name == '':
            raise EmptyAnswerError()
        elif first_name == '0':
            update_options(NHS_number)
        x = first_name.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""", (first_name, NHS_number))
            connection.commit()
            print("Successfully changed first name")
            summary(NHS_number)
            options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_first_name(NHS_number)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_first_name(NHS_number)

def update_last_name(NHS_number):
    try:
        last_name = input("Please enter your new last name (press 0 to go back): ")
        last_name = last_name.strip().title()
        if last_name == '':
            raise EmptyAnswerError()
        elif last_name == '0':
            update_options(NHS_number)
        x = last_name.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            c.execute("""UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""", (last_name, NHS_number))
            connection.commit()
            print("Successfully changed last name")
            summary(NHS_number)
            options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_last_name(NHS_number)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_last_name(NHS_number)

def update_address_line_1(NHS_number, update_patient):
    try:
        address_line_1 = input("Please enter your new address line 1 (press 0 to go back): ")
        address_line_1 = address_line_1.strip().title()
        if address_line_1 == '':
            raise EmptyAnswerError()
        elif address_line_1 == '0':
            update_options(NHS_number)
        elif len(address_line_1) > 100:
            raise InvalidAnswerError()
        else:
            update_patient["address_line_1"] = address_line_1
            update_address_line_2(NHS_number,update_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_address_line_1(NHS_number, update_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_address_line_1(NHS_number, update_patient)

def update_address_line_2(NHS_number, update_patient):
    try:
        address_line_2 = input("Please enter your new address line 2 (press 0 to go back to update details menu, press 1 to go back): ")
        address_line_2 = address_line_2.strip().title()
        if address_line_2 == '0':
            update_options(NHS_number)
        elif address_line_2 == "1":
            update_address_line_1(NHS_number, update_patient)
        elif len(address_line_2) > 100:
            raise InvalidAnswerError()
        else:
            update_patient["address_line_2"] = address_line_2
            update_city(NHS_number, update_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_address_line_2(NHS_number, update_patient)

def update_city(NHS_number, update_patient):
    try:
        city = input("Please enter your new city (press 0 to go back to update details menu, press 1 to go back): ")
        city = city.strip().title()
        if city == '':
            raise EmptyAnswerError()
        elif city == '0':
            update_options(NHS_number)
        elif city == "1":
            update_address_line_2(NHS_number, update_patient)
        elif len(city) > 100:
            raise InvalidAnswerError()
        x = city.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            address_line_2 = (update_patient["address_line_2"] + " " + city).strip()
            update_patient["address_line_2"] = address_line_2
            update_postcode(NHS_number, update_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_city(NHS_number, update_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_city(NHS_number, update_patient)

def update_postcode(NHS_number, update_patient):
    try:
        postcode = input("Please enter your new postcode (press 0 to go back to update details menu, press 1 to go back): ")
        postcode = postcode.strip().upper()
        if postcode == '':
            raise EmptyAnswerError()
        elif postcode == '0':
            update_options(NHS_number)
        elif postcode == "1":
            update_city(NHS_number, update_patient)
        elif len(postcode) > 100:
            raise InvalidAnswerError()
        else:
            update_patient["postcode"] = postcode
            c.execute("""UPDATE PatientDetail SET addressLine1 = ? WHERE nhsNumber = ?""", (update_patient["address_line_1"], NHS_number))
            connection.commit()
            c.execute("""UPDATE PatientDetail SET addressLine2 = ? WHERE nhsNumber = ?""", (update_patient["address_line_2"], NHS_number))
            connection.commit()
            c.execute("""UPDATE PatientDetail SET postcode = ? WHERE nhsNumber = ?""", (update_patient["postcode"], NHS_number))
            connection.commit()
            print("Successfully changed address")
            summary(NHS_number)
            options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_postcode(NHS_number, update_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        update_postcode(NHS_number, update_patient)

def update_telephone_number(NHS_number):
    try:
        telephone_number = input("Please enter your new telephone number, including country code (i.e. +447123456789)(press 0 to go back): ")
        if telephone_number == '':
            raise EmptyAnswerError()
        elif telephone_number == '0':
            update_options(NHS_number)
        telephone_number = re.sub("[^0-9]", "", telephone_number)
        if len(telephone_number) > 12 or len(telephone_number) < 11:
            raise InvalidTelephoneError()
        else:
            telephone_number = int(telephone_number)
            c.execute("""UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""", (telephone_number, NHS_number))
            connection.commit()
            print("Successfully changed telephone number")
            summary(NHS_number)
            options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_telephone_number(NHS_number)
    except InvalidTelephoneError:
        error = InvalidTelephoneError()
        print(error)
        update_telephone_number(NHS_number)

def update_patient_email(NHS_number):
    try:
        patient_email = input("Please enter your new email (press 0 to go back): ")
        if patient_email == '':
            raise EmptyAnswerError()
        elif patient_email == '0':
            update_options(NHS_number)
        elif re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
            update_patient_email_check(NHS_number, patient_email)
        else:
            raise InvalidEmailError()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_patient_email(NHS_number)
    except InvalidEmailError:
        error = InvalidEmailError()
        print(error)
        update_patient_email(NHS_number)

def update_patient_email_check(NHS_number, patient_email):
    try:
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",
              [patient_email])
        patient_emails = c.fetchall()
        if patient_emails != []:
            raise EmailAlreadyExistsError()
        else:
            c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""", (patient_email, NHS_number))
            connection.commit()
            print("Successfully changed email address")
            summary(NHS_number)
            options(NHS_number)
    except EmailAlreadyExistsError:
        error = EmailAlreadyExistsError()
        print(error)
        update_patient_email(NHS_number)

def update_password_check(NHS_number):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
        NHS_numbers = c.fetchall()
        password = input("In order to change your password, please enter your old password (press 0 to go back): ")
        if password == '':
            raise EmptyAnswerError()
        elif password == '0':
            update_options(NHS_number)
        else:
            if password != NHS_numbers[0][10]:
                raise PasswordIncorrectError()
            else:
                update_password(NHS_number)
    except PasswordIncorrectError:
        error = PasswordIncorrectError()
        print(error)
        update_password_check(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_password_check(NHS_number)

def update_password(NHS_number):
    try:
        password = input("Please enter your new password (press 0 to go back to update details menu): ")
        if password == '':
            raise EmptyAnswerError()
        elif password == '0':
            update_options(NHS_number)
        else:
            c.execute("""UPDATE PatientDetail SET password = ? WHERE nhsNumber = ?""", (password, NHS_number))
            connection.commit()
            print("Successfully changed password")
            summary(NHS_number)
            options(NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        update_password(NHS_number)

def email_password_check(patient_email):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail = ?", [patient_email])
        patient_emails = c.fetchall()
        password = input("Password: ")
        if password != patient_emails[0][10]:
            raise PasswordIncorrectError()
        else:
            check_NHS(patient_emails[0][0])
    except PasswordIncorrectError:
        error = PasswordIncorrectError()
        print(error)
        email_password_check(patient_email)


def email_check(patient_email):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail = ?", [patient_email])
        patient_emails = c.fetchall()
        if patient_emails == []:
            raise EmailDoesNotExistError
        else:
            email_password_check(patient_email)
    except EmailDoesNotExistError:
        error = EmailDoesNotExistError()
        print(error)
        patient_email = input("Email: ")
        email_check(patient_email)


def email_login():
    try:
        patient_email = input("Email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
            email_check(patient_email)
        else:
            raise InvalidEmailError()
    except InvalidEmailError:
        error = InvalidEmailError()
        print(error)
        email_login()


def NHS_password_check(NHS_number):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
        NHS_numbers = c.fetchall()
        password = input("Password: ")
        if password != NHS_numbers[0][10]:
            raise PasswordIncorrectError()
        else:
            check_NHS(NHS_numbers[0][0])
    except PasswordIncorrectError:
        error = PasswordIncorrectError()
        print(error)
        NHS_password_check(NHS_number)


def NHS_login():
    try:
        NHS_number = input("NHS Number: ")
        NHS_number = int(re.sub("[^0-9]", "", NHS_number))
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber = ?", [NHS_number])
        NHS_numbers = c.fetchall()
        if NHS_numbers == []:
            raise NHSDoesNotExistError()
        else:
            NHS_password_check(NHS_number)
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

def first_name_q(new_patient):
    try:
        first_name = input("Please enter your first name (press 0 to exit registration): ")
        first_name = first_name.strip().title()
        if first_name == '':
            raise EmptyAnswerError()
        elif first_name == '0':
            task()
        x = first_name.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            new_patient["first_name"] = first_name
            last_name_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        first_name_q(new_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        first_name_q(new_patient)

def last_name_q(new_patient):
    try:
        last_name = input("Please enter your last name (press 0 to exit registration, press 1 to go back): ")
        last_name = last_name.strip().title()
        if last_name == '':
            raise EmptyAnswerError()
        elif last_name == '0':
            task()
        elif last_name == '1':
            first_name_q(new_patient)
        x = last_name.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            new_patient["last_name"] = last_name
            date_of_birth_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        last_name_q(new_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        last_name_q(new_patient)
    
def date_of_birth_q(new_patient):
    try:
        date_of_birth = input('Please enter your birthday in YYYY-MM-DD format (press 0 to exit registration, press 1 to go back): ')
        if date_of_birth == '':
            raise EmptyAnswerError()
        elif date_of_birth == '0':
            task()
        elif date_of_birth == '1':
            last_name_q(new_patient)
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
                date_of_birth = uf.tounixtime(date_of_birth)
                new_patient["date_of_birth"] = date_of_birth
                gender_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        date_of_birth_q(new_patient)
    except DateFormatError:
        error = DateFormatError()
        print(error)
        date_of_birth_q(new_patient)
    except DateInvalidError:
        error = DateInvalidError()
        print(error)
        date_of_birth_q(new_patient)
    except DateInFutureError:
        error = DateInFutureError()
        print(error)
        date_of_birth_q(new_patient)

def gender_q(new_patient):
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
            new_patient["gender"] = gender
            address_line_1_q(new_patient)
        elif choice == "2":
            gender = "Male"
            new_patient["gender"] = gender
            address_line_1_q(new_patient)
        elif choice == "3":
            gender = "Non-Binary"
            new_patient["gender"] = gender
            address_line_1_q(new_patient)
        elif choice == "4":
            task()
        elif choice == "5":
            date_of_birth_q(new_patient)
        else:
            raise InvalidAnswerError()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        gender_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        gender_q(new_patient)

def address_line_1_q(new_patient):
    try:
        address_line_1 = input("Address Line 1 (press 0 to exit registration, press 1 to go back): ")
        address_line_1 = address_line_1.strip().title()
        if address_line_1 == '':
            raise EmptyAnswerError()
        elif address_line_1 == '0':
            task()
        elif address_line_1 == "1":
            gender_q(new_patient)
        elif len(address_line_1) > 100:
            raise InvalidAnswerError()
        else:
            new_patient["address_line_1"] = address_line_1
            address_line_2_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        address_line_1_q(new_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        address_line_1_q(new_patient)

def address_line_2_q(new_patient):
    try:
        address_line_2 = input("Address Line 2 (press 0 to exit registration, press 1 to go back): ")
        address_line_2 = address_line_2.strip().title()
        if address_line_2 == '0':
            task()
        elif address_line_2 == "1":
            address_line_1_q(new_patient)
        elif len(address_line_2) > 100:
            raise InvalidAnswerError()
        else:
            new_patient["address_line_2"] = address_line_2
            city_q(new_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        address_line_2_q(new_patient)

def city_q(new_patient):
    try:
        city = input("City (press 0 to exit registration, press 1 to go back): ")
        city = city.strip().title()
        if city == '':
            raise EmptyAnswerError()
        elif city == '0':
            task()
        elif city == "1":
            address_line_2_q(new_patient)
        elif len(city) > 100:
            raise InvalidAnswerError()
        x = city.replace(" ", "")
        if x.isalpha() == False:
            raise InvalidAnswerError()
        else:
            address_line_2 = (new_patient["address_line_2"] + " " + city).strip()
            new_patient["address_line_2"] = address_line_2
            postcode_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        city_q(new_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        city_q(new_patient)

def postcode_q(new_patient):
    try:
        postcode = input("Postcode (press 0 to exit registration, press 1 to go back): ")
        postcode = postcode.strip().upper()
        if postcode == '':
            raise EmptyAnswerError()
        elif postcode == '0':
            task()
        elif postcode == "1":
            city_q(new_patient)
        elif len(postcode) > 100:
            raise InvalidAnswerError()
        else:
            new_patient["postcode"] = postcode
            telephone_number_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        postcode_q(new_patient)
    except InvalidAnswerError:
        error = InvalidAnswerError()
        print(error)
        postcode_q(new_patient)

def telephone_number_q(new_patient):
    try:
        telephone_number = input("Telephone number, including country code (i.e. +447123456789)(press 0 to exit registration, press 1 to go back): ")
        if telephone_number == '':
            raise EmptyAnswerError()
        elif telephone_number == '0':
            task()
        elif telephone_number == "1":
            postcode_q(new_patient)
        telephone_number = re.sub("[^0-9]", "", telephone_number)
        if len(telephone_number) > 12 or len(telephone_number) < 11:
            raise InvalidTelephoneError()
        else:
            telephone_number = int(telephone_number)
            new_patient["telephone_number"] = telephone_number
            patient_email_q(new_patient)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        telephone_number_q(new_patient)
    except InvalidTelephoneError:
        error = InvalidTelephone()
        print(error)
        telephone_number_q(new_patient)

def patient_email_q(new_patient):
    try:
        patient_email = input("Email (press 0 to exit registration, press 1 to go back): ")
        if patient_email == '':
            raise EmptyAnswerError()
        elif patient_email == '0':
            task()
        elif patient_email == "1":
            telephone_number_q(new_patient)
        elif re.match(r"[^@]+@[^@]+\.[^@]+", patient_email):
            patient_email_q_check(new_patient, patient_email)
        else:
            raise InvalidEmailError()
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        patient_email_q(new_patient)
    except InvalidEmailError:
        error = InvalidEmailError()
        print(error)
        patient_email_q(new_patient)

def patient_email_q_check(new_patient, patient_email):
    try:
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?",
              [patient_email])
        patient_emails = c.fetchall()
        if patient_emails != []:
            raise EmailAlreadyExistsError()
        else:
            new_patient["patient_email"] = patient_email
            password_q(new_patient)
    except EmailAlreadyExistsError:
        error = EmailAlreadyExistsError()
        print(error)
        patient_email_q(new_patient)

def password_q(new_patient):
    try:
        password = input("Password (press 0 to exit registration, press 1 to go back): ")
        if password == '':
            raise EmptyAnswerError()
        elif password == '0':
            task()
        elif password == "1":
            patient_email_q(new_patient)
        else:
            new_patient["password"] = password
            x = Patient(new_patient["patient_email"], new_patient["first_name"], new_patient["last_name"], new_patient["date_of_birth"], new_patient["gender"], new_patient["address_line_1"], new_patient["address_line_2"], new_patient["postcode"], new_patient["telephone_number"], new_patient["password"])
            x.register()
            summary(x.NHS_number)
            check_NHS(x.NHS_number)
    except EmptyAnswerError:
        error = EmptyAnswerError()
        print(error)
        password_q(new_patient)

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
    first_name_q(new_patient)


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
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


class notRegistered(Error):
    def __init__(self, message="A GP needs to confirm your registration before you can access our services - please try logging in tomorrow"):
        self.message = message
        super().__init__(self.message)


class emptyAnswer(Error):
    def __init__(self, message="I'm sorry, this field cannot be left empty, please try again"):
        self.message = message
        super().__init__(self.message)


class invalidAnswer(Error):
    def __init__(self, message="I'm sorry, this is not a valid answer, please try again"):
        self.message = message
        super().__init__(self.message)


class invalidEmail(Error):
    def __init__(self, message="I'm sorry, that is not a valid email, please try again"):
        self.message = message
        super().__init__(self.message)


class emailDoesNotExist(Error):
    def __init__(self, message="I'm sorry, that email is not in our system, please try again"):
        self.message = message
        super().__init__(self.message)


class emailAlreadyExists(Error):
    def __init__(self, message="I'm sorry, that email is already in use, please try again"):
        self.message = message
        super().__init__(self.message)


class passwordIncorrect(Error):
    def __init__(self, message="I'm sorry, that password is not correct, please try again"):
        self.message = message
        super().__init__(self.message)


class nhsDoesNotExist(Error):
    def __init__(self, message="I'm sorry, that NHS number is not in our system, please try again"):
        self.message = message
        super().__init__(self.message)


class invalidTelephone(Error):
    def __init__(self, message="I'm sorry, that is not a valid telephone, please try again"):
        self.message = message
        super().__init__(self.message)

class dateInvalidError(Error):
    def __init__(self, message = "I'm sorry, that is not a valid date, please try again"):
        self.message = message
        super().__init__(self.message)

class dateInFutureError(Error):
    def __init__(self, message = "I'm sorry, your date of birth cannot be in the future, please try again"):
        self.message = message
        super().__init__(self.message)

class dateFormatError(Error):
    def __init__(self, message = "I'm sorry, this date in not in the proper YYYY-MM-DD format, with '-'s as separators, please try again"):
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

def checkNHS(nhsNumber):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        results = c.fetchall()
        uf.banner('Patient')
        if results[0][11] == 0:
            raise notRegistered()
    except notRegistered:
        error = notRegistered()
        print(error)
        exit()
    else:
        options(nhsNumber)


def questOptions(nhsNumber):
    try:
        print("********************************************")
        print("Choose [1] to see your medical profile")
        print("Choose [2] to take the lifestyle risk questionnaire")
        print("Choose [3] to update your medical history")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise emptyAnswer()
        elif action == '1':
            name = PatientMedical(nhsNumber)
            name.show_profile(nhsNumber)
            options(nhsNumber)
        elif action == '2':
            print("Please fill out the following risk profile")
            x = RiskProfile(nhsNumber)
            x.questions(nhsNumber)
            x.BMI_calculator(nhsNumber)
            x.diet(nhsNumber)
            x.smoking(nhsNumber)
            x.drugs(nhsNumber)
            x.alcohol(nhsNumber)
            x.insert_to_table(nhsNumber)
            options(nhsNumber)
        elif action == '3':
            x = PatientMedical(nhsNumber)
            x.vaccination(nhsNumber)
            x.cancer(nhsNumber)
            options(nhsNumber)
        else:
            raise invalidAnswer()
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        questOptions(nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        questOptions(nhsNumber)


def options(nhsNumber):
    try:
        print("********************************************")
        print("What would you like to do next?")
        print("Choose [1] to book an appointment")
        print("Choose [2] to view your confirmed appointments")
        print("Choose [3] to cancel an appointment")
        print("Choose [4] to see your medical profile")
        print("Choose [5] to see your contact details")
        print("Choose [6] to update your contact details")
        print("Choose [0] to log out")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise emptyAnswer()
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
            questOptions(nhsNumber)
        elif action == '5':
            summary(nhsNumber)
            options(nhsNumber)
        elif action == '6':
            summary(nhsNumber)
            updateOptions(nhsNumber)
        elif action == '0':
            task()
            return 0
        else:
            raise invalidAnswer()
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        options(nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        options(nhsNumber)

def updateOptions(nhsNumber):
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
            raise emptyAnswer()
        elif action == '1':
            updateFirstName(nhsNumber)
        elif action == '2':
            updateLastName(nhsNumber)
        elif action == '3':
            updatePatient = {"addressLine1": "",
                  "addressLine2": "",
                  "postcode": ""}
            updateAddressLine1(nhsNumber,updatePatient)
        elif action == '4':
            updateTelephoneNumber(nhsNumber)
        elif action == '5':
            updatePatientEmail(nhsNumber)
        elif action == '6':
            pass
        elif action == '0':
            options(nhsNumber)
        else:
            raise invalidAnswer()
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updateOptions(nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updateOptions(nhsNumber)

def updateFirstName(nhsNumber):
    try:
        firstName = input("Please enter your new first name (press 0 to go back): ")
        firstName = string.capwords(firstName.strip())
        if firstName == '':
            raise emptyAnswer()
        elif firstName == '0':
            updateOptions(nhsNumber)
        x = firstName.replace(" ", "")
        if x.isalpha() == False:
            raise invalidAnswer()
        else:
            c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""", (firstName, nhsNumber))
            connection.commit()
            print("Successfully changed first name")
            summary(nhsNumber)
            options(nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updateFirstName(nhsNumber)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updateFirstName(nhsNumber)

def updateLastName(nhsNumber):
    try:
        lastName = input("Please enter your new last name (press 0 to go back): ")
        lastName = string.capwords(lastName.strip())
        if lastName == '':
            raise emptyAnswer()
        elif lastName == '0':
            updateOptions(nhsNumber)
        x = lastName.replace(" ", "")
        if x.isalpha() == False:
            raise invalidAnswer()
        else:
            c.execute("""UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""", (lastName, nhsNumber))
            connection.commit()
            print("Successfully changed last name")
            summary(nhsNumber)
            options(nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updateLastName(nhsNumber)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updateLastName(nhsNumber)

def updateAddressLine1(nhsNumber, updatePatient):
    try:
        addressLine1 = input("Please enter your new address line 1 (press 0 to go back): ")
        addressLine1 = string.capwords(addressLine1.strip())
        if addressLine1 == '':
            raise emptyAnswer()
        elif addressLine1 == '0':
            updateOptions(nhsNumber)
        elif len(addressLine1) > 100:
            raise invalidAnswer()
        else:
            updatePatient["addressLine1"] = addressLine1
            updateAddressLine2(nhsNumber,updatePatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updateAddressLine1(nhsNumber, updatePatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updateAddressLine1(nhsNumber, updatePatient)

def updateAddressLine2(nhsNumber, updatePatient):
    try:
        addressLine2 = input("Please enter your new address line 2 (press 0 to go back to update details menu, press 1 to go back): ")
        addressLine2 = string.capwords(addressLine2.strip())
        if addressLine2 == '0':
            updateOptions(nhsNumber)
        elif addressLine2 == "1":
            updateAddressLine1(nhsNumber, updatePatient)
        elif len(addressLine2) > 100:
            raise invalidAnswer()
        else:
            updatePatient["addressLine2"] = addressLine2
            updateCity(nhsNumber, updatePatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updateAddressLine2(nhsNumber, updatePatient)

def updateCity(nhsNumber, updatePatient):
    try:
        city = input("Please enter your new city (press 0 to go back to update details menu, press 1 to go back): ")
        city = string.capwords(city.strip())
        if city == '':
            raise emptyAnswer()
        elif city == '0':
            updateOptions(nhsNumber)
        elif city == "1":
            updateAddressLine2(nhsNumber, updatePatient)
        elif len(city) > 100:
            raise invalidAnswer()
        x = city.replace(" ", "")
        if x.isalpha() == False:
            raise invalidAnswer()
        else:
            addressLine2 = (updatePatient["addressLine2"] + " " + city).strip()
            updatePatient["addressLine2"] = addressLine2
            updatePostcode(nhsNumber, updatePatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updateCity(nhsNumber, updatePatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updateCity(nhsNumber, updatePatient)

def updatePostcode(nhsNumber, updatePatient):
    try:
        postcode = input("Please enter your new postcode (press 0 to go back to update details menu, press 1 to go back): ")
        postcode = postcode.strip().upper()
        if postcode == '':
            raise emptyAnswer()
        elif postcode == '0':
            updateOptions(nhsNumber)
        elif postcode == "1":
            updateCity(nhsNumber, updatePatient)
        elif len(postcode) > 100:
            raise invalidAnswer()
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
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updatePostcode(nhsNumber, updatePatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        updatePostcode(nhsNumber, updatePatient)

def updateTelephoneNumber(nhsNumber):
    try:
        telephoneNumber = input("Please enter your new telephone number, including country code (i.e. +447123456789)(press 0 to go back): ")
        if telephoneNumber == '':
            raise emptyAnswer()
        elif telephoneNumber == '0':
            updateOptions(nhsNumber)
        telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
        if len(telephoneNumber) > 12 or len(telephoneNumber) < 11:
            raise invalidTelephone()
        else:
            telephoneNumber = int(telephoneNumber)
            c.execute("""UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""", (telephoneNumber, nhsNumber))
            connection.commit()
            print("Successfully changed telephone number")
            summary(nhsNumber)
            options(nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updateTelephoneNumber(nhsNumber)
    except invalidTelephone:
        error = invalidTelephone()
        print(error)
        updateTelephoneNumber(nhsNumber)

def updatePatientEmail(nhsNumber):
    try:
        patientEmail = input("Please enter your new email (press 0 to go back): ")
        if patientEmail == '':
            raise emptyAnswer()
        elif patientEmail == '0':
            updateOptions(nhsNumber)
        elif re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            updatePatientEmailCheck(nhsNumber, patientEmail)
        else:
            raise invalidEmail()
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        updatePatientEmail(nhsNumber)
    except invalidEmail:
        error = invalidEmail()
        print(error)
        updatePatientEmail(nhsNumber)

def updatePatientEmailCheck(nhsNumber, patientEmail):
    try:
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?",
              [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails != []:
            raise emailAlreadyExists()
        else:
            c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""", (patientEmail, nhsNumber))
            connection.commit()
            print("Successfully changed email address")
            summary(nhsNumber)
            options(nhsNumber)
    except emailAlreadyExists:
        error = emailAlreadyExists()
        print(error)
        updatePatientEmail(nhsNumber)


def emailPasswordCheck(patientEmail):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        password = input("Password: ")
        if password != patientEmails[0][10]:
            raise passwordIncorrect()
        else:
            checkNHS(patientEmails[0][0])
    except passwordIncorrect:
        error = passwordIncorrect()
        print(error)
        emailPasswordCheck(patientEmail)


def emailCheck(patientEmail):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails == []:
            raise emailDoesNotExist
        else:
            emailPasswordCheck(patientEmail)
    except emailDoesNotExist:
        error = emailDoesNotExist()
        print(error)
        patientEmail = input("Email: ")
        emailCheck(patientEmail)


def emailLogin():
    try:
        patientEmail = input("Email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            emailCheck(patientEmail)
        else:
            raise invalidEmail()
    except invalidEmail:
        error = invalidEmail()
        print(error)
        emailLogin()


def nhsPasswordCheck(nhsNumber):
    try:
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = c.fetchall()
        password = input("Password: ")
        if password != nhsNumbers[0][10]:
            raise passwordIncorrect()
        else:
            checkNHS(nhsNumbers[0][0])
    except passwordIncorrect:
        error = passwordIncorrect()
        print(error)
        nhsPasswordCheck(nhsNumber)


def nhsLogin():
    try:
        nhsNumber = input("NHS Number: ")
        nhsNumber = int(re.sub("[^0-9]", "", nhsNumber))
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = c.fetchall()
        if nhsNumbers == []:
            raise nhsDoesNotExist()
        else:
            nhsPasswordCheck(nhsNumber)
    except nhsDoesNotExist:
        error = nhsDoesNotExist()
        print(error)
        nhsLogin()


def login():
    try:
        print("********************************************")
        print("Choose [1] to login using your email")
        print("Choose [2] to login using your NHS number")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise emptyAnswer
        elif action == '1':
            emailLogin()
        elif action == '2':
            nhsLogin()
        else:
            raise invalidAnswer()
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        login()
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        login()

def firstNameQ(newPatient):
    try:
        firstName = input("Please enter your first name (press 0 to exit registration): ")
        firstName = string.capwords(firstName.strip())
        if firstName == '':
            raise emptyAnswer()
        elif firstName == '0':
            task()
        x = firstName.replace(" ", "")
        if x.isalpha() == False:
            raise invalidAnswer()
        else:
            newPatient["firstName"] = firstName
            lastNameQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        firstNameQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        firstNameQ(newPatient)

def lastNameQ(newPatient):
    try:
        lastName = input("Please enter your last name (press 0 to exit registration, press 1 to go back): ")
        lastName = string.capwords(lastName.strip())
        if lastName == '':
            raise emptyAnswer()
        elif lastName == '0':
            task()
        elif lastName == '1':
            firstNameQ(newPatient)
        x = lastName.replace(" ", "")
        if x.isalpha() == False:
            raise invalidAnswer()
        else:
            newPatient["lastName"] = lastName
            dateOfBirthQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        lastNameQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        lastNameQ(newPatient)
    
def dateOfBirthQ(newPatient):
    try:
        dateOfBirth = input('Please enter your birthday in YYYY-MM-DD format (press 0 to exit registration, press 1 to go back): ')
        if dateOfBirth == '':
            raise emptyAnswer()
        elif dateOfBirth == '0':
            task()
        elif dateOfBirth == '1':
            lastNameQ(newPatient)
        x = dateOfBirth.replace(" ", "")
        x = x.replace("-", "")
        if (len(dateOfBirth) != 10) or (dateOfBirth[4] != '-' or dateOfBirth[7] != '-') or (x.isdigit() == False):
            raise dateFormatError()
        day = dateOfBirth[8:10]
        month = dateOfBirth[5:7]
        year = dateOfBirth[0:4]
        if (day.isdigit() == False) or (month.isdigit() == False) or (year.isdigit() == False):
            raise dateInvalidError()
        day = int(dateOfBirth[8:10])
        month = int(dateOfBirth[5:7])
        year = int(dateOfBirth[0:4])
        if month > 12 or month < 1:
            raise dateInvalidError()
        elif (month == 9 or month == 4 or month == 6 or month == 11) and day > 30:
            raise dateInvalidError()
        elif month == 2 and year % 4 != 0 and day > 28:
            raise dateInvalidError()
        elif month == 2 and year % 4 == 0 and day > 29:
            raise dateInvalidError()
        elif day > 31 or day < 1:
                raise dateInvalidError()
        else:
            dateOfBirth = datetime.date(year, month, day)
            today = date.today()
            if dateOfBirth > today:
                raise dateInFutureError()
            else:
                dateOfBirth = uf.tounixtime(dateOfBirth)
                newPatient["dateOfBirth"] = dateOfBirth
                print(newPatient)
                genderQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        dateOfBirthQ(newPatient)
    except dateFormatError:
        error = dateFormatError()
        print(error)
        dateOfBirthQ(newPatient)
    except dateInvalidError:
        error = dateInvalidError()
        print(error)
        dateOfBirthQ(newPatient)
    except dateInFutureError:
        error = dateInFutureError()
        print(error)
        dateOfBirthQ(newPatient)

def genderQ(newPatient):
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
            raise emptyAnswer()
        elif choice == '1':
            gender = "Female"
            newPatient["gender"] = gender
            addressLine1Q(newPatient)
        elif choice == "2":
            gender = "Male"
            newPatient["gender"] = gender
            addressLine1Q(newPatient)
        elif choice == "3":
            gender = "Non-Binary"
            newPatient["gender"] = gender
            addressLine1Q(newPatient)
        elif choice == "4":
            task()
        elif choice == "5":
            dateOfBirthQ(newPatient)
        else:
            raise invalidAnswer()
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        genderQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        genderQ(newPatient)

def addressLine1Q(newPatient):
    try:
        addressLine1 = input("Address Line 1 (press 0 to exit registration, press 1 to go back): ")
        addressLine1 = string.capwords(addressLine1.strip())
        if addressLine1 == '':
            raise emptyAnswer()
        elif addressLine1 == '0':
            task()
        elif addressLine1 == "1":
            genderQ(newPatient)
        elif len(addressLine1) > 100:
            raise invalidAnswer()
        else:
            newPatient["addressLine1"] = addressLine1
            addressLine2Q(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        addressLine1Q(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        addressLine1Q(newPatient)

def addressLine2Q(newPatient):
    try:
        addressLine2 = input("Address Line 2 (press 0 to exit registration, press 1 to go back): ")
        addressLine2 = string.capwords(addressLine2.strip())
        if addressLine2 == '0':
            task()
        elif addressLine2 == "1":
            addressLine1Q(newPatient)
        elif len(addressLine2) > 100:
            raise invalidAnswer()
        else:
            newPatient["addressLine2"] = addressLine2
            cityQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        addressLine2Q(newPatient)

def cityQ(newPatient):
    try:
        city = input("City (press 0 to exit registration, press 1 to go back): ")
        city = string.capwords(city.strip())
        if city == '':
            raise emptyAnswer()
        elif city == '0':
            task()
        elif city == "1":
            addressLine2Q(newPatient)
        elif len(city) > 100:
            raise invalidAnswer()
        x = city.replace(" ", "")
        if x.isalpha() == False:
            raise invalidAnswer()
        else:
            addressLine2 = (newPatient["addressLine2"] + " " + city).strip()
            newPatient["addressLine2"] = addressLine2
            postcodeQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        cityQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        cityQ(newPatient)

def postcodeQ(newPatient):
    try:
        postcode = input("Postcode (press 0 to exit registration, press 1 to go back): ")
        postcode = postcode.strip().upper()
        if postcode == '':
            raise emptyAnswer()
        elif postcode == '0':
            task()
        elif postcode == "1":
            cityQ(newPatient)
        elif len(postcode) > 100:
            raise invalidAnswer()
        else:
            newPatient["postcode"] = postcode
            telephoneNumberQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        postcodeQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        postcodeQ(newPatient)

def telephoneNumberQ(newPatient):
    try:
        telephoneNumber = input("Telephone number, including country code (i.e. +447123456789)(press 0 to exit registration, press 1 to go back): ")
        if telephoneNumber == '':
            raise emptyAnswer()
        elif telephoneNumber == '0':
            task()
        elif telephoneNumber == "1":
            postcodeQ(newPatient)
        telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
        if len(telephoneNumber) > 12 or len(telephoneNumber) < 11:
            raise invalidTelephone()
        else:
            telephoneNumber = int(telephoneNumber)
            newPatient["telephoneNumber"] = telephoneNumber
            patientEmailQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        telephoneNumberQ(newPatient)
    except invalidTelephone:
        error = invalidTelephone()
        print(error)
        telephoneNumberQ(newPatient)

def patientEmailQ(newPatient):
    try:
        patientEmail = input("Email (press 0 to exit registration, press 1 to go back): ")
        if patientEmail == '':
            raise emptyAnswer()
        elif patientEmail == '0':
            task()
        elif patientEmail == "1":
            telephoneNumberQ(newPatient)
        elif re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            patientEmailQCheck(newPatient, patientEmail)
        else:
            raise invalidEmail()
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        patientEmailQ(newPatient)
    except invalidEmail:
        error = invalidEmail()
        print(error)
        patientEmailQ(newPatient)

def patientEmailQCheck(newPatient, patientEmail):
    try:
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?",
              [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails != []:
            raise emailAlreadyExists()
        else:
            newPatient["patientEmail"] = patientEmail
            passwordQ(newPatient)
    except emailAlreadyExists:
        error = emailAlreadyExists()
        print(error)
        patientEmailQ(newPatient)

def passwordQ(newPatient):
    try:
        password = input("Password (press 0 to exit registration, press 1 to go back): ")
        if password == '':
            raise emptyAnswer()
        elif password == '0':
            task()
        elif password == "1":
            patientEmailQ(newPatient)
        else:
            newPatient["password"] = password
            x = Patient(newPatient["patientEmail"], newPatient["firstName"], newPatient["lastName"], newPatient["dateOfBirth"], newPatient["gender"], newPatient["addressLine1"], newPatient["addressLine2"], newPatient["postcode"], newPatient["telephoneNumber"], newPatient["password"])
            x.register()
            ps.summary(x.nhsNumber)
            options(x.nhsNumber)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        passwordQ(newPatient)

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
    firstNameQ(newPatient)


# Main Patient Function
def task():
    try:
        print("********************************************")
        print("Choose [1] to register for a new account")
        print("Choose [2] to login")
        print("Choose [0] to exit")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise emptyAnswer()
        elif action == '1':
            register()
        elif action == '2':
            login()
        elif action == '0':
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()
        else:
            raise invalidAnswer()
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        task()
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        task()

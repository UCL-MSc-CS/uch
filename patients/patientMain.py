import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.PatientRiskProfile import PatientMedical
from patients.lifeStyleQuestionnaire import RiskProfile
from patients.appointment import Appointment
import patients.patientSummary as ps
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

# Patient Functions


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
            ps.summary(nhsNumber)
            options(nhsNumber)
        elif action == '6':
            options(nhsNumber)
        elif action == '0':
            print("Thank you for using the UCH e-health system! Goodbye for now!")
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
        if firstName == '0':
            task()
        elif firstName == "1":
            raise invalidAnswer()
        else:
            newPatient["firstName"] = firstName
            lastNameQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        firstNameQ(newPatient)

def lastNameQ(newPatient):
    try:
        lastName = input("Please enter your last name (press 0 to exit registration, press 1 to go back): ")
        lastName = string.capwords(lastName.strip())
        if lastName == '0':
            task()
        elif lastName == '1':
            firstNameQ(newPatient)
        elif lastName == "2":
            raise invalidAnswer()
        else:
            newPatient["lastName"] = lastName
            dateOfBirthQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        lastNameQ(newPatient)
    
def dateOfBirthQ(newPatient):
    try:
        dateOfBirth = input('Please enter your birthday in YYYY-MM-DD format (press 0 to exit registration, press 1 to go back): ')
        if dateOfBirth == '0':
            task()
        elif dateOfBirth == '1':
            lastNameQ(newPatient)
        elif dateOfBirth == "2":
            raise invalidAnswer()
        else:
            year, month, day = map(int, dateOfBirth.split('-'))
            dateOfBirth = str(datetime.date(year, month, day))
            newPatient["dateOfBirth"] = dateOfBirth
            genderQ(newPatient)
    except invalidAnswer:
        error = invalidAnswer()
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
            print(newPatient)
        elif choice == "2":
            gender = "Male"
            newPatient["gender"] = gender
            print(newPatient)
        elif choice == "3":
            gender = "Non-Binary"
            newPatient["gender"] = gender
            print(newPatient)
        elif choice == "4":
            task()
        elif choice == "5":
            dateOfBirthQ(newPatient)
        else:
            raise invalidAnswer()
    except invalidAnswer:
        error = invalidAnswer()
        print(error)
        genderQ(newPatient)
    except emptyAnswer:
        error = emptyAnswer()
        print(error)
        genderQ(newPatient)

def register():
    newPatient = {"firstName": "",
                  "lastName": "",
                  "dateOfBirth": "",
                  "gender": "",
                  "addressLine1": "",
                  "addressLine2": "",
                  "postcode": "",
                  "telephoneNumber": 0,
                  "patientEmail": "",
                  "password": ""}
    firstNameQ(newPatient)


# Main Patient Function
def task():
    try:
        print("********************************************")
        print("Choose [1] to register for a new account")
        print("Choose [2] to login")
        print("********************************************")
        action = input("Please select an option: ")
        if action == '':
            raise emptyAnswer()
        elif action == '1':
            register()
        elif action == '2':
            login()
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

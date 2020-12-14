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
        print("Choose [0] to exit")
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
            print("********************************************")
            print("Choose [1] to see your medical profile")
            print("Choose [2] to take the lifestyle risk questionnaire")
            print("Choose [3] to update your medical history")
            print("********************************************")
            qchoice = input("Please select an option: ")
            if qaction == '1':
                name = PatientMedical()
                name.show_profile(nhsNumber)
                options(nhsNumber)
            elif qaction == '2':
                print("Please fill out the following risk profile")
                x = RiskProfile()  # need to pass patientEmail into the functions
                x.questions()
                x.BMI_calculator()
                x.diet()
                x.smoking()
                x.drugs()
                x.alcohol()
                x.insert_to_table(nhsNumber)
                options(nhsNumber)
            elif qaction == '3':
                x = PatientMedical()
                x.vaccination(nhsNumber)
                x.cancer(nhsNumber)
                options(nhsNumber)
        elif action == '5':
            ps.summary(nhsNumber)
            options(nhsNumber)
        elif action == '6':
            options(nhsNumber)
        elif action == '0':
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()
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


def login():
    print("********************************************")
    print("Choose [1] to login using your email")
    print("Choose [2] to login using your NHS number")
    print("********************************************")
    action = input("Please select an option: ")
    if action == '1':
        patientEmail = input("Email: ")
        goodEmail = True
        if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            goodEmail = True
        else:
            goodEmail = False
        while goodEmail == False:
            print("I'm sorry, that is not a valid email")
            patientEmail = input("Email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
                goodEmail = True
            else:
                goodEmail = False
        c.execute(
            "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails == []:
            while patientEmails == []:
                print("I'm sorry, that email is not in our system")
                patientEmail = input("Email: ")
                c.execute(
                "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
                patientEmails = c.fetchall()
        password = input("Password: ")
        if password != patientEmails[0][10]:
            while password != patientEmails[0][10]:
                print("I'm sorry, that password is not correct")
                password = input("Password: ")
            checkNHS(patientEmails[0][0])
        else:
            checkNHS(patientEmails[0][0])
    elif action == '2':
        nhsNumber = input("NHS Number: ")
        nhsNumber = int(re.sub("[^0-9]", "", nhsNumber))
        c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = c.fetchall()
        if nhsNumbers == []:
            while nhsNumbers == []:
                print("I'm sorry, that NHS number is not in our system")
                nhsNumber = input("NHS Number: ")
                c.execute(
                "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
                nhsNumbers = c.fetchall()
        password = input("Password: ")
        if password != nhsNumbers[0][10]:
            while password != nhsNumbers[0][10]:
                print("I'm sorry, that password is not correct")
                password = input("Password: ")
            checkNHS(nhsNumbers[0][0])
        else:
            checkNHS(nhsNumbers[0][0])


def register():
    # First Name
    firstName = input("Please enter your first name: ")
    firstName = string.capwords(firstName.strip())
    # print(firstName)
    # Last Name
    lastName = input("Please enter your last name: ")
    lastName = string.capwords(lastName.strip())
    # print(lastName)
    # Date of Birth
    dateOfBirth = input('Please enter your birthday in YYYY-MM-DD format: ')
    year, month, day = map(int, dateOfBirth.split('-'))
    dateOfBirth = datetime.date(year, month, day)
    # print(dateOfBirth)
    # Gender
    print("********************************************")
    print("Choose [1] for female")
    print("Choose [2] for male")
    print("Choose [3] for non-binary")
    print("********************************************")
    gender = input("Please select an option: ")
    while gender != '1' and gender != '2' and gender != '3':
        print("I'm sorry, '" + gender + "' is an invalid option")
        print("********************************************")
        print("Choose [1] for female")
        print("Choose [2] for male")
        print("Choose [3] for non-binary")
        print("********************************************")
        gender = input("Please select an option: ")
    if gender == '1':
        gender = "Female"
    elif gender == '2':
        gender = "Male"
    elif gender == '3':
        gender = "Non-Binary"
    # print(gender)
    # Address Line 1
    addressLine1 = input("Address Line 1: ")
    addressLine1 = string.capwords(addressLine1.strip())
    # print(addressLine1)
    # Address Line 2
    addressLine2 = input("Address Line 2: ")
    addressLine2 = string.capwords(addressLine2.strip())
    # print(addressLine2)
    # City
    city = input("City: ")
    city = string.capwords(city.strip())
    addressLine2 = (addressLine2 + " " + city).strip()
    # print(addressLine2)
    # Postcode
    postcode = input("Postcode: ")
    postcode = postcode.strip().upper()
    # print(postcode)
    # Telephone Number
    telephoneNumber = input(
        "Telephone number, including country code (i.e. +447123456789): ")
    telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
    while len(telephoneNumber) > 12 or len(telephoneNumber) < 11:
        print("I'm sorry, that is not a valid telephone")
        telephoneNumber = input(
            "Telephone number, including country code (i.e. +447123456789): ")
        telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
    telephoneNumber = int(telephoneNumber)
    # print(telephoneNumber)
    # Email
    patientEmail = input("Email: ")
    goodEmail = True
    if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
        goodEmail = True
    else:
        goodEmail = False
    while goodEmail == False:
        print("I'm sorry, that is not a valid email")
        patientEmail = input("Email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            goodEmail = True
        else:
            goodEmail = False
    c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?",
              [patientEmail])
    patientEmails = c.fetchall()
    if patientEmails != []:
        while patientEmails != []:
            print("I'm sorry, that email is already in use")
            patientEmail = input("Email: ")
            c.execute(
                "SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
            patientEmails = c.fetchall()
    # Password
    password = input("Password: ")
    x = Patient(patientEmail, firstName, lastName, dateOfBirth, gender,
                addressLine1, addressLine2, postcode, telephoneNumber, password)
    x.register()
    ps.summary(x.nhsNumber)
    options(x.nhsNumber)


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

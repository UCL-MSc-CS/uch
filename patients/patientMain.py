import sqlite3 as sql
from getpass import getpass
import datetime
from datetime import date
from patient import Patient
from PatientRiskProfile import PatientMedical
from lifeStyleQuestionnaire import RiskProfile

connection = sql.connect('patient.db')
c = connection.cursor()


def options(patientEmail):
    # if registration is not confirmed where patientEmail = patientEmail, try again later, end program
    # else, run program below:

        print("What would you like to do next?")
        print("Choose [1] to book an appointment")
        print("Choose [2] to cancel an appointment")
        print("Choose [3] to see your profile")
        action = int(input("Choice: "))
        if action == 1:
            pass
        elif action == 2:
            pass
        elif action == 3:
            print("Choose [1] to see your medical profile")
            print("Choose [2] to see your child's medical profile")
            print("Choose [3] to take the lifestyle questionnaire")
            print("Choose [4] to take the patient risk questionnaire")
            qaction = int(input("Choice: "))
            if qaction == 1:
                pass
            elif qaction == 2:
                name = RiskProfile
                name.show_profile()
            elif qaction == 3:
                print("Please fill out the following risk profile")
                x = RiskProfile()
                x.questions()
                x.BMI_calculator()
                x.diet()
                x.smoking()
                x.drugs()
                x.alcohol()
                x.insert_to_table()
            elif qaction == 4:
                x = PatientMedical()
                x.medicalHistory()
                x.cancer()


def task():
    print("Choose [1] to register for a new account")
    print("Choose [2] to login")
    action=input("Choice: ")
    if action != '1' and action != '2':
        print("I'm sorry, '" + action + "' is an invalid option. ")
        task()
    elif action == '1':
        firstName=input("Please enter your first name. ")
        lastName=input("Please enter your last name. ")
        dateOfBirth = input('Please enter your birthday in YYYY-MM-DD format. ')
        year, month, day = map(int, dateOfBirth.split('-'))
        dateOfBirth = datetime.date(year, month, day)
        today = date.today()
        age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
        print("Gender")
        print("Choose [1] for female")
        print("Choose [2] for male")
        print("Choose [3] for non-binary")
        gender=input("Choice: ")
        while gender != '1' and gender != '2' and gender != '3':
            print("I'm sorry, '" + gender + "' is an invalid option. ")
            print("Gender")
            print("Choose [1] for female")
            print("Choose [2] for male")
            print("Choose [3] for non-binary")
            gender=input("Choice: ")
        if gender == '1':
            gender = "Female"
        elif gender == '2':
            gender = "Male"
        elif gender == '3':
            gender = "Non-Binary"
        addressLine1 = input("Address Line 1: ")
        addressLine2 = input("Address Line 2 (including city): ")
        postcode = input("Postcode: ")
        telephoneNumber = input("Telephone in XXXXX-XXX-XXX format: ")
        patientEmail=input("Please enter your email. ")
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmail != []:
            while patientEmails != []:
                print("I'm sorry, that email is already in use. Please use another email.")
                patientEmail=input("Please enter your email. ")
                c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
                patientEmails = c.fetchall()
        password=getpass("Please enter your password. ")
        x=Patient(patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2, postcode, telephoneNumber, password)
        x.register()
        x.registrationSummary()
        options(x.patientEmail)
    elif action == '2':
        patientEmail=input("Please enter your email. ")
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        password=getpass("Please enter your password. ")
        if password != patientEmails[0][10]:
            while password != patientEmails[0][10]:
                print("I'm sorry, that password is not correct. ")
                password=getpass("Please enter your password. ")
            print("Wonderful! Hi, " + patientEmails[0][1] + " you are now logged in.")
            options(patientEmail)
        else:
            print("Wonderful! Hi, " + patientEmails[0][1] + " you are now logged in.")
            options(patientEmail)
    

print("Welcome!")
task()
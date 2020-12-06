import sqlite3 as sql
from getpass import getpass
from patient import Patient
from PatientRiskProfile import PatientMedical
from lifeStyleQuestionnaire import RiskProfile

connection = sql.connect('patient.db')
c = connection.cursor()


def options():
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
        email=input("Please enter your email. ")
        c.execute("SELECT * FROM PatientDetail WHERE email =?", [email])
        emails = c.fetchall()
        if email != []:
            while emails != []:
                print("I'm sorry, that email is already in use. Please use another email.")
                email=input("Please enter your email. ")
                c.execute("SELECT * FROM PatientDetail WHERE email =?", [email])
                emails = c.fetchall()
        password=getpass("Please enter your password. ")
        x=Patient(firstName, lastName, email, password)
        x.register()
        x.registrationSummary()
        options()
    elif action == '2':
        email=input("Please enter your email. ")
        c.execute("SELECT * FROM PatientDetail WHERE email =?", [email])
        emails = c.fetchall()
        password=getpass("Please enter your password. ")
        if password != emails[0][4]:
            while password != emails[0][4]:
                print("I'm sorry, that password is not correct. ")
                password=getpass("Please enter your password. ")
            print("Wonderful! Hi, " + emails[0][1] + " you are now logged in.")
            options()
        else:
            print("Wonderful! Hi, " + emails[0][1] + " you are now logged in.")
            options()
    

print("Welcome!")
task()
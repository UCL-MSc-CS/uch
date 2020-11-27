import sqlite3 as sql
from getpass import getpass
from patient import Patient

connection = sql.connect('patient.db')
c = connection.cursor()

def task():
    print("Welcome!")
    print("Choose [1] to register for a new account")
    print("Choose [2] to login")
    action=int(input("Choice: "))
    if action == 1:
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
        x.registrationSummary()
        x.options()
    elif action == 2:
        email=input("Please enter your email. ")
        password=getpass("Please enter your password. ")
    else:
        print("I'm sorry, that is an invalid option. Please type 'Register' or 'Login'. ")
        task()

task()
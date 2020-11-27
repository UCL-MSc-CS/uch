import sqlite3 as sql
from getpass import getpass


class Patient:

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.loggedIn = 1
        self.connection = sql.connect('patient.db')
        self.c = self.connection.cursor()
        self.update()

    def update(self):
        self.c.execute("INSERT INTO PatientDetail VALUES (null,?,?,?,?,?)",
                       (self.firstName, self.lastName, self.email, self.password, self.loggedIn))
        self.c.execute("SELECT * FROM PatientDetail WHERE firstName =? AND lastName =? AND email =?", [self.firstName, self.lastName, self.email])
        patientDetail = self.c.fetchall()
        for i in patientDetail:
            print(i)

    def login(self):
        email = input("Please enter your email. ")
        password = getpass("Please enter your password. ")
        self.loginCheck(email, password)

    def registrationSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        print("Welcome, " + self.firstName +
              "! Thank you for registering with UCH.")
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Email: " + self.email)
        print("Password: " + hash)

    def loginCheck(self, email, password):
        if self.email == email and self.password == password:
            self.loggedIn = True
            print("Hello, " + self.firstName + ", welcome back!")
            self.options()
        else:
            print("I'm sorry, those details are not correct, please try again. ")
            self.login()

    def options(self):
        print("What would you like to do next?")
        print("Choose [1] to book an appointment")
        print("Choose [2] to cancel an appointment")
        action=int(input("Choice: "))

    def patientSummary(self):
        hash=""
        for i in self.password:
            hash += "*"
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Email: " + self.email)
        print("Password: " + hash)
        print("Questionnaire: " + str(self.questionnaire))
        print("Appointments: " + str(self.appointments))
        print("Prescriptions: " + str(self.prescriptions))


def task():
    print("Welcome!")
    print("Choose [1] to register for a new account")
    print("Choose [2] to login")
    action=int(input("Choice: "))
    if action == 1:
        firstName=input("Please enter your first name. ")
        lastName=input("Please enter your last name. ")
        email=input("Please enter your email. ")
        password=getpass("Please enter your password. ")
        x=Patient(firstName, lastName, email, password)
        x.registrationSummary()
    elif action == 2:
        email=input("Please enter your email. ")
        password=getpass("Please enter your password. ")
    else:
        print("I'm sorry, that is an invalid option. Please type 'Register' or 'Login'. ")
        task()

task()

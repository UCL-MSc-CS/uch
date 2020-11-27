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
        self.c.execute("INSERT INTO PatientDetail VALUES (null,?,?,?,?,?)",
                       (self.firstName, self.lastName, self.email, self.password, self.loggedIn))

    def login(self):
        email = input("Please enter your email. ")
        password = getpass("Please enter your password. ")
        self.loginCheck(email, password)

    def registrationSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        self.c.execute("SELECT * FROM PatientDetail WHERE firstName =? AND lastName =? AND email =?",
                       [self.firstName, self.lastName, self.email])
        patientDetail = self.c.fetchall()
        for i in patientDetail:
            print("Welcome, " + i[1] + "! Thank you for registering with UCH.")
            print("Patient ID: " + str(i[0]))
            print("First Name: " + i[1])
            print("Last Name: " + i[2])
            print("Email: " + i[3])
            print("Password: " + hash)
            self.connection.commit()

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
        action = int(input("Choice: "))

    def patientSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Email: " + self.email)
        print("Password: " + hash)
        print("Questionnaire: " + str(self.questionnaire))
        print("Appointments: " + str(self.appointments))
        print("Prescriptions: " + str(self.prescriptions))

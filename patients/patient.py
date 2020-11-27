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

    def register(self):
        self.c.execute("INSERT INTO PatientDetail VALUES (null,?,?,?,?,?)",
                       (self.firstName, self.lastName, self.email, self.password, self.loggedIn))

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


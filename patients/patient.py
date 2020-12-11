import sqlite3 as sql
from getpass import getpass

class Patient:

    def __init__(self, patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2,
                 postcode, telephoneNumber, password):
        self.patientEmail = patientEmail
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.age = age
        self.gender = gender
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.postcode = postcode
        self.telephoneNumber = telephoneNumber
        self.password = password
        self.loggedIn = 1
        self.registrationConfirm = 0
        self.connection = sql.connect('patient.db')
        self.c = self.connection.cursor()

    def register(self):
        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (self.patientEmail, self.firstName, self.lastName, self.dateOfBirth, self.age, self.gender,
                        self.addressLine1, self.addressLine2, self.postcode, self.telephoneNumber, self.password,
                        self.loggedIn, self.registrationConfirm))
        self.connection.commit()

    def registrationSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        self.c.execute("SELECT * FROM PatientDetail WHERE firstName =? AND lastName =? AND patientEmail =?",
                       [self.firstName, self.lastName, self.patientEmail])
        patientDetail = self.c.fetchall()
        for i in patientDetail:
            print("Welcome, " + i[1] + "! Thank you for registering with UCH.")
            print("First Name: " + i[1])
            print("Last Name: " + i[2])
            print("Email: " + i[0])
            print("Password: " + hash)
            self.connection.commit()


# ari = Patient("ariannabourke@hotmail.com", "Arianna", "Bourke", "27/04/1988", 10, "male",
#               "123 Happy", "street", "12343", "389753957", "1234")







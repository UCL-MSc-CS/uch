import sqlite3 as sql
from numpy import random

""" This is the main patient class, to create a new patient in the database"""

class Patient:
    # Initializing a patient
    def __init__(self, patientEmail, firstName, lastName, dateOfBirth, gender, addressLine1, addressLine2,
                 postcode, telephoneNumber, password):
        self.nhsNumber = 0
        self.patientEmail = patientEmail
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.postcode = postcode
        self.telephoneNumber = telephoneNumber
        self.password = password
        # For admins to confirm registration of new patients
        self.registrationConfirm = 0
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()
        self.nhsGenerator()

    def register(self):
        # Puts new patients into the database
        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                       (self.nhsNumber, self.patientEmail, self.firstName, self.lastName, self.dateOfBirth, self.gender,
                        self.addressLine1, self.addressLine2, self.postcode, self.telephoneNumber, self.password,
                        self.registrationConfirm))
        self.connection.commit()
    
    def nhsGenerator(self):
        # To create a random and unique NHS number for each new patient
        count = 0
        nhsNumber = ""
        while count < 10:
            x = random.randint(0,9)
            nhsNumber += str(x)
            count += 1
        self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
        nhsNumbers = self.c.fetchall()
        if nhsNumbers != []:
            while nhsNumbers != []:
                count = 0
                nhsNumber = ""
                while count < 10:
                    x = random.randint(0,9)
                    nhsNumber += str(x)
                    count += 1
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
                nhsNumbers = self.c.fetchall()
        self.nhsNumber = nhsNumber


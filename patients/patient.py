import sqlite3 as sql
from numpy import random

""" This is the main patient class, to create a new patient in the database"""

class Patient:
    # Initializing a patient
    def __init__(self, patient_email, first_name, last_name, date_of_birth, gender, address_line_1, address_line_2,
                 postcode, telephone_number, password):
        self.NHS_number = 0
        self.patient_email = patient_email
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.postcode = postcode
        self.telephone_number = telephone_number
        self.password = password
        # For admins to confirm registration of new patients
        self.registration_confirm = 0
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()
        self.NHS_generator()

    def register(self):
        # Puts new patients into the database
        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                       (self.NHS_number, self.patient_email, self.first_name, self.last_name, self.date_of_birth, self.gender,
                        self.address_line_1, self.address_line_2, self.postcode, self.telephone_number, self.password,
                        self.registration_confirm))
        self.connection.commit()
    
    def NHS_generator(self):
        # To create a random and unique NHS number for each new patient
        count = 0
        NHS_number = ""
        while count < 10:
            x = random.randint(0,9)
            NHS_number += str(x)
            count += 1
        self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [NHS_number])
        NHS_numbers = self.c.fetchall()
        if NHS_numbers != []:
            while NHS_numbers != []:
                count = 0
                NHS_number = ""
                while count < 10:
                    x = random.randint(0,9)
                    NHS_number += str(x)
                    count += 1
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [NHS_number])
                NHS_numbers = self.c.fetchall()
        self.NHS_number = NHS_number


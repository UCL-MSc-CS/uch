import sqlite3 as sql
from numpy import random

"""
This is the main patient class, to create a new patient in the database.

In this class, all of the patient's personal details are initialised. After initialisation,
the patient's NHS number is randomly generated, and the patient's details are inserted into the database.
"""


class Patient:
    """
    This is a class for patients.

    Attributes:
        nhs_number (int): The patient's NHS number.
        patient_email (string): The patient's email.
        first_name (string): The patient's first name.
        last_name (string): The patient's last name.
        date_of_birth (string): The patient's date of birth.
        gender (string): The patient's gender.
        address_line_1 (string): The patient's first line of their address.
        address_line_2 (string): The patient's second line of their address.
        postcode (string): The patient's postcode.
        telephone_number (int): The patient's telephone number.
        password (string): The patient's password.
        registration_confirm (int): For adminstrators to confirm registration of new patients - 0 for not confirmed and 1 for confirmed.
    """

    def __init__(self):
        """
        The constructor for Patient class.
        """

        self.nhs_number = 0  # Generated on line 25
        self.patient_email = ""
        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.gender = ""
        self.address_line_1 = ""
        self.address_line_2 = ""
        self.postcode = ""
        self.telephone_number = 0
        self.password = ""
        self.registration_confirm = 0  
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()
        self.nhs_generator()

    def register(self):
        # Function puts new patients into the database.
        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (self.nhs_number, self.patient_email, self.first_name, self.last_name, self.date_of_birth, self.gender, self.address_line_1, self.address_line_2, self.postcode, self.telephone_number, self.password, self.registration_confirm))
        self.connection.commit()

    def nhs_generator(self):
        # Function creates a random and unique NHS number for each new patient.
        count = 0
        nhs_number = ""
        while count < 10:
            x = random.randint(0, 9)
            nhs_number += str(x)
            count += 1
        self.c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhs_number])
        nhs_numbers = self.c.fetchall()
        if nhs_numbers != []:
            while nhs_numbers != []:
                count = 0
                nhs_number = ""
                while count < 10:
                    x = random.randint(0, 9)
                    nhs_number += str(x)
                    count += 1
                self.c.execute(
                    "SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhs_number])
                nhs_numbers = self.c.fetchall()
        self.nhs_number = nhs_number

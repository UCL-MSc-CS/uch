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
    """

    def __init__(self, patient_email, first_name, last_name, date_of_birth, gender, address_line_1, address_line_2,
                 postcode, telephone_number, password):
        """
        The constructor for Patient class.

        Parameters:
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
        """

        self.NHS_number = 0  # Generated on line 25
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
        self.registration_confirm = 0  # For admins to confirm registration of new patients
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()
        self.NHS_generator()

    def register(self):
         """
         Function puts new patients into the database.
         """

        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                       (self.NHS_number, self.patient_email, self.first_name, self.last_name, self.date_of_birth, self.gender,
                        self.address_line_1, self.address_line_2, self.postcode, self.telephone_number, self.password,
                        self.registration_confirm))
        self.connection.commit()

    def NHS_generator(self):
         """
         Function creates a random and unique NHS number for each new patient.
         """

        count = 0
        NHS_number = ""
        while count < 10:
            x = random.randint(0, 9)
            NHS_number += str(x)
            count += 1
        self.c.execute(
            "SELECT * FROM PatientDetail WHERE nhsNumber =?", [NHS_number])
        NHS_numbers = self.c.fetchall()
        if NHS_numbers != []:
            while NHS_numbers != []:
                count = 0
                NHS_number = ""
                while count < 10:
                    x = random.randint(0, 9)
                    NHS_number += str(x)
                    count += 1
                self.c.execute(
                    "SELECT * FROM PatientDetail WHERE nhsNumber =?", [NHS_number])
                NHS_numbers = self.c.fetchall()
        self.NHS_number = NHS_number

import sqlite3 as sql
import random


class Patient:

    def __init__(self, patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2,
                 postcode, telephoneNumber, password):
        self.nhsNumber = 0
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
        self.registrationConfirm = 0
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()
        self.nhsGenerator()

    def register(self):
        self.c.execute("INSERT INTO PatientDetail VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (self.nhsNumber, self.patientEmail, self.firstName, self.lastName, self.dateOfBirth, self.age, self.gender,
                        self.addressLine1, self.addressLine2, self.postcode, self.telephoneNumber, self.password,
                        self.registrationConfirm))
        self.connection.commit()
    
    def nhsGenerator(self):
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
    
    def printNHS(self):
        x = str(self.nhsNumber)
        one = x[0:3]
        two = x[3:6]
        three = x[6:10]
        print(one, two, three)

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

# kamala = Patient("hello@me.com", "Kamala", "Harris", "27/04/1988", 10, "male",
#               "123 Happy", "street", "12343", "389753957", "1234")
# kamala.printNHS()
# kamala.register()
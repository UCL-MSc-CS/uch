
import sqlite3 as sql
from datetime import datetime as dt


class adminFunctions():

    def __init__(self):
        print("connection initialized")  # whenever you close the connection, you will have to
        self.connection = sql.connect('UCH.db')
        # create a new adminFunctions() object to re-open
        self.c = self.connection.cursor()  # the connection, so that __init__ is called.

    def admin_login(self):
        username = input('Username: (press 0 to go back) ')
        if username == '0':
            return "restart"
        password = input('Password: ')
        self.c.execute("SELECT * FROM Admin WHERE username=? AND password =?", (username, password))
        items = self.c.fetchall()
        if len(items) == 0:
            return False
        else:
            print("Logged in")
            return True

    def add_doctor(self):
        print("registering new physician")
        create = int(input("choose [1] to input physician or [2] to exit: "))
        if create == 1:
            a = input("email ")
            b = input("first name ")
            c = input("last name ")
            d = int(input("enter date of birth as ddmmyy "))
            f = input("specialty ")
            g = int(input("telephone number: "))
            i = input("gender: ")
            j = "Y"
            gp = [a, b, c, d, f, g, i, j]
            self.c.execute("""INSERT INTO Doctor VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", gp)
            self.c.execute("SELECT * FROM Doctor")
            items = self.c.fetchall()
            for i in items:
                print(i)
            self.connection.commit()
            return 0
        elif create == 2:
            return 0
        else:
            print("did not enter Y or N")
            raise NameError

    def check_registrations(self):
        self.c.execute("""SELECT COUNT(patientID) FROM PatientDetail WHERE registrationConfirm = 'N' """)
        items = self.c.fetchall()
        count = items[0][0]
        print("You have %d patient registrations to confirm" % count)

    def confirm_registrations(self):
        self.c.execute("""SELECT * FROM PatientDetail WHERE registrationConfirm = 'N'""")
        items = self.c.fetchall()
        if len(items) == 0:
            print("no patient registrations to confirm")
        else:
            for i in items:
                print("first name: {}".format(i[1]))
                print("last name: {}".format(i[2]))
                print("date of birth: {}".format(i[3]))
                print("age: {}".format(i[4]))
                print("gender: {}".format(i[5]))
                print("address line 1: {}".format(i[6]))
                print("addresss line 2: {}".format(i[7]))
                print("postcode: {}".format(i[8]))
                print("telephone number: {}".format(i[9]))
                print("email: {}".format(i[10]))
                change = input("Do you want to confirm this registration?: (Y/N) ")
                while change != 'Y' and change != 'N':
                    if change == 'Y':
                        self.c.execute("""UPDATE PatientDetail SET registrationConfirm = 'Y' WHERE email = ? """,
                                       (i[10],))
                    elif change == 'N':
                        print("registration not confirmed")
                    else:
                        print("please enter Y/N")
                        change = input("Do you want to confirm this registration?: (Y/N) ")
            self.connection.commit()

    def deactivate_doctor(self):
        email = input("Type in the practitioner's email: ")
        self.c.execute("""UPDATE Doctor SET active = 'N' WHERE email = ?""", (email,))
        self.c.execute("SELECT * FROM Doctor")
        items = self.c.fetchall()
        for i in items:
            print(i)
        self.connection.commit()
        # add in exception handling here

    def delete_doctor(self):
        email = input("Type in the practitioner's email: ")
        self.c.execute("DELETE FROM Doctor WHERE email = ?", (email,))
        self.c.execute("SELECT * FROM Doctor")
        items = self.c.fetchall()
        for i in items:
            print(i)
        self.connection.commit()

    def cin(self):
        intime = dt.now()
        In = str((input("Type in appointment id: ")))
        self.c.execute("""UPDATE Appointment SET checkin = datetime('now') WHERE appointmentID = ? """, In)
        self.connection.commit()
        # add exceptions

    def cout(self):
        outtime = dt.now()
        Out = str(input("Type in appointment id: "))
        self.c.execute("""UPDATE Appointment SET checkout = datetime('now') WHERE appointmentID = ? """, Out)
        self.connection.commit()
        # add exceptions

    def managedet(self):
        patID = int(input("enter patient ID: "))
        firstn = input("first name: ")
        lastnm = input("last name: ")
        dateob= input("date of birth as dd/mm/yyyy: ")
        age = int(input("age: "))
        gender = input("gender: ")
        addl1 = input("address line 1: ")
        addl2 = input("address line 2: ")
        postcode = int(input("postcode: "))
        tel = int(input("telephone number: "))
        email = input("email: ")
        regcon = input("Registration confirmation: Y or N")

        self.c.execute("""UPDATE PatientDetail SET firstName = ?, lastName = ?, dateOfBirth = ?,
        age = ?, gender = ?, addressLine1 = ?, addressLine2 = ?, postcode = ?,
        telephoneNumber = ?, email = ?, registrationConfirm = ? WHERE patientID = ?""",
        (firstn) (lastnm) (dateob) (age) (gender) (addl1) (addl2) (postcode) (tel) (email) (regcon), (patID))
        self.connection.commit()

    def delpatdet(self):
        patID = int(input("enter patient ID: "))

        self.c.execute("""DELETE FROM PatientDetail WHERE patientID = ?""", (patID,))
        self.connection.commit()

    def commit_and_close(self):
        self.connection.commit()
        self.connection.close()


# yadayada add more functions for selections


"""old code under here"""

# def addGP():
#     print("registering new physician")
#     create = int(input("choose [1] to input physician or [2] to exit: "))
#     if create == 1:
#         a = input("first name ")
#         b = input("last name ")
#         c = input("email ")
#         d = int(input("enter date of birth as ddmmyy "))
#         f = input("specialty ")
#         gp = physician(a, b, c, d, f)
#         gp.add_physician()
#     elif create == 2:
#         pass  # add code to abort registration
#     else:
#         print("did not enter Y or N")
#         raise NameError
#
# #yadayada add more functions for selections
#
# class physician():
#     def __init__(self, first, last, email, date_birth, specialty):
#         self.first = first
#         self.last = last
#         self.email = email
#         self.date_birth = date_birth
#         self.specialty = specialty
#
#     def add_physician(self):
#         connection = sql.connect('UCH.db')
#         c = connection.cursor()
#         input = [self.email, self.first, self.last, self.date_birth, self.specialty]
#         c.execute("""INSERT INTO doctors VALUES(?, ?, ?, ?, ?)""", input)
#         connection.commit()
#         # The following allows you to check the doctors table:
#         # c.execute("SELECT * FROM doctors")
#         # items = c.fetchall()
#         # for i in items:
#         #     print(i)
#         # connection.commit()

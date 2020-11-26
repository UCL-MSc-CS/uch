import sqlite3 as sql

class adminFunctions():

    def __init__(self):                              # whenever you close the connection, you will have to
        self.connection = sql.connect('UCH.db')      # create a new adminFunctions() object to re-open
        self.c = self.connection.cursor()            # the connection, so that __init__ is called.

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
            gp = [a, b, c, d, f, g, i ,j]
            self.c.execute("""INSERT INTO doctors VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", gp)

        elif create == 2:
            pass  # add code to abort registration
        else:
            print("did not enter Y or N")
            raise NameError

    def check_registrations(self):
        self.c.execute("""SELECT COUNT(patientID) FROM patient_details WHERE registrationConfirm = 'N' """)
        items = self.c.fetchall()
        count = items[0][0]
        print("You have %d patient registrations to confirm" % count)

    def confirm_registrations(self):
        self.c.execute("""SELECT * FROM patient_details WHERE registrationConfirm = 'N'""")
        items = self.c.fetchall()
        for i in items:
            print(i)
            change = input("Do you want to confirm this registration?: (Y/N)")
            if change == 'Y':
                pass
                # key = ("Type in the practitioner's email: ")
                # c.execute("""UPDATE patient_details SET registrationConfirm = 'Y' WHERE email = '?' """, key)

    def deactivate_doctor(self):
        key = input("Type in the practitioner's email: ")
        self.c.execute("""UPDATE doctors SET active = 'N' WHERE email = ?""",(key,))
        # add in exception handling here

    def cin(self):
        In = int(input("Type in appointment id: "))
        self.c.execute("""UPDATE Appointment SET checkin = (fill in time stamp) WHERE appointment_ID = ? """, (In,))
        #add exceptions
    def cout(self):
        Out = int(input("Type in appointment id: "))
        self.c.execute("""UPDATE Appointment SET checkout = (fill in time stamp") WHERE appointment_ID = ? """, (Out))
        #add exceptions
    def commit_and_close(self):
        self.connection.commit()
        self.connection.close()



#yadayada add more functions for selections


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
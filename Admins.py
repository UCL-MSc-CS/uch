from datetime import datetime as dt
import sqlite3 as sql
from datetime import datetime as dt

"""exceptions under here"""
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class FieldEmpty(Error):
    """
    Exception raised when the user provides a blank input

    :param: message - explanation of the error to the user
    """
    def __init__(self, message = "this field cannot be left empty"):
        self.message = message
        super().__init__(self.message)

class EmailInUse(Error):
    """
    Exception raised when the email is already in use

    :param: email - input email which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, email, message = "email already in use"):
        self.email = email
        self.message = message
        super().__init__(self.message)

class EmailInvalid(Error):
    """
    Exception raised when the email does not contain @ or .co

    :param: email - input email which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, email, message = "please enter a valid email"):
        self.email = email
        self.message = message
        super().__init__(self.message)

class EmailNotExists(Error):
    """Exception raised when email does not exist in list"""
    def __init__(self, message = "email does not exists"):
        self.message = message
        super().__init__(self.message)

class IncorrectInputLength(Error):
    """
    Exception raised when the input length is incorrect

    :param: correct_length - input length that the input should be
            message - explanation of the error to the user
    """
    def __init__(self, correct_length):
        self.correct_length = str(correct_length)
        self.message = "Incorrect input length, input should be {} characters long" .format(correct_length)
        super().__init__(self.message)

class GenderError(Error):
    """
    Exception raised when the input gender is incorrect

    :param: message - explanation of the error to the user
    """
    def __init__(self, message = "please enter one of the options shown"):
        self.message = message
        super().__init__(self.message)

class InvalidAgeRange(Error):
    """Exception raised when age is not supported by date of birth"""
    def __init__(self, message = "please input correct age"):
        self.message = message
        super().__init__(self.message)

class InvalidAdd(Error):
    """exception raised when address is not valid"""
    def __init__(self, message = "please input address containing number and street"):
        self.message = message
        super().__init__(self.message)

""" admin functions under here: """

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
            try:
                a = input("email: ")
                if not a:
                    raise FieldEmpty()
                if "@" not in a or (".co" not in a and ".ac" not in a and ".org" not in a and ".gov" not in a):
                    raise EmailInvalid(a)
                self.c.execute("SELECT * FROM Doctor WHERE email = ?", (a,))
                items = self.c.fetchall()
                if len(items) != 0:
                    raise EmailInUse(a)
                b = input("first name: ")
                if not b:
                    raise FieldEmpty()
                c = input("last name: ")
                if not c:
                    raise FieldEmpty()
                d = int(input("enter date of birth as ddmmyy: "))
                if not d:
                    raise FieldEmpty()
                input_list = [int(i) for i in str(d)]  
                if len(input_list) != 6:
                    correct_length = 6
                    raise IncorrectInputLength(6)
                f = input("specialty: ")
                if not f:
                    raise FieldEmpty()
                g = (input("telephone number: "))
                if not g:
                    raise FieldEmpty()
                input_list = [i for i in g]  
                if len(input_list) != 11:
                    correct_length = 11
                    raise IncorrectInputLength(correct_length)
                i = input("gender (enter male/female/non-binary/prefer not to say): ")
                if not i:
                    raise FieldEmpty()
                if i != "male" or i != "female" or i != "non-binary" or i != "prefer not to say":
                    raise GenderError()
                j = "Y"
            except FieldEmpty:
                error = FieldEmpty()
                print(error)
                return 1
            except EmailInvalid:
                error = EmailInvalid(a)
                print(error)
                return 1
            except EmailInUse:
                error = EmailInUse(a)
                print(error)
                return 1
            except ValueError:
                print("please provide a numerical input")
                return 1
            except IncorrectInputLength:
                error = IncorrectInputLength(correct_length)
                print(error)
                return 1
            except GenderError:
                error = GenderError()
                print(error)
                return 1
            else:
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
        try:
            email = input("Type in the practitioner's email (press 0 to go back): ")
            if email == "0":
                return 0
            if not email:
                raise FieldEmpty()
            if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                raise EmailInvalid(email)
        except FieldEmpty:
            error = FieldEmpty()
            print(error)
            return 1
        except EmailInvalid:
            error = EmailInvalid(email)
            print(error)
            return 1
        else:
            self.c.execute("SELECT * FROM Doctor WHERE email = ?", (email,))
            items = self.c.fetchall()
            if len(items) == 0:
                print("no record exists with this email")
                return 1
            else:
                self.c.execute("""UPDATE Doctor SET active = 'N' WHERE email = ?""", (email,))
                self.c.execute("SELECT * FROM Doctor")
                items = self.c.fetchall()
                for i in items:
                    print(i)
                self.connection.commit()
                return 0

    def delete_doctor(self):
        try:
            email = input("Type in the practitioner's email (press 0 to go back): ")
            if email == "0":
                return 0
            if not email:
                raise FieldEmpty()
            if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                raise EmailInvalid(email)
        except FieldEmpty:
            error = FieldEmpty()
            print(error)
            return 2
        except EmailInvalid:
            error = EmailInvalid(email)
            print(error)
            return 2
        else:
            self.c.execute("SELECT * FROM Doctor WHERE email = ?", (email,))
            items = self.c.fetchall()
            if len(items) == 0:
                print("no record exists with this email")
                return 2
            else:
                self.c.execute("DELETE FROM Doctor WHERE email = ?", (email,))
                self.c.execute("SELECT * FROM Doctor")
                items = self.c.fetchall()
                for i in items:
                    print(i)
                self.connection.commit()
                return 0

    def cin(self):
        try:
            intime = dt.now()
            In = str((input("Type in appointment id (press 0 to go back): ")))
            if In == "0":
                return 0
            if not In:
                raise FieldEmpty()
            check_number = int(In)
        except FieldEmpty:
            error = FieldEmpty()
            print(error)
            return 1
        except ValueError:
            print("please provide a numerical input")
            return 1
        else:
            self.c.execute("SELECT * FROM Appointment WHERE appointmentID = ?", (In,))
            items = self.c.fetchall()
            if len(items) == 0:
                print("no record exists with this appointmentID")
                return 1
            self.c.execute("SELECT checkin FROM Appointment WHERE appointmentID = ?", (In,))
            items = self.c.fetchall()
            if len(items) != 0:
                print("a check-in time has already been provided for that appointment")
                return 1
            else:
                self.c.execute("""UPDATE Appointment SET checkin = datetime('now') WHERE appointmentID = ? """, In)
                self.connection.commit()
                return 0

    def cout(self):
        try:
            outtime = dt.now()
            Out = str(input("Type in appointment id (press 0 to go back): "))
            if Out == "0":
                return 0
            if not Out:
                raise FieldEmpty()
            check_number = int(Out)
        except FieldEmpty:
            error = FieldEmpty()
            print(error)
            return 2
        except ValueError:
            print("please provide a numerical input")
            return 2
        else:
            self.c.execute("SELECT * FROM Appointment WHERE appointmentID = ?", (Out,))
            items = self.c.fetchall()
            if len(items) == 0:
                print("no record exists with this appointmentID")
                return 2
            self.c.execute("SELECT checkin FROM Appointment WHERE appointmentID = ?", (In,))
            items = self.c.fetchall()
            if len(items) != 0:
                print("a check-in time has already been provided for that appointment")
                return 2
            else:
                self.c.execute("""UPDATE Appointment SET checkout = datetime('now') WHERE appointmentID = ? """, Out)
                self.connection.commit()
                return 0

    def managedet(self):
        try:
            email = input("enter patient email: ")
            self.c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?", (email,))
            emailq = self.c.fetchall()
            if not email:
                raise FieldEmpty
            elif len(emailq) < 1:
                raise EmailNotExists

            firstn = input("first name: ")
            if not firstnm:
                raise FieldEmpty

            lastnm = input("last name: ")
            if not lastnm:
                raise FieldEmpty

            dateob= int(input("date of birth as dd/mm/yyyy: "))
            if not dateob:
                raise FieldEmpty()
            input_list2 = [int(i) for i in str(d)]
            if len(input_list2) != 6:
                correct_length = 6
                raise IncorrectInputLength(6)

            age = int(input("age: "))
            currdate = dt.now().year
            dobyear = int(dateob[:4])
            if age != currdate - dobyear or age != currdate - dobyear - 1:
                raise InvalidAgeRange
            elif not age:
                raise FieldEmpty()

            gender = input("gender (enter male/female/non-binary/prefer not to say): ")
            if not gender:
                raise FieldEmpty()
            if gender != "male" or gender != "female" or gender != "non-binary" or gender != "prefer not to say":
                raise GenderError()

            addl1 = input("address line 1: ")
            if not addl1:
                raise FieldEmpty()
            elif any(chr.isdigit() for chr in addl1) == False:
                raise InvalidAddr

            addl2 = input("address line 2: ")
            if not add2:
                raise FieldEmpty()
            elif any(chr.isdigit() for chr in addl1) == False:
                raise InvalidAddr

            postcode = int(input("postcode: "))
            if not postcode:
                raise FieldEmpty()

            tel = int(input("telephone number: "))
            if not tel:
                raise FieldEmpty()
            elif len(tel) <= 10 or len >= 12:
                raise IncorrectInputLength
                #ask matthew about this exception

            regcon = input("Registration confirmation: Y or N")
            #fill in Y later

        except EmailNotExists:
            error = EmailNotExists()
            print(error)
        except FieldEmpty:
            error = FieldEmpty()
            print(error)
        except IncorrectInputLength:
            error = IncorrectInputLength(correct_length)
            print(error)
        except InvalidAgeRange:
            error = InvalidAgeRange()
            print(error)
        except GenderError:
            error = GenderError()
            print(error)
        except InvalidAdd:
            error = InvalidAdd()
            print(error)
        else:
            self.c.execute("""UPDATE PatientDetail SET firstName = ?, lastName = ?, dateOfBirth = ?,
            age = ?, gender = ?, addressLine1 = ?, addressLine2 = ?, postcode = ?,
            telephoneNumber1 = ?, registrationConfirm = ? WHERE patientEmail = ?""",
            (firstn, lastnm, dateob, age, gender, addl1, addl2, postcode, tel, regcon, email))
            self.connection.commit()

    def delpatdet(self):
        try:
            email = input("enter patient email: ")
            self.c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?", (email,))
            emailq = self.c.fetchall()
            if not email:
                raise FieldEmpty
            elif len(emailq) < 1:
                raise EmailNotExists
        except EmailNotExists:
            error = EmailNotExists()
            print(error)
        except FieldEmpty:
            error = FieldEmpty()
            print(error)

        else:
            self.c.execute("""DELETE FROM PatientDetail WHERE patientEmail = ?""", (email,))
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

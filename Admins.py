import sqlite3 as sql
from datetime import datetime as dt
from datetime import date 
import usefulfunctions as uf

"""exceptions under here"""
# still need to come up with UK postcode validity check - make user input space separated post code,
# splice the inputted string at the space to get the outcode and incode, check the outcode and incode,
# based on the rules we found.
# change telephone number check (won't work with international numbers rn)
# DoB not in future check.

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

class nhsNotExists(Error):
    """Exception raised when email does not exist in list"""
    def __init__(self, message = "please enter an existing NHS number"):
        self.message = message
        super().__init__(self.message)

class DateInvalidError(Error):
    """
    Exception raised when the date is not in the correct format (dd/mm/yyyy)

    :param: date - input date which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "date does not exist, please enter a valid date"):
        self.message = message
        super().__init__(self.message)

class DateInFutureError(Error):
    """
    Exception raised when the date of birth is in the future

    :param: date - input date which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "date of birth cannot be in the future"):
        self.message = message
        super().__init__(self.message)

class DateFormatError(Error):
    """
    Exception raised when the date of birth is not in the format dd/mm/yyyy

    :param: date - input date which causes the error
            message - explanation of the error to the user
    """
    def __init__(self, message = "please enter the date in the correct format, with '-'s as separators"):
        self.message = message
        super().__init__(self.message)

class TeleNoFormatError(Error):
    """
    Exception raised when the inputted phone number is not in the format +<country code>xxxxxxxxxx

    :param: message - explanation of the error to the user
    """
    def __init__(self, message = "please enter the phone number in the correct format"):
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

class IntegerError(Error):
    """exception raised when integer is not in choice range"""
    def __init__(self, message = "please input a valid number"):
        self.message = message
        super().__init__(self.message)

""" admin functions under here: """

class adminFunctions():

    def __init__(self): 
        self.connection = sql.connect('UCH.db')
        self.c = self.connection.cursor()  

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
            return True

    def add_doctor(self):
        question_num = 0
        while True:
            try:
                while question_num == 0:
                    a = input("email: ")
                    if a == '0':
                        print('going back')
                        return 0
                    if not a:
                        raise FieldEmpty()
                    if "@" not in a or (".co" not in a and ".ac" not in a and ".org" not in a and ".gov" not in a):
                        raise EmailInvalid(a)
                    self.c.execute("SELECT * FROM GP WHERE gpEmail = ?", (a,))
                    items = self.c.fetchall()
                    if len(items) != 0:
                        raise EmailInUse(a)
                    question_num = 1
                while question_num == 1:
                    pw = input("password: ")
                    if pw == '0':
                        print('going back')
                        return 0
                    if not pw:
                        raise FieldEmpty()
                    question_num = 2
                while question_num == 2:
                    b = input("first name: ")
                    if b == '0':
                        print('going back')
                        return 0
                    if not b:
                        raise FieldEmpty()
                    question_num = 3
                while question_num == 3:
                    c = input("last name: ")
                    if c == '0':
                        print('going back')
                        return 0
                    if not c:
                        raise FieldEmpty()
                    question_num = 4
                while question_num == 4:
                    dateOfBirth = (input("enter date of birth as YYYY-MM-DD: "))
                    if dateOfBirth == '0':
                        print('going back')
                        return 0
                    if not dateOfBirth:
                        raise FieldEmpty()
                    if len(dateOfBirth) != 10:
                        correct_length = 10
                        raise IncorrectInputLength(10)
                    if dateOfBirth[4] != '-' or dateOfBirth[7] != '-':
                        raise DateFormatError
                    day = int(dateOfBirth[8:10])
                    month = int(dateOfBirth[5:7])
                    year = int(dateOfBirth[0:4])
                    if month == 9 or month == 4 or month == 6 or month == 11:
                        if day > 30:
                            raise DateInvalidError
                    elif month == 2:
                        if year % 4 != 0:
                            if day > 28:
                                raise DateInvalidError
                        elif year % 4 == 0:
                            if day > 29:
                                raise DateInvalidError
                    else:
                        if day > 31:
                            raise DateInvalidError
                    if month > 12:
                        raise DateInvalidError
                    
                    # input_list = [int(i) for i in str(dateOfBirth)]
                    date_entered = date(year,month,day)
                    date_today = date.today()
                    if date_entered > date_today:
                        raise DateInFutureError
                    dateOfBirth = uf.tounixtime(date_entered)
                    print(dateOfBirth)
                    question_num = 5
                while question_num == 5:
                    department = input("department: ")
                    if department == '0':
                        print('going back')
                        return 0
                    if not department:
                        raise FieldEmpty()
                    question_num = 6
                while question_num == 6:
                    teleNo = input("telephone number (no spaces, with country code. E.g. +4471234123123): ")
                    if teleNo == '0':
                        print('going back')
                        return 0
                    if not teleNo:
                        raise FieldEmpty()
                    if '+' not in teleNo or ' ' in teleNo:
                        raise TeleNoFormatError()
                    teleNo = teleNo.replace('+', '')
                    input_list = [i for i in teleNo]
                    if len(input_list) != 11 and len(input_list) != 12 and len(input_list) != 13 and len(input_list) != 14 and len(input_list) != 15 and len(input_list) != 16 and len(input_list) != 17:
                        correct_length = '12 to 18'
                        raise IncorrectInputLength(correct_length)
                    question_num = 7
                while question_num == 7:
                    gender = input("gender (enter male/female/non-binary/prefer not to say): ")
                    gender = gender.lower()
                    if gender == '0':
                        print('going back')
                        return 0
                    if not gender:
                        raise FieldEmpty()
                    if gender != 'male' and gender != 'female' and gender != 'non-binary' and gender != 'prefer not to say':
                        raise GenderError()
                    active = "Y"
                    question_num = 8
                while question_num == 8:
                    addressL1 = input("Address Line 1: ")
                    if addressL1 == '0':
                        print('going back')
                        return 0
                    if not addressL1:
                        raise FieldEmpty()
                    addressL2 = input("Address Line 2: ")
                    if addressL2 == '0':
                        print('going back')
                        return 0
                    if not addressL2:
                        raise FieldEmpty()
                    question_num = 9
            except FieldEmpty:
                error = FieldEmpty()
                print(error)
            except EmailInvalid:
                error = EmailInvalid(a)
                print(error)
            except EmailInUse:
                error = EmailInUse(a)
                print(error)
            except ValueError:
                print("please provide a numerical input")
            except TeleNoFormatError:
                error = TeleNoFormatError()
                print(error)
            except IncorrectInputLength:
                error = IncorrectInputLength(correct_length)
                print(error)
            except GenderError:
                error = GenderError()
                print(error)
            except DateInvalidError:
                error = DateInvalidError()
                print(error)
            except DateInFutureError:
                error = DateInFutureError()
                print(error)
            except DateFormatError:
                error = DateFormatError()
                print(error)
            else:
                gp = [a, pw, b, c, gender, dateOfBirth, addressL1, addressL2, teleNo, department, active]
                self.c.execute("""INSERT INTO GP VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", gp)
                print("Details entered successfully")
                return 0

    def check_registrations(self):
        self.c.execute("""SELECT COUNT(patientEmail) FROM PatientDetail WHERE registrationConfirm = 0 """)
        items = self.c.fetchall()
        count = items[0][0]
        print("   < You have %d patient registrations to confirm >" % count)

    def confirm_registrations(self):
        self.c.execute("""SELECT * FROM PatientDetail WHERE registrationConfirm = 0 """)
        items = self.c.fetchall()
        if len(items) == 0:
            print("no patient registrations to confirm")
        else:
            for i in items:
                print("NHS Number: {}".format(i[0]))
                print("email: {}".format(i[1]))
                print("first name: {}".format(i[2]))
                print("last name: {}".format(i[3]))
                date = uf.toregulartime(i[4])
                date = date.strftime("%Y-%m-%d") 
                print("date of birth: {}".format(date))
                print("gender: {}".format(i[5]))
                print("address line 1: {}".format(i[6]))
                print("addresss line 2: {}".format(i[7]))
                print("postcode: {}".format(i[8]))
                tele_no = '+' + str(i[9])
                print("telephone number: {}".format(tele_no))
                change = input("Do you want to confirm this registration?: (Y/N) ")
                while change != 'Y' and change != 'N':
                    if change == 'Y':
                        self.c.execute("""UPDATE PatientDetail SET registrationConfirm = 1 WHERE patientEmail = ? """,
                                       (i[1],))
                    elif change == 'N':
                        print("registration not confirmed")
                    else:
                        print("please enter Y/N")
                        change = input("Do you want to confirm this registration?: (Y/N) ")
            self.connection.commit()

    def deactivate_doctor(self):
        while True:
            try:
                email = input("Type in the practitioner's email (press 0 to go back): ")
                if email == '0':
                    return 2
                if not email:
                    raise FieldEmpty()
                if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                    raise EmailInvalid(email)
            except FieldEmpty:
                error = FieldEmpty()
                print(error)
            except EmailInvalid:
                error = EmailInvalid(email)
                print(error)
            else:
                self.c.execute("SELECT * FROM GP WHERE gpEmail = ?", (email,))
                items = self.c.fetchall()
                if len(items) == 0:
                    print("no record exists with this email")
                else:
                    self.c.execute("""UPDATE GP SET active = 'N' WHERE gpEmail = ?""", (email,))
                    self.c.execute("SELECT * FROM GP")
                    items = self.c.fetchall()
                    for i in items:
                        print(i)
                    self.connection.commit()
                    return 2

    def delete_doctor(self):
        providing_input = True
        while providing_input == True:
            try:
                email = input("Type in the practitioner's email (press 0 to go back): ")
                if email == "0":
                    return 2
                if not email:
                    raise FieldEmpty()
                if "@" not in email or (".co" not in email and ".ac" not in email and ".org" not in email and ".gov" not in email):
                    raise EmailInvalid(email)
            except FieldEmpty:
                error = FieldEmpty()
                print(error)
            except EmailInvalid:
                error = EmailInvalid(email)
                print(error)
            else:
                self.c.execute("SELECT * FROM GP WHERE gpEmail = ?", (email,))
                items = self.c.fetchall()
                if len(items) == 0:
                    print("no record exists with this email")
                else:
                    self.c.execute("DELETE FROM GP WHERE gpEmail = ?", (email,))
                    self.c.execute("SELECT * FROM GP")
                    items = self.c.fetchall()
                    for i in items:
                        print(i)
                    self.connection.commit()
                    return 2

    def cin(self):
        try:
            intime = dt.now()
            print("********************************************")
            In = str(input("Type in appointment id (press 0 to go back): "))
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
            print("< Please provide a numerical input >")
            return 1
        else:
            self.c.execute("SELECT * FROM Appointment WHERE appointmentID = ?", (check_number,))
            items = self.c.fetchall()
            if len(items) == 0:
                print("No record exists with this appointmentID")
                return 1
            self.c.execute("SELECT checkIn FROM Appointment WHERE appointmentID = ?", (check_number,))
            items = self.c.fetchall()
            if len(items) != 0:
                print("A check-in time has already been provided for that appointment")
                return 1
            else:
                unixd = dt.utcnow().timestamp()
                print(unixd)
                self.c.execute("""UPDATE Appointment SET checkIn = ? WHERE appointmentID = ? """, (unixd, check_number))
                self.connection.commit()
                print("successfully checked in patient")
                return 0

    def cout(self):
        try:
            outtime = dt.now()
            print("********************************************")
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
            print("< Please provide a numerical input >")
            return 2
        else:
            self.c.execute("SELECT * FROM Appointment WHERE appointmentID = ?", (Out,))
            items = self.c.fetchall()
            if len(items) == 0:
                print("No record exists with this appointmentID")
                return 2
            self.c.execute("SELECT checkIn FROM Appointment WHERE appointmentID = ?", (In,))
            items = self.c.fetchall()
            if len(items) != 0:
                print("A check-in time has already been provided for that appointment")
                return 2
            else:
                unixd = dt.utcnow().timestamp()
                print(unixd)
                self.c.execute("""UPDATE Appointment SET checkOut = ? WHERE appointmentID = ? """, (unixd, Out))
                self.connection.commit()
                print("Successfully checked out patient")
                return 0

    def managedet(self):
        masterback = 0
        while masterback == 0:
            try:
                print("********************************************")
                nhsnum = input("Enter patient nhs number (press 0 to go back): ")
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhsnum,))
                nhsq = self.c.fetchall()
                if nhsnum == '0':
                    masterback = 1
                    break
                elif not nhsnum:
                    raise FieldEmpty()
                elif len(nhsq) < 1:
                    raise nhsNotExists
            except FieldEmpty:
                error = FieldEmpty()
                print(error)
            except nhsNotExists:
                error = nhsNotExists()
                print(error)
            else:
                patback = 0
                question_num = 1
                while patback == 0:
                    print("********************************************")
                    print("Press [0] to re-enter NHS number: ")
                    print("Press [1] to go back to update patient details menu")
                    try:
                        while question_num == 1:
                            emails = input("New email: ")
                            if emails == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif emails == '1':
                                return masterback
                                break
                            elif "@" not in emails or ".com" not in emails:
                                raise EmailInvalid(emails)
                            elif not emails:
                                raise FieldEmpty
                            question_num = 2

                        while question_num == 2:
                            firstn = input("New first name: ")
                            if firstn == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif firstn == '1':
                                return masterback
                                break
                            elif not firstn:
                                raise FieldEmpty
                            question_num = 3

                        while question_num == 3:
                            lastnm = input("New last name: ")
                            if lastnm == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif lastnm == '1':
                                return masterback
                                break
                            elif not lastnm:
                                raise FieldEmpty
                            question_num = 4

                        while question_num == 4:
                            dateOfBirth = (input("New date of birth as YYYY-MM-DD: "))
                            if dateOfBirth == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif dateOfBirth == '1':
                                return masterback
                                break
                            elif not dateOfBirth:
                                raise FieldEmpty()
                            elif len(dateOfBirth) != 10:
                                correct_length = 10
                                raise IncorrectInputLength(10)
                            elif dateOfBirth[4] != '-' or dateOfBirth[7] != '-':
                                raise DateFormatError
                            day = int(dateOfBirth[8:10])
                            month = int(dateOfBirth[5:7])
                            year = int(dateOfBirth[0:4])
                            if month == 9 or month == 4 or month == 6 or month == 11:
                                if day > 30:
                                    raise DateInvalidError
                            elif month == 2:
                                if year % 4 != 0:
                                    if day > 28:
                                        raise DateInvalidError
                                elif year % 4 == 0:
                                    if day > 29:
                                        raise DateInvalidError
                            else:
                                if day > 31:
                                    raise DateInvalidError
                            if month > 12:
                                raise DateInvalidError

                            # input_list = [int(i) for i in str(dateOfBirth)]
                            date_entered = date(year, month, day)
                            date_today = date.today()
                            if date_entered > date_today:
                                raise DateInFutureError
                            dateOfBirth = uf.tounixtime(date_entered)
                            print(dateOfBirth)
                            question_num = 6

                        while question_num == 6:
                            gender = input("New gender (enter male/female/non-binary/prefer not to say): ")
                            if gender == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif gender == '1':
                                return masterback
                                break
                            elif not gender:
                                raise FieldEmpty()
                            if gender != "male" and gender != "female" and gender != "non-binary" and gender != "prefer not to say":
                                raise GenderError()
                            question_num = 7

                        while question_num == 7:
                            addl1 = input("New address line 1: ")
                            if addl1 == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif addl1 == '1':
                                return masterback
                                break
                            elif not addl1:
                                raise FieldEmpty()
                            elif any(chr.isdigit() for chr in addl1) == False:
                                raise InvalidAdd
                            question_num = 8

                        while question_num == 8:
                            addl2 = input("New address line 2: ")
                            if addl2 == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif addl2 == '1':
                                return masterback
                                break
                            elif not addl2:
                                raise FieldEmpty()
                            elif any(chr.isdigit() for chr in addl1) == False:
                                raise InvalidAdd
                            question_num = 9

                        while question_num == 9:
                            postcode = input("New postcode: ")
                            if postcode == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif postcode == '1':
                                return masterback
                                break
                            elif not postcode:
                                raise FieldEmpty()
                            question_num = 10

                        while question_num == 10:
                            tel = (input("New telephone number (no spaces, with country code. E.g. +4471234123123): "))
                            if tel == '0':
                                return adminFunctions.managedet(self)
                                break
                            elif tel == '1':
                                return masterback
                                break
                            elif not tel:
                                raise FieldEmpty()
                            if '+' not in tel or ' ' in tel:
                                raise TeleNoFormatError()
                            tel = tel.replace('+', '')
                            input_list = [i for i in tel]
                            if len(input_list) != 12 and len(input_list) != 13 and len(input_list) != 14 and len(
                                    input_list) != 15 and len(input_list) != 16 and len(input_list) != 17 and len(input_list) != 18:
                                correct_length = '12 to 18'
                                raise IncorrectInputLength(correct_length)
                            question_num = 11

                    except nhsNotExists:
                        error = nhsNotExists()
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
                    except EmailInvalid:
                        error = EmailInvalid(emails)
                        print(error)
                    except TeleNoFormatError:
                        error = TeleNoFormatError()
                        print(error)
                    except ValueError:
                        print("< Please provide a numerical input >")
                    else:
                        self.c.execute("""UPDATE PatientDetail SET patientEmail = ?, firstName = ?, lastName = ?, dateOfBirth = ?
                        , gender = ?, addressLine1 = ?, addressLine2 = ?, postcode = ?,
                        telephoneNumber = ? WHERE nhsNumber = ?""",
                        (emails, firstn, lastnm, dateOfBirth, gender, addl1, addl2, postcode, tel, nhsnum))
                        self.connection.commit()
                        print("Succesfully updated entire patient record")
                        return masterback

    def delpatdet(self):
        delback = 0
        while delback == 0:
            try:
                print("********************************************")
                nhsnum = input("Enter patient nhs number (press 0 to go back): ")
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhsnum,))
                nhsq = self.c.fetchall()
                if nhsnum == "0":
                    delback = 1
                    break
                elif not nhsnum:
                    raise FieldEmpty
                elif len(nhsq) < 1:
                    raise nhsNotExists
            except nhsNotExists:
                error = nhsNotExists()
                print(error)
            except FieldEmpty:
                error = FieldEmpty()
                print(error)

            else:
                self.c.execute("""DELETE FROM PatientDetail WHERE nhsNumber = ?""", (nhsnum,))
                self.connection.commit()
                print("Successfully deleted patient record")
                delback = 1


    def manIndDet(self):
        masterback = 0
        while masterback == 0:
            try:
                print("********************************************")
                nhsnum = input("Enter patient nhs number (press 0 to go back): ")
                self.c.execute("SELECT * FROM PatientDetail WHERE nhsNumber = ?", (nhsnum,))
                nhsq = self.c.fetchall()
                if nhsnum == "0":
                    masterback = 1
                    break
                if not nhsnum:
                    raise FieldEmpty
                elif len(nhsq) < 1:
                    raise nhsNotExists
            except nhsNotExists:
                error = nhsNotExists()
                print(error)
            except FieldEmpty:
                error = FieldEmpty()
                print(error)
            else:
                Cagain = 0
                while Cagain == 0:
                    print("********************************************")
                    print("Choose [1] to go back to update patient details menu")
                    print("Choose [2] to update email")
                    print("Choose [3] to update first name")
                    print("Choose [4] to update last name")
                    print("Choose [5] to update date of birth")
                    print("Choose [6] to update gender")
                    print("Choose [7] to update address line 1")
                    print("Choose [8] to update address line 2")
                    print("Choose [9] to update post code")
                    print("Choose [10] to update telephone number")
                    print("********************************************")
                    try:
                        print("Press [0] to re-enter NHS number")
                        detinp = input("Choose which detail to change: ")
                        if detinp == '0':
                            Cagain = 1
                            break
                        elif detinp == '1':
                            masterback = 1
                            break
                        elif detinp.isdigit() == False:
                            raise IntegerError
                        indetinp = int(detinp)
                        if indetinp > 10:
                            raise IntegerError
                        elif not indetinp:
                            raise FieldEmpty
                    except FieldEmpty:
                            error = FieldEmpty()
                            print(error)
                    except IntegerError:
                            error = IntegerError()
                            print(error)
                    else:
                        print("********************************************")
                        print("Press [0] to re-enter NHS number")
                        print("Press [1] to go back to options")
                        if indetinp == 2:
                            back = 0
                            while back == 0:
                                try:
                                    CEmail = input("New email: ")
                                    self.c.execute("SELECT * FROM PatientDetail WHERE patientEmail = ?", (CEmail,))
                                    emailCheck = self.c.fetchall()
                                    if CEmail == '0':
                                        Cagain = 1
                                        break
                                    elif CEmail == '1':
                                        back = 0
                                        break
                                    elif len(emailCheck) > 0:
                                        raise EmailInUse
                                    elif "@" not in CEmail or ".com" not in CEmail:
                                        raise EmailInvalid(CEmail)
                                    elif not CEmail:
                                        raise FieldEmpty
                                except EmailInUse:
                                    error = EmailInUse()
                                    print(error)
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                except EmailInvalid:
                                    error = EmailInvalid(CEmail)
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET patientEmail = ? WHERE nhsNumber = ?""", (CEmail, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed email")
                                    back = 1

                        elif indetinp == 3:
                            back2 = 0
                            while back2 == 0:
                                try:
                                    Cfn = input("New first name: ")
                                    if Cfn == '0':
                                        Cagain = 1
                                        break
                                    elif Cfn == '1':
                                        back2 = 1
                                        break
                                    elif not Cfn:
                                        raise FieldEmpty
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET firstName = ? WHERE nhsNumber = ?""", (Cfn, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed first name")
                                    back2 = 1

                        elif indetinp == 4:
                            back3 = 0
                            while back3 == 0:
                                try:
                                    Cln = input("New last name: ")
                                    if Cln == '0':
                                        Cagain = 1
                                        break
                                    elif Cln == '1':
                                        back3 = 1
                                        break
                                    elif not Cln:
                                        raise FieldEmpty
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET lastName = ? WHERE nhsNumber = ?""", (Cln, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed last name")
                                    back3 = 1

                        elif indetinp == 5:
                            back4 = 0
                            while back4 == 0:
                                try:
                                    dateOfBirth = (input("New date of birth as YYYY-MM-DD: "))
                                    if dateOfBirth == '0':
                                        Cagain = 1
                                        break
                                    elif dateOfBirth == '1':
                                        back4 = 1
                                        break
                                    elif not dateOfBirth:
                                        raise FieldEmpty()
                                    elif len(dateOfBirth) != 10:
                                        correct_length = 10
                                        raise IncorrectInputLength(10)
                                    elif dateOfBirth[4] != '-' or dateOfBirth[7] != '-':
                                        raise DateFormatError
                                    day = int(dateOfBirth[8:10])
                                    month = int(dateOfBirth[5:7])
                                    year = int(dateOfBirth[0:4])
                                    if month == 9 or month == 4 or month == 6 or month == 11:
                                        if day > 30:
                                            raise DateInvalidError
                                    elif month == 2:
                                        if year % 4 != 0:
                                            if day > 28:
                                                raise DateInvalidError
                                        elif year % 4 == 0:
                                            if day > 29:
                                                raise DateInvalidError
                                    else:
                                        if day > 31:
                                            raise DateInvalidError
                                    if month > 12:
                                        raise DateInvalidError

                                    # input_list = [int(i) for i in str(dateOfBirth)]
                                    date_entered = date(year, month, day)
                                    date_today = date.today()
                                    if date_entered > date_today:
                                        raise DateInFutureError
                                    dateOfBirth = uf.tounixtime(date_entered)
                                    print(dateOfBirth)
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                except IncorrectInputLength:
                                    error = IncorrectInputLength(correct_length)
                                    print(error)
                                except DateFormatError:
                                    error = DateFormatError()
                                    print(error)
                                except DateInvalidError:
                                    error = DateInvalidError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET dateOfBirth = ? WHERE nhsNumber = ?""", (dateOfBirth, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed date of birth")
                                    back4 = 1

                        elif indetinp == 6:
                            back6 = 0
                            while back6 == 0:
                                try:
                                    Cgen = input("New gender (enter male/female/non-binary/prefer not to say): ")
                                    if Cgen == '0':
                                        Cagain = 1
                                        break
                                    elif Cgen == '1':
                                        back6 = 1
                                        break
                                    elif not Cgen:
                                        raise FieldEmpty()
                                    elif Cgen != "male" and Cgen != "female" and Cgen != "non-binary" and Cgen != "prefer not to say":
                                        raise GenderError()
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                except GenderError:
                                    error = GenderError()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET gender = ? WHERE nhsNumber = ?""",
                                                   (Cgen, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed gender")
                                    back6 = 1

                        elif indetinp == 7:
                            back7 = 0
                            while back7 == 0:
                                try:
                                    Cad1 = input("New address line 1: ")
                                    if Cad1 == '0':
                                        Cagain = 1
                                        break
                                    elif Cad1 == '1':
                                        back7 = 1
                                        break
                                    elif not Cad1:
                                        raise FieldEmpty()
                                    elif any(chr.isdigit() for chr in Cad1) == False:
                                        raise InvalidAdd
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                except InvalidAdd:
                                    error = InvalidAdd()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET addressLine1 = ? WHERE nhsNumber = ?""",
                                                   (Cad1, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed address line 1")
                                    back7 = 1

                        elif indetinp == 8:
                            back8 = 0
                            while back8 == 0:
                                try:
                                    Cad2 = input("new address line 2: ")
                                    if Cad2 == '0':
                                        Cagain = 1
                                        break
                                    elif Cad2 == '1':
                                        back8 = 1
                                        break
                                    elif not Cad2:
                                        raise FieldEmpty()
                                    elif any(chr.isdigit() for chr in Cad2) == False:
                                        raise InvalidAdd
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                except InvalidAdd:
                                    error = InvalidAdd()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET addressLine2 = ? WHERE nhsNumber = ?""",
                                                   (Cad2, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed address line 2")
                                    back8 = 1

                        elif indetinp == 9:
                            back9 = 0
                            while back9 == 0:
                                try:
                                    Cpost = input("New postcode: ")
                                    if Cpost == '0':
                                        Cagain = 1
                                        break
                                    elif Cpost == '1':
                                        back9 = 1
                                        break
                                    elif not Cpost:
                                        raise FieldEmpty()
                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                else:
                                    self.c.execute("""UPDATE PatientDetail SET postcode = ? WHERE nhsNumber = ?""",
                                                   (Cpost, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed post code")
                                    back9 = 1

                        elif indetinp == 10:
                            back10 = 0
                            while back10 == 0:
                                try:
                                    Ctel = (
                                        input("Telephone number (no spaces, with country code. E.g. +4471234123123): "))
                                    if Ctel == '0':
                                        Cagain = 1
                                        break
                                    elif Ctel == '1':
                                        back10 = 1
                                        break
                                    elif not Ctel:
                                        raise FieldEmpty()
                                    if '+' not in Ctel or ' ' in Ctel:
                                        raise TeleNoFormatError()
                                    Ctel = Ctel.replace('+', '')
                                    input_list = [i for i in Ctel]
                                    if len(input_list) != 12 and len(input_list) != 13 and len(
                                            input_list) != 14 and len(
                                            input_list) != 15 and len(input_list) != 16 and len(
                                        input_list) != 17 and len(
                                        input_list) != 18:
                                        correct_length = '12 to 18'
                                        raise IncorrectInputLength(correct_length)

                                except FieldEmpty:
                                    error = FieldEmpty()
                                    print(error)
                                except IncorrectInputLength:
                                    error = IncorrectInputLength(correct_length)
                                    print(error)
                                except IntegerError:
                                    error = IntegerError()
                                    print(error)
                                except TeleNoFormatError:
                                    error = TeleNoFormatError()
                                    print(error)
                                else:
                                    self.c.execute(
                                        """UPDATE PatientDetail SET telephoneNumber = ? WHERE nhsNumber = ?""",
                                        (Ctel, nhsnum))
                                    self.connection.commit()
                                    print("Successfully changed telephone number")
                                    back10 = 1

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

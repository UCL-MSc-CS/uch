import sqlite3,time

class gpsFunctions():

    def login():
        while True:
            email = input("Please enter your email address: ")
            password = input("Please enter your password: ")

            with sqlite3.connect(r'/Users/ao331/PycharmProjects/uch/UCH.db') as db:
                c = db.cursor()

            find_doctor = ("SELECT * FROM Doctors WHERE email =? AND password =?")

            # avoid using %s as this is vulnerable to injection attacks.
            c.execute(find_doctor, [(email), (password)])
            results = c.fetchall()

            if results:
                for i in results:
                    print("Welcome " + i[2])
                return ("exit")


            else:
                print("Email and password not recognised")
                again = input("Do you want to try again?(y/n)")
                if again.lower() == "n":
                    print("Goodbye")
                    time.sleep(1)
                    return("exit")

    def __init__(self):                              # whenever you close the connection, you will have to
        self.connection = sql.connect('UCH.db')      # create a new adminFunctions() object to re-open
        self.c = self.connection.cursor()            # the connection, so that __init__ is called.

    def check_appointments(self):
        self.c.execute("""SELECT COUNT(patientID) FROM appointments WHERE registrationConfirm = 'N' """)
        items = self.c.fetchall()
        count = items[0][0]
        print("You have %d patient appointments to confirm" % count)

    def confirm_appointments(self):
        self.c.execute("""SELECT * FROM appointments WHERE registrationConfirm = 'N'""")
        items = self.c.fetchall()
        for i in items:
            print(i)
            change = input("Do you want to confirm this appointment?: (Y/N)")
            if change == 'Y':
                pass
                # key = ("Type in the practitioner's email: ")
                # c.execute("""UPDATE patient_details SET registrationConfirm = 'Y' WHERE email = '?' """, key)



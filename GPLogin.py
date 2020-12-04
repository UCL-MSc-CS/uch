import sqlite3,time

def login():
    while True:
        email = input("Please enter your email address: ")
        password = input("Please enter your password: ")

        with sqlite3.connect("Database/GPs.db") as db:
            c = db.cursor()

        find_doctor = ("SELECT * FROM Doctors WHERE email =? AND password =?")

        # avoid using %s as this is vulnerable to injection attacks.
        c.execute(find_doctor,[(email),(password)])
        results = c.fetchall()

        if results:
            for i in results:
                print("Welcome "+i[2])
            return("exit")


        else:
            print("Email and password not recognised")
            again = input("Do you want to try again?(y/n)")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                return("exit")
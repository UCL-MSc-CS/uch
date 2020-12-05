import sqlite3 as sql
import time

def login(gpEmail):
    while True:
        email = input("Please enter your email address: ")
        password = input("Please enter your password: ")

        with sql.connect("../UCH.db") as db:
            c = db.cursor()

        find_doctor = ("SELECT * FROM GP WHERE gpEmail =? AND password =?")

        # avoid using %s as this is vulnerable to injection attacks.
        c.execute(find_doctor, [(email), (password)])
        results = c.fetchall()

        if results:
            for i in results:
                print("Welcome Doctor " + i[2] + " " + i[3])
                gpEmail.append(email)
            return("exit")

        else:
            print("Email and password not recognised")
            again = input("Do you want to try again?(y/n)")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                return("exit")


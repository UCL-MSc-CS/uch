import sqlite3 as sql
import time

def login(gpEmail):
    while True:
        email = input("Email (press 0 to go back): ")
        if email == '0':
            return ("exit")
        password = input("Password: ")

        db = sql.connect("UCH.db")
        c = db.cursor()
        find_doctor = ("SELECT * FROM GP WHERE gpEmail =? AND password =?")
        # avoid using %s as this is vulnerable to injection attacks.
        c.execute(find_doctor, [(email), (password)])
        db.commit()
        results = c.fetchall()

        if results:
            for i in results:
                print("Welcome Doctor " + i[2] + " " + i[3])
                gpEmail.append(email)
            db.close()
            return("exit")

        else:
            print("\t<Email and password not recognised>")
            again = input("Would you like to try again? (Y/N):")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                db.close()
                return("exit")
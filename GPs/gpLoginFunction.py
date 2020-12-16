import sqlite3 as sql
import time

def login(gpEmail):
    while True:
        email = input("Email (press 0 to go back): ")
        if email == '0':
            return ("exitGPLogin")
        db = sql.connect("UCH.db")
        c = db.cursor()
        find_email = ("SELECT * FROM GP WHERE gpEmail =?")
        c.execute(find_email, [email])
        db.commit()
        results = c.fetchall()
        if not results:
            print("Sorry, this email does not exist.")
        else:
            password = results[0][1]
            break

    while True:
        inputPassword = input("Password (press 0 to go back): ")
        if inputPassword == '0':
            return ("exitGPLogin")
        if inputPassword != password:
            print("Sorry, you have entered the incorrect password.")
        else:
            gpEmail.append(email)
            db.close()
            break
    print("\nWelcome Doctor " + results[0][2] + " " + results[0][3])

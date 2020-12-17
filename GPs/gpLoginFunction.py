import sqlite3 as sql
import time

def login():

    print("\n--------------------------------------------")
    print("\t Doctor Login")
    print("--------------------------------------------\n")

    while True:
        email = input("Email (press 0 to exit): ")
        if email == '0':
            print("Returning to main menu.....\n\n")
            return "exitGPLogin",''
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
        inputPassword = input("Password (press 0 to exit): ")
        if inputPassword == '0':
            print("Returning to main menu.....\n\n")
            db.close()
            return "exitGPLogin",''
        if inputPassword != password:
            print("Sorry, you have entered the incorrect password.")
        else:
            db.close()
            doctorname = results[0][2] + " " + results[0][3]
            return email,doctorname

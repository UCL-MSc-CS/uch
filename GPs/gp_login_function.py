import sqlite3 as sql

def gp_login():

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
        find_inactive_email = ("SELECT * FROM GP WHERE gpEmail =? AND active = 0")
        c.execute(find_inactive_email, [email])
        db.commit()
        inactiveresults = c.fetchall()
        if not results:
            print("\n\t< Sorry, this email does not exist >\n")
        elif inactiveresults:
            print("\n\t< This account has been deactivated. Please speak to an administrator to reactivate >\n")
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
            print("\n\t< Sorry, you have entered the incorrect password >\n")
        else:
            db.close()
            doctorname = results[0][2] + " " + results[0][3]
            return email,doctorname

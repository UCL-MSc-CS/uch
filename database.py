import sqlite3

""" This will function as our main database script. Rather than making large changes to this file, 
set up your own database script to make test changes to, and implement them here when they are 
finalised. If you want to test out queries and test out features with dummy data, do this in your
own scripts too for the time being. """

connection = sqlite3.connect('UCH.db')
# parts of sqlite queries are often case sensistive, be mindful of this.
# sqlite keeps things simple and only has 5 datatypes you can choose from:
# null, integer, real, text, blob
# (real is a decimal number)
# keep all attribute names in camelCase, and all table names singular with the
# first letter of each word capitalised e.g. Doctor, PatientDetail.

c = connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Doctor(
                    email text PRIMARY KEY,
                    firstName text,
                    lastName text,
                    dateOfBirth integer,
                    speciality text,
                    telephoneNumber integer,
                    gender text,
                    active text)
                    """)
connection.commit()


c.execute("""CREATE TABLE IF NOT EXISTS PatientDetail (
                    patientID integer PRIMARY KEY,
                    firstName text,
                    lastName text,
                    dateOfBirth text,
                    age integer,
                    gender text,
                    addressLine1 text,
                    addressLine2 text,
                    postcode text,
                    telephoneNumber integer,
                    email text,
                    registrationConfirm text)""")
connection.commit()

c.execute(""" CREATE TABLE IF NOT EXISTS Appointment (
                appointmentID INTEGER PRIMARY KEY,
                patientName DATATYPE text,
                date DATATYPE text,
                time DATATYPE text,
                gp DATATYPE text,
                gpGender DATATYPE text,
                bookedStatus DATATYPE text,
                checkIn DATATYPE text DEFAULT NULL,
                checkOut DATATYPE text DEFAULT NULL
                )""")

times = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
        '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30'
         ]

dates = ['01/01/2021', '02/01/2021', '03/01/2021', '04/01/2021', '05/01/2021', '06/01/2021',
         '07/01/2021', '08/01/2021', '09/01/2021', '10/01/2021', '11/01/2021', '12/01/2021',
         '13/01/2021', '14/01/2021', '15/01/2021', '16/01/2021', '17/01/2021', '18/01/2021',         '19/01/2021', '20/01/2021', '21/01/2021', '22/01/2021', '23/01/2021', '24/01/2021',
          '25/01/2021', '26/01/2021', '27/01/2021', '28/01/2021', '29/01/2021', '30/01/2021',
         '31/01/2021'
         ]

patientName = ''
gp = 'Dr Shepherd'
gpGender = 'M'
bookedStatus = 'Available'

for date in dates:
    for time in times:        c.execute("INSERT INTO Appointment VALUES (null, ?, ?, ?, ?, ?, ?, null, null)", (patientName, date, time, gp,
                                                                                        gpGender, bookedStatus))
c.execute("SELECT * FROM Appointment")
print(c.fetchall())

connection.commit()

c.execute("""SELECT * FROM Doctor""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

c.execute("""SELECT * FROM PatientDetail""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

connection.close()
#---------------------------------------------------------------------------
# ---- Some example queries: ----
# Creating a table:
# c.execute(""" CREATE TABLE customers(
#                 first_name text,
#                 last_name text,
#                 email text)""")

# Inserting many values into a table:
# many_customers = [
#                 ('matt1','sh','m.shorvon@gmail.com'),
#                 ('matt2','sh','m.shorvon@gmail.com'),
#                 ('matt3','sh','m.shorvon@gmail.com'),
#                 ]
#
# c.executemany("INSERT INTO customers VALUES (?,?,?)", many_customers)

# Viewing a table with fetchall and each row printed on a separate line:
# c.execute("SELECT rowID, * FROM customers")
# items = c.fetchall()
# for i in items:
#     print(i)
# connection.commit()
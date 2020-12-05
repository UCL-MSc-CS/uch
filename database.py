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
#create GP table
c.execute("""CREATE TABLE IF NOT EXISTS GP (
                    gpEmail text UNIQUE,
                    password text,
                    firstName text,
                    lastName text,
                    gender text,
                    dateOfBirth integer,
                    addressLine1 text,
                    addressLine2 text,
                    telephoneNumber text,
                    department text,
                    active text)""")
connection.commit()

#create patients table
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

#create the appointments table
c.execute("""CREATE TABLE IF NOT EXISTS Appointment (
                    appointmentID integer primary key,
                    gpEmail text,
                    gpLastName text,
                    patientEmail text,
                    start integer,
                    end integer,
                    reason text,
                    appointmentStatus text,
                    dateRequested integer,
                    patientComplaints text,
                    doctorFindings text,
                    diagnosis text,
                    furtherInspections text,
                    doctorAdvice text,
                    checkIn integer NULL,
                    checkOut integer NULL)""")
connection.commit()

c.execute("""SELECT * FROM GP""")
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
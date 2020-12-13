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
#create Appointment table

c.execute("""CREATE TABLE IF NOT EXISTS Admin(
                    username text PRIMARY KEY,
                    password text
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Admin VALUES(
            'Matthew',
            '1234'
)""")
connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS PatientDetail (
                    patientEmail text PRIMARY KEY ,
                    firstName text,
                    lastName text,
                    dateOfBirth text,
                    age integer, 
                    gender text,
                    addressLine1 text,
                    addressLine2 text,
                    postcode text,
                    telephoneNumber integer,
                    password text,
                    registrationConfirm text,
                    loggedIn text
)""")
connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS medicalHistory(
            patientEmail DATATYPE text,
            Status DATATYPE text,
            DTap DATATYPE text,
            HepC DATATYPE text,
            HepB DATATYPE text,
            Measles DATATYPE text,
            Mumps DATATYPE text,
            Rubella DATATYPE text,
            Varicella DATATYPE text,
            PRIMARY KEY (patientEmail, Status)
            )""")
connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS questionnaireTable(
            patientEmail text PRIMARY KEY,
            exercise DATATYPE text,
            exerciseType DATATYPE text,
            exerciseFrequency DATATYPE integer,
            exerciseDuration DATATYPE integer,
            goal DATATYPE text,
            height DATATYPE real,
            weight DATATYPE real,
            bmi DATATYPE real,
            smoking DATATYPE text,
            drugs DATATYPE text,
            drugType DATATYPE text,
            alcohol DATATYPE text,
            alcoholUnit DATATYPE text,
            meat DATATYPE text,
            diet DATATYPE text,
            caffeine DATATYPE text
            )""")
connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS cancer(
                    patientEmail DATATYPE text,
                    cancerRelation DATATYPE text,
                    cancerType DATATYPE text,
                    cancerAge DATATYPE text,
                    PRIMARY KEY (patientEmail, cancerRelation)
                    )""")
connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS GP(
                    gpEmail text PRIMARY KEY ,
                    password text,
                    firstName text,
                    lastName text,
                    gender text,
                    dateOfBirth text,
                    addressLine1 text,
                    addressLine2 text,
                    telephoneNumber integer,
                    department text,
                    active text
)""")
connection.commit()


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

c.execute("""CREATE TABLE IF NOT EXISTS Medecine(
                    medicineID integer PRIMARY KEY,
                    medicineName text,
                    medicineCompany text,
                    drug text,
                    medicineType text
)""")
connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS Prescription(
                    AppointmentID integer PRIMARY KEY,
                    medicineID integer,
                    dosage text,
                    frequency text,
                    duration text
)""")

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

c.execute("""INSERT OR IGNORE INTO PatientDetail VALUES (
                    'm.shorvon@gmail.com',
                    'Matthew',
                    'Shorvon',
                    '16071998',
                    22,
                    'male',
                    '10 downing street',
                    'London',
                    'idk',
                    07758221088,
                    'passwrrrdd',
                    'N',
                    'N')""")
connection.commit()

c.execute("""INSERT OR IGNORE INTO GP VALUES(
            'matthew.shorvon@ucl.ac.uk',
            'another passwrrrdd',
            'Matthew',
            'Shorvon',
            'male',
            '160798',
            '10 Beverly Hills',
            'LA',
            '07758221088',
            'Plastic Surgery',
            'Y')""")
connection.commit()

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
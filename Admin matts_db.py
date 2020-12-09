import sqlite3

""" Matt's db script for messing around in. """

connection = sqlite3.connect('UCH.db')
# parts of sqlite queries are often case sensistive, be mindful of this.
# sqlite keeps things simple and only has 5 datatypes you can choose from:
# null, integer, real, text, blob
# (real is a decimal number)
# keep all attribute names in camelCase, and all table names singular with the
# first letter of each word capitalised e.g. Doctor, PatientDetail.

c = connection.cursor()
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

c.execute("""CREATE TABLE IF NOT EXISTS Appointment (
                    appointmentID integer PRIMARY KEY,
                    patientEmail text,
                    gpEmail text,
                    checkIn text,
                    checkOut text,
                    date text,
                    time text,
                    room text,
                    bookedStatus text,
                    patientComplaints text,
                    doctorFindings text, 
                    diagnosis text,
                    furtherInspections text,
                    reason text,
                    dateRequested text, 
                    appointmentStatus text, 
                    start text, 
                    end text, 
                    gpLastName text, 
                    doctorAdvice text, 
                    appointmentConfirmed text, 
                    prescriptionID integer)""")
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

c.execute("""CREATE TABLE IF NOT EXISTS MedicalHistory (
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

c.execute("""CREATE TABLE IF NOT EXISTS PatientQuestionaire (
                    questionnaireID integer PRIMARY KEY ,
                    height integer,
                    weight integer,
                    bmi text,
                    smoking text,
                    alcohol text,
                    diet text,
                    drugs text,
                    exercise text,
                    exerciseType text,
                    exerciseFrequency text,
                    exerciseDuration text,
                    goal text
)""")
connection.commit()


c.execute("""CREATE TABLE IF NOT EXISTS FamilyMedicalHistory(
                    familyMedHistoryID integer PRIMARY KEY,
                    medHistoryID integer,
                    dTap text,
                    hepC text,
                    hepB text,
                    measles text,
                    mumps text,
                    rubella text,
                    varicella text
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Cancer(
                    patientEmail text PRIMARY KEY ,
                    cancer text,
                    cancerType text,
                    cancerAge integer,
                    cancerFamily text,
                    cancerTypeFamily text,
                    cancerAgeFamily text
)""")

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

c.execute("""INSERT OR IGNORE INTO PatientDetail VALUES (
                    'm.shorvon2@gmail.com',
                    'Matthew',
                    'Shorvon the 2nd',
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

c.execute("""INSERT OR IGNORE INTO PatientDetail VALUES (
                    'm.shorvon3@gmail.com',
                    'Matthew',
                    'Shorvon the 3rd',
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

c.execute("""INSERT OR IGNORE INTO PatientDetail VALUES (
                    'm.shorvon4@gmail.com',
                    'Matthew',
                    'Shorvon the 4th',
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

c.execute("""INSERT OR IGNORE INTO PatientDetail VALUES (
                    'BoJo@gmail.gov',
                    'Boris',
                    'Jhn',
                    '16071998',
                    22,
                    'male',
                    '10 downing street',
                    'London',
                    'idk',
                    07758221088,
                    'passwrrdrd',
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

c.execute("""SELECT rowid,* FROM GP""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

c.execute("""SELECT rowid,* FROM Admin""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

c.execute("""SELECT rowid,* FROM PatientDetail""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

connection.close()

# Some example queries:
# c.execute(""" CREATE TABLE customers(
#                 first_name text,
#                 last_name text,
#                 email text)""")

# many_customers = [
#                 ('matt1','sh','m.shorvon@gmail.com'),
#                 ('matt2','sh','m.shorvon@gmail.com'),
#                 ('matt3','sh','m.shorvon@gmail.com'),
#                 ]
#
# c.executemany("INSERT INTO customers VALUES (?,?,?)", many_customers)
# c.execute("SELECT rowID, * FROM customers")
# items = c.fetchall()
# for i in items:
#     print(i)
# connection.commit()

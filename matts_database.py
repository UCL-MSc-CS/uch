import sqlite3
import pandas as pd
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

# patientEmail is not UNIQUE/PRIMARY KEY ..
c.execute("""CREATE TABLE IF NOT EXISTS PatientDetail (
                    nhsNumber DATATYPE INTEGER PRIMARY KEY,
                    patientEmail DATATYPE TEXT,
                    firstName DATATYPE TEXT,
                    lastName DATATYPE TEXT,
                    dateOfBirth DATATYPE TEXT,
                    gender DATATYPE TEXT,
                    addressLine1 DATATYPE TEXT,
                    addressLine2 DATATYPE TEXT,
                    postcode DATATYPE TEXT,
                    telephoneNumber DATATYPE TEXT,
                    password DATATYPE TEXT,
                    registrationConfirm DATATYPE INTEGER
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
            nhsNumber DATATYPE INTEGER PRIMARY KEY,
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
                    nhsNumber integer,
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

c.execute("DROP TABLE IF EXISTS Medicine")
connection.commit()

#create medicine table
c.execute("""CREATE TABLE IF NOT EXISTS Medicine (
                    medicineID integer primary key,
                    medicineName text,
                    medicineType text,
                    dosageType text,
                    drugRoute text,
                    company text,
                    drug text,
                    dosages text,
                    activeIngredientUnit text,
                    pharmacologicalClasses text,
                    category text)""")
connection.commit()

c.execute("""
            SELECT COUNT(medicineID)
            FROM Medicine
""")
connection.commit()

numrows = c.fetchone()[0]

if numrows < 1:
    try:
        medicines = pd.read_csv("medicinedata.txt",delimiter='\t',header=0,encoding='CP850')
    except:
        medicines = pd.read_csv("medicinedata.txt",delimiter='\t',header=0,encoding='ANSI')

    medicines.to_sql("Medicine",connection,if_exists='append',index=False)

    pass



c.execute("""CREATE TABLE IF NOT EXISTS Prescription (
                    appointmentID integer PRIMARY KEY,
                    medicineID integer,
                    dosage text,
                    dosageMultiplier integer,
                    furtherInformation text
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
                    1234567890,
                    'm.shorvon@gmail.com',
                    'Matthew',
                    'Shorvon',
                    900543600,
                    'Male',
                    '10 Downing Street',
                    'London',
                    'SW1A 0AA',
                    07758221088,
                    '1234',
                    1)""")
connection.commit()

c.execute("""INSERT OR IGNORE INTO GP VALUES(
            'matthew.shorvon@ucl.ac.uk',
            '1234',
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

c.execute("SELECT * FROM PatientDetail WHERE registrationConfirm = 0")
items = c.fetchall()
for i in items:
    print(i)

c.execute("""UPDATE PatientDetail SET registrationConfirm = 1 WHERE patientEmail = 'm.shorvon@gmail.com' """)
connection.commit()

c.execute("SELECT * FROM PatientDetail WHERE registrationConfirm = 1")
items = c.fetchall()
for i in items:
    print(i)

c.execute("""UPDATE PatientDetail SET registrationConfirm = 0 WHERE patientEmail = 'm.shorvon@gmail.com' """)
connection.commit()

c.execute("SELECT * FROM PatientDetail WHERE registrationConfirm = 0")
items = c.fetchall()
for i in items:
    print(i)

# c.execute("""CREATE TABLE IF NOT EXISTS Appointment (
#                     appointmentID integer primary key,
#                     gpEmail text,
#                     gpLastName text,
#                     nhsNumber integer,
#                     start integer,
#                     end integer,
#                     reason text,
#                     appointmentStatus text,
#                     dateRequested integer,
#                     patientComplaints text,
#                     doctorFindings text,
#                     diagnosis text,
#                     furtherInspections text,
#                     doctorAdvice text,
#                     checkIn integer NULL,
#                     checkOut integer NULL)""")

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    12,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-14",
                    'did too much ket',
                    'he did indeed do too much ket',
                    'Ket Overdose',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    NULL,
                    NULL
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    13,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-13",
                    'did too much coke',
                    'he did indeed do too much coke',
                    'coke Overdose',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    14,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-16",
                    'did too much molly',
                    'he did indeed do too much molly',
                    'Molly Overdose',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    15,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-11",
                    'did too much acid',
                    'he did indeed do too much acid',
                    'Acid Overdose',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    16,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-18",
                    'did too much shisha',
                    'wtf is wrong with this guy how do you OD on shisha',
                    'Hes dumb af',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    17,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-19",
                    'did too much tea',
                    'wtf is wrong with this guy how do you OD on tea',
                    'Tea Overdose lol',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    18,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    '2020-12-20',
                    'Im really dumb',
                    'Hes dumb af',
                    'Hes just dumb asf i swear',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    19,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-14",
                    'did too much shisha',
                    'wtf is wrong with this guy how do you OD on shisha',
                    'ODd on the meds I prescribed him to be less dumb ',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute(""" INSERT OR IGNORE INTO Appointment VALUES(
                    20,
                    'matthew.shorvon@ucl.ac.uk',
                    'Shorvon',
                    1234567890,
                    "15:00", 
                    "16:30",
                    'Appointment',
                    'confirmed',
                    "2020-12-21",
                    'did too much shisha',
                    'wtf is wrong with this guy how do you OD on shisha',
                    'hes too dumb to function',
                    'None',
                    'Should try some slighly more wholesome activities in his free time',
                    1,
                    1 
)""")
connection.commit()

c.execute("""SELECT dateRequested, diagnosis FROM Appointment WHERE nhsNumber = 1234567890""")
items = c.fetchall()
for i in items:
    print(i)


check_number = 11
c.execute("SELECT checkIn FROM Appointment WHERE appointmentID = ?", (check_number,))
items = c.fetchall()
print(items)
print(len(items))
print(len(items) != 0)

c.execute("""INSERT OR IGNORE INTO questionnaireTable VALUES(
            1234567890,
            '1',
            'justdance on the nintendo switch Xddd',
            7,
            300,
            'idk',
            1.8,
            75,
            23.15,
            '1',
            '1',
            'molly',
            '1',
            '3',
            '2',
            '5',
            '1'
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Prescription (
                    appointmentID integer PRIMARY KEY ,
                    medicineID integer,
                    dosage text,
                    dosageMultiplier integer,
                    furtherInformation text
)""")

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    12,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")
connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    13,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    14,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    15,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    16,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    17,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    18,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    19,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

c.execute("""INSERT OR IGNORE INTO Prescription VALUES(
                    20,
                    4124,
                    '2/day',
                    1,
                    'enjoy ;)' 
)""")

connection.commit()

# c.execute("""CREATE TABLE IF NOT EXISTS Medicine (
#                     medicineID integer primary key,
#                     medicineName text,
#                     medicineType text,
#                     dosageType text,
#                     drugRoute text,
#                     company text,
#                     drug text,
#                     dosages text,
#                     activeIngredientUnit text,
#                     pharmacologicalClasses text,
#                     category text)""")
# connection.commit()

# c.execute("""CREATE TABLE IF NOT EXISTS Prescription (
#                     appointmentID integer,
#                     medicineID integer,
#                     dosage text,
#                     dosageMultiplier integer,
#                     furtherInformation text
# )""")

# c.execute("""CREATE TABLE IF NOT EXISTS Appointment (
#                     appointmentID integer primary key,
#                     gpEmail text,
#                     gpLastName text,
#                     nhsNumber integer,
#                     start integer,
#                     end integer,
#                     reason text,
#                     appointmentStatus text,
#                     dateRequested integer,
#                     patientComplaints text,
#                     doctorFindings text,
#                     diagnosis text,
#                     furtherInspections text,
#                     doctorAdvice text,
#                     checkIn integer NULL,
#                     checkOut integer NULL)""")

# c.execute("""SELECT Medicine.medicineName, Prescription.dosage, Appointment.dateRequested
# FROM Medicine
# INNER JOIN Appointment ON Appointment.appointmentID = Prescription.appointmentID
# INNER JOIN Prescription ON Prescription.medicineID = Medicine.medicineID""")

c.execute("""SELECT Medicine.medicineName, Prescription.dosage, Appointment.dateRequested, Appointment.appointmentID
FROM Medicine, Prescription, Appointment
WHERE Appointment.appointmentID = Prescription.appointmentID
AND Medicine.medicineID = Prescription.medicineID
AND Appointment.nhsNumber = 1234567890""")


items = c.fetchall()
for i in items:
    print(i)

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
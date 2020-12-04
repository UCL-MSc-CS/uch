import sqlite3 as sql

conn = sql.connect('patient.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS PatientDetail (
                    patientID integer PRIMARY KEY,
                    firstName text,
                    lastName text,
                    email text,
                    password text,
                    loggedIn text)""")

c.execute('DROP TABLE IF EXISTS questionnaireTable')
c.execute("""CREATE TABLE IF NOT EXISTS questionnaireTable(
            PatientID INTEGER PRIMARY KEY,
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

c.execute("""CREATE TABLE IF NOT EXISTS medicalHistory(
            PatientID INTEGER PRIMARY KEY,
            DTap DATATYPE text,
            HepC DATATYPE text,
            HepB DATATYPE text,
            Measles DATATYPE text,
            Mumps DATATYPE text,
            Rubella DATATYPE text,
            Varicella DATATYPE text
            )""")

c.execute(""" CREATE TABLE IF NOT EXISTS GP (
                gpEmail text PRIMARY KEY,
                gpLastName DATATYPE text,
                gpGender DATATYPE text
                )""")

c.execute("INSERT INTO GP VALUES ('Shepherd@dr.com', 'Shepherd', 'M')")
c.execute("INSERT INTO GP VALUES ('Grey@dr.com', 'Grey', 'F' )")
c.execute("INSERT INTO GP VALUES ('Bailey@dr.com', 'Bailey', 'F' )")

c.execute(""" CREATE TABLE IF NOT EXISTS Appointment (
                appointmentID INTEGER PRIMARY KEY,
                patientEmail DATATYPE text,
                date DATATYPE text,
                time DATATYPE text,
                gpLastName DATATYPE text,
                bookedStatus DATATYPE text,
                checkIn DATATYPE text DEFAULT NULL,
                checkOut DATATYPE text DEFAULT NULL
                )""")

conn.commit()
conn.close()
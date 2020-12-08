import sqlite3 as sql

conn = sql.connect('patient.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS PatientDetail (
                    patientEmail DATATYPE TEXT,
                    firstName DATATYPE TEXT,
                    lastName DATATYPE TEXT,
                    dateOfBirth DATATYPE TEXT,
                    age DATATYPE INTEGER,
                    gender DATATYPE TEXT,
                    addressLine1 DATATYPE TEXT,
                    addressLine2 DATATYPE TEXT,
                    postcode DATATYPE TEXT,
                    telephoneNumber DATATYPE TEXT,
                    password DATATYPE TEXT,
                    loggedIn DATATYPE INTEGER,
                    registrationConfirm DATATYPE INTEGER)""")

c.execute('DROP TABLE IF EXISTS questionnaireTable')
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

c.execute("""CREATE TABLE IF NOT EXISTS cancer(
                    patientEmail DATATYPE text,
                    cancerRelation DATATYPE text,
                    cancerType DATATYPE text,
                    cancerAge DATATYPE text,
                    PRIMARY KEY (patientEmail, cancerRelation)
                    )""")

c.execute(""" CREATE TABLE IF NOT EXISTS GP (
                gpEmail text PRIMARY KEY,
                gpFirstName DATATYPE text,
                gpLastName DATATYPE text,
                gpGender DATATYPE text
                )""")

c.execute("INSERT INTO GP VALUES ('Shepherd@dr.com', 'Derek', 'Shepherd', 'M')")
c.execute("INSERT INTO GP VALUES ('Meredith@dr.com', 'Meredith', 'Grey', 'F' )")
c.execute("INSERT INTO GP VALUES ('Bailey@dr.com', 'Miranda', 'Bailey', 'F' )")
c.execute("INSERT INTO GP VALUES ('Julia@dr.com', 'Julia', 'Bailey', 'F' )")

c.execute("""CREATE TABLE IF NOT EXISTS Appointment (
                    appointmentId integer primary key,
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

conn.commit()
conn.close()
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

c.execute("INSERT INTO GP VALUES ('Shep@erd.com', 'Shepherd', 'M')")
c.execute("INSERT INTO GP VALUES ('Meridith@grey.com', 'Grey', 'F' )")
c.execute("INSERT INTO GP VALUES ('Bailey@dr.com', 'Bailey', 'F' )")

c.execute(""" CREATE TABLE IF NOT EXISTS Appointment (
                appointmentID INTEGER PRIMARY KEY,
                patientID INTEGER,
                date DATATYPE text,
                time DATATYPE text,
                gpLastName DATATYPE text,
                bookedStatus DATATYPE text,
                gpAvailability DATATYPE text,
                checkIn DATATYPE text DEFAULT NULL,
                checkOut DATATYPE text DEFAULT NULL
                )""")

times = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
        '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30'
         ]

dates = ['01/01/2021', '02/01/2021', '03/01/2021', '04/01/2021', '05/01/2021', '06/01/2021',
         '07/01/2021', '08/01/2021', '09/01/2021', '10/01/2021', '11/01/2021', '12/01/2021',
         '13/01/2021', '14/01/2021', '15/01/2021', '16/01/2021', '17/01/2021', '18/01/2021',
         '19/01/2021', '20/01/2021', '21/01/2021', '22/01/2021', '23/01/2021', '24/01/2021',
         '25/01/2021', '26/01/2021', '27/01/2021', '28/01/2021', '29/01/2021', '30/01/2021',
         '31/01/2021'
         ]

gp_list = ['Shepherd', 'Grey', 'Bailey']

patientID = ''
bookedStatus = 'Available'
gpAvailability = 'Available'

for date in dates:
    for time in times:
        for gpLastName in gp_list:
            c.execute("INSERT INTO Appointment VALUES (null, ?, ?, ?, ?, ?, ?, null, null)", (patientID, date, time,
                                                                                            gpLastName, bookedStatus,
                                                                                           gpAvailability))

conn.commit()
conn.close()
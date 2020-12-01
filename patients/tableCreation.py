import sqlite3 as sql

conn = sql.connect('medicalHistory.db')

c = conn.cursor()

c.execute("""CREATE TABLE medicalHistory(
            PatientID INTEGER PRIMARY KEY,
            DTap DATATYPE text,
            HepC DATATYPE text,
            HepB DATATYPE text,
            Measles DATATYPE text,
            Mumps DATATYPE text,
            Rubella DATATYPE text,
            Varicella DATATYPE text
            )""")


c.execute("SELECT * FROM medicalHistory")


conn.commit()
conn.close()
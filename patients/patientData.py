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
                    
c.execute("SELECT * FROM PatientDetail")
print(c.fetchall())

conn.commit()
conn.close()
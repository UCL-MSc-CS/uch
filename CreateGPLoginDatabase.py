import sqlite3

""" For now, this file will sort of be my (Andrew's) sandbox to experiment with the database (GP side)."""
conn = sqlite3.connect(r'/Users/ao331/PycharmProjects/uch/UCH.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Doctors(
                    email text PRIMARY KEY,
                    password text,
                    firstName text,
                    lastName text,
                    dateOfBirth integer,
                    department text,
                    telephoneNumber integer,
                    gender text,
                    active text);
                    """) # todo add addressLine1 and addressLine2
conn.commit()

c.execute("""
INSERT INTO Doctors(email, password, firstName, lastName, dateOfBirth, department, telephoneNumber, gender, active)
VALUES("test2@gmail.com","badpassword","Human","Being","01/01/01","A&E",12345678,"Prefer not to say","Yes")
""")

conn.commit()

c.execute("SELECT * FROM Doctors")
print(c.fetchall())
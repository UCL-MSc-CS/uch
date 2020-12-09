import sqlite3

""" For now, this file will sort of be my (Andrew's) sandbox to experiment with the database (GP side)."""
conn = sqlite3.connect(r'/Users/ao331/PycharmProjects/uch/UCH.db')
c = conn.cursor()


c.execute("""
INSERT INTO GP(gpEmail, password, firstName, lastName, gender, dateOfBirth, addressLine1, addressLine2, telephoneNumber, department, active)
VALUES("test@gmail.com","badpassword","Human","Being","m",0,"The Ghetto","Ratatata","99999","A&E","Yes")
""")



conn.commit()

c.execute("SELECT * FROM GP")
print(c.fetchall())
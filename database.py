import sqlite3

connection = sqlite3.connect('UCH.db')
# parts of sqlite queries are often case sensistive, be mindful of this. 
# sqlite keeps things simple and only has 5 datatypes you can choose from:
# null, integer, real, text, blob
# (real is a decimal number)
# keep all attribute names in camelCase, and all table names singular with the 
# first letter of each word capitalised e.g. Doctor, PatientDetail.

c = connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Doctor(
                    email text PRIMARY KEY,
                    firstName text,
                    lastName text,
                    dateOfBirth integer,
                    speciality text,
                    telephoneNumber integer,
                    gender text,
                    active text)
                    """)
connection.commit()
#
# c.execute("""ALTER TABLE doctors
#              ADD COLUMN telephoneNumber integer;""")
# # c.execute("""ALTER TABLE doctors
#              ADD COLUMN gender text;""")
# c.execute("""ALTER TABLE doctors
#              ADD COLUMN active text;""")
# connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS PatientDetail (
                    patientID integer PRIMARY KEY,
                    firstName text,
                    lastName text,
                    dateOfBirth text,
                    age integer,
                    gender text,
                    addressLine1 text,
                    addressLine2 text,
                    postcode text,
                    telephoneNumber integer,
                    email text,
                    registrationConfirm text)""")
connection.commit()

# c.execute("""INSERT INTO patient_details VALUES (
#                     50,
#                     'Matthew',
#                     'Shorvon',
#                     16071998,
#                     22,
#                     'male',
#                     '10 downing street',
#                     'London',
#                     'idk',
#                     07758221088,
#                     'm.shorvon@gmail.com',
#                     'N')""")
# connection.commit()
#
# c.execute("""INSERT INTO patient_details VALUES (
#                     2,
#                     'Matthew',
#                     'Shorvon the 2nd',
#                     16071998,
#                     22,
#                     'male',
#                     '10 downing street',
#                     'London',
#                     'idk',
#                     07758221088,
#                     'm.shorvon@gmail.com',
#                     'Y')""")
# connection.commit()
#
# c.execute("""INSERT INTO patient_details VALUES (
#                     3,
#                     'Matthew',
#                     'Shorvon the 3rd',
#                     16071998,
#                     22,
#                     'male',
#                     '10 downing street',
#                     'London',
#                     'idk',
#                     07758221088,
#                     'm.shorvon@gmail.com',
#                     'N')""")
# connection.commit()
#
# c.execute("""INSERT INTO patient_details VALUES (
#                     4,
#                     'Matthew',
#                     'Shorvon the 4th',
#                     16071998,
#                     22,
#                     'male',
#                     '10 downing street',
#                     'London',
#                     'idk',
#                     07758221088,
#                     'm.shorvon@gmail.com',
#                     'Y')""")
# connection.commit()

c.execute("""SELECT * FROM doctors""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

c.execute("""SELECT * FROM patient_details""")
items = c.fetchall()
for i in items:
    print(i)
connection.commit()
print(" ")

c.execute("""SELECT COUNT(patientID) FROM patient_details WHERE registrationConfirm = 'N' """)
items = c.fetchall() # items will be a list with a tuple with a single element in it, [(n,)]
count = items[0][0]  # this line gets n out of the tuple in the items list
print("You have %d patient registrations to confirm" % count)
connection.commit()

c.execute("""SELECT *
             FROM patient_details
             WHERE registrationConfirm = 'N'""")
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
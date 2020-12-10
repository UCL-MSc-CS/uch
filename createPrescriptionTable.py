import sqlite3
import pandas as pd

connection = sqlite3.connect('UCH.db')
c = connection.cursor()

c.execute("DROP TABLE IF EXISTS Prescription")
connection.commit()

#create prescription table
c.execute("""CREATE TABLE IF NOT EXISTS Prescription (
                    appointmentID integer,
                    medicineID integer,
                    dosage text,
                    dosageMultiplier integer,
                    furtherInformation text
)""")
connection.commit()

connection.close()
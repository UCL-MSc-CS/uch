import sqlite3
from pathlib import Path

path = str(Path(__file__).parent.absolute()) + "/UCLHospital.db"
conn = sqlite3.connect(path) #DO NOT add this file to Git!!!
cursor = conn.cursor()

#create the unavailability table

cursor.execute("""
CREATE TABLE DoctorTimetable (
gpId integer,
start integer,
end integer,
reason text,
Appointment text
)
""")

conn.commit()
conn.close()
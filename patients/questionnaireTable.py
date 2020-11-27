import sqlite3 as sql

conn = sql.connect('questionnaireTable.db')

c = conn.cursor()

# c.execute('DROP TABLE IF EXISTS questionnaireTable')
c.execute("""CREATE TABLE questionnaireTable(
            PatientID INTEGER PRIMARY KEY,
            exercise DATATYPE text,
            exerciseType DATATYPE text,
            exerciseFrequency DATATYPE integer,
            exerciseDuration DATATYPE integer,
            goal DATATYPE text,
            height DATATYPE real,
            weight DATATYPE real
            bmi DATATYPE real,
            smoking DATATYPE text,
            drugs DATATYPE text,
            drugType DATATYPE text,
            alcoholUnit DATATYPE text
            )""")
conn.commit()
conn.close()

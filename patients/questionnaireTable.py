import sqlite3 as sql

conn = sql.connect('questionnaireTable.db')

c = conn.cursor()

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
conn.commit()
conn.close()

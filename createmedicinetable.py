import sqlite3
import pandas as pd

connection = sqlite3.connect('UCH.db')
c = connection.cursor()

c.execute("DROP TABLE IF EXISTS Medicine")
connection.commit()

#create medicine table
c.execute("""CREATE TABLE IF NOT EXISTS Medicine (
                    medicineID integer primary key,
                    medicineName text,
                    medicineType text,
                    dosageType text,
                    drugRoute text,
                    company text,
                    drug text,
                    dosages text,
                    activeIngredientUnit text,
                    pharmacologicalClasses text,
                    category text)""")
connection.commit()

c.execute("""
            SELECT COUNT(medicineID)
            FROM Medicine
""")
connection.commit()

numrows = c.fetchone()[0]

if numrows < 1:
    medicines = pd.read_csv("medicinedata.txt",delimiter='\t',header=0,encoding='ANSI')
    medicines.to_sql("Medicine",connection,if_exists='append',index=False)
    pass

connection.close()

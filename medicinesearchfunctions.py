import sqlite3
from pathlib import Path


# connect to your database
def connecttodb():
    path = str(Path(__file__).parent.absolute()) + "/UCH.db"
    connection = sqlite3.connect(path)  # DO NOT add this file to Git!!!
    cursor = connection.cursor()
    conncursordict = {"connection": connection, "cursor": cursor}
    return conncursordict


# disconnect from your database
def closeconn(conn):
    conn.commit()
    conn.close()


"""
place all functions below in the following template....

def functionname(args):
    conn = connecttodb()

    *your code here.....*

    closeconn(conn["connection"])

"""


def alldosagetypes():
    conn = connecttodb()

    conn['cursor'].execute("""SELECT DISTINCT dosageType FROM Medicine ORDER BY dosageType asc""")
    results = conn['cursor'].fetchall()

    dosageTypes = []

    for result in results:
        dosageTypes.append(result[0])

    closeconn(conn["connection"])

    return dosageTypes

def allmedtypes():
    conn = connecttodb()

    conn['cursor'].execute("""SELECT DISTINCT medicineType FROM Medicine ORDER BY medicineType asc""")
    results = conn['cursor'].fetchall()

    medicineTypes = []

    for result in results:
        medicineTypes.append(result[0])

    closeconn(conn["connection"])

    return medicineTypes

def allcategories():
    conn = connecttodb()

    conn['cursor'].execute("""SELECT DISTINCT category FROM Medicine ORDER BY medicineType asc""")
    results = conn['cursor'].fetchall()

    categories = []

    for result in results:
        categories.append(result[0])

    closeconn(conn["connection"])

    return categories

# This searches for drugs
def search(medname,drugname,dosetype,medtype,category):
    conn = connecttodb()

    if medname:
        medname = "%" + medname + "%"
    if drugname:
        drugname = "%" + drugname + "%"

    valuearray = [medname, medtype, drugname, dosetype, category]

    for key, value in enumerate(valuearray):
        if not value:
            valuearray[key] = "%"

    values = tuple(valuearray)

    sql = """
            SELECT * FROM Medicine
            WHERE
                medicineName LIKE ? AND
                medicineType LIKE ? AND
                drug LIKE ? AND
                dosageType LIKE ? AND
                category LIKE ?
            LIMIT 30"""
    conn['cursor'].execute(sql,values)
    results = conn['cursor'].fetchall()

    closeconn(conn["connection"])
    return results

def addPrescription(prescription):
    conn = connecttodb()

    prescriptionTuple = tuple(prescription)
    print(prescriptionTuple)

    conn['cursor'].execute("""
        INSERT INTO
            Prescription
        VALUES
            (?, ?, ?, ?, ?)
        """, prescriptionTuple)

    closeconn(conn["connection"])




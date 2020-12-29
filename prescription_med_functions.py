import sqlite3
from pathlib import Path
import re


# connect to your database
def connect_to_db():
    path = str(Path(__file__).parent.absolute()) + "/UCH.db"
    connection = sqlite3.connect(path)  # DO NOT add this file to Git!!!
    cursor = connection.cursor()
    conncursordict = {"connection": connection, "cursor": cursor}
    return conncursordict


# disconnect from your database
def close_connection(conn):
    conn.commit()
    conn.close()


"""
place all functions below in the following template....

def functionname(args):
    conn = connecttodb()

    *your code here.....*

    closeconn(conn["connection"])

"""


def get_all_dosage_types():
    conn = connect_to_db()

    conn['cursor'].execute("""SELECT DISTINCT dosageType FROM Medicine ORDER BY dosageType asc""")
    results = conn['cursor'].fetchall()

    dosageTypes = []

    for result in results:
        dosageTypes.append(result[0])

    close_connection(conn["connection"])

    return dosageTypes

def get_all_med_types():
    conn = connect_to_db()

    conn['cursor'].execute("""SELECT DISTINCT medicineType FROM Medicine ORDER BY medicineType asc""")
    results = conn['cursor'].fetchall()

    medicineTypes = []

    for result in results:
        medicineTypes.append(result[0])

    close_connection(conn["connection"])

    return medicineTypes

def get_all_med_categories():
    conn = connect_to_db()

    conn['cursor'].execute("""SELECT DISTINCT category FROM Medicine ORDER BY medicineType asc""")
    results = conn['cursor'].fetchall()

    categories = []

    for result in results:
        categories.append(result[0])

    close_connection(conn["connection"])

    return categories

# This searches for drugs
def medicine_search(medname, drugname, dosetype, medtype, category):
    conn = connect_to_db()

    if medname:
        medname = "%" + medname + "%"
    if drugname:
        drugname = "%" + drugname + "%"

    valuearray = [medname, medtype, drugname, dosetype, category]

    for key, value in enumerate(valuearray):
        if not value or value == "-":
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

    close_connection(conn["connection"])
    return results

def add_prescription_to_db(prescription):
    conn = connect_to_db()

    prescriptionTuple = tuple(prescription)

    conn['cursor'].execute("""
        INSERT INTO
            Prescription
        VALUES
            (?, ?, ?, ?, ?)
        """, prescriptionTuple)

    close_connection(conn["connection"])

def get_prescription_from_db(appointmentID):
    conn = connect_to_db()

    conn['cursor'].execute("""
        SELECT medicineID, medicineName, dosage, dosageMultiplier, dosageType, furtherInformation
        FROM Prescription
        LEFT JOIN Medicine
        USING (medicineID)
        WHERE appointmentID = ?
    """,(appointmentID,))

    results = conn['cursor'].fetchall()
    close_connection(conn["connection"])
    return results

def get_medicine_units(medicineID):
    conn = connect_to_db()

    conn['cursor'].execute("""
        SELECT activeIngredientUnit
        FROM Medicine
        WHERE medicineID = ?
    """,(medicineID,))

    results = conn['cursor'].fetchall()[0]
    close_connection(conn["connection"])
    return results

def delete_med_record(appointmentID):
    conn = connect_to_db()
    conn['cursor'].execute("""
            DELETE from Prescription
            WHERE 
            appointmentID = ?
        """, (appointmentID,))
    close_connection(conn["connection"])

def get_patient_allergies(nhsNumber):
    conn = connect_to_db()

    conn['cursor'].execute("""
                SELECT medName 
                FROM medAllergy
                WHERE nhsNumber = ?
            """, (nhsNumber,))

    results = conn['cursor'].fetchall()
    allergies = []
    for result in results:
        allergies.append(result[0])

    return allergies

    close_connection(conn["connection"])

def allergy_message_handler(nhsNumber, medicine):
    conn = connect_to_db()

    conn['cursor'].execute("""
                SELECT medName 
                FROM medAllergy
                WHERE nhsNumber = ?
            """, (nhsNumber,))

    results = conn['cursor'].fetchall()
    allergies = []
    for result in results:
        allergies.append(result[0])

    for allergy in allergies:
        searchpattern = r"\b{}\b".format(allergy)
        results = re.search(searchpattern,medicine,re.IGNORECASE)
        if results:
            warningmsg = "Warning! The patient has listed '" + allergy +\
                         "' as a medical allergy. Please consider carefully before adding this medicine"
            return warningmsg

    close_connection(conn["connection"])


# if __name__=="__main__":
#     #print(allergyhandler(1234567890,"The ultimate ibuprofen coma"))

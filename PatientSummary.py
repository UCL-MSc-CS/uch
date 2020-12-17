import sqlite3 as sql
import usefulfunctions as uf

connection = sql.connect('UCH.db')
c = connection.cursor()

nhsNumber = 1234567890

with open('PatientSummary.txt','w') as f:
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
    results = c.fetchall()
    dateOfBirth = uf.toregulartime(results[0][4])
    dateOfBirth = str(dateOfBirth)[0:10]
    f.write("-----------------------------------------------------------------------------------\n")
    f.write("                       Patient Summary of " + str(results[0][2]) + " " + str(results[0][3] + '\n'))
    f.write("-----------------------------------------------------------------------------------\n")
    f.write("Your NHS number is: \n")
    x = str(results[0][0])
    one = x[0:3]
    two = x[3:6]
    three = x[6:10]
    f.write("{} {} {} ".format(one,two,three) + '\n')
    f.write("First Name: " + str(results[0][2] + '\n'))
    f.write("Last Name: " + str(results[0][3] + '\n'))
    f.write("Email: " + str(results[0][1]) + '\n')
    f.write("Date of Birth: " + str(dateOfBirth) + '\n')
    f.write("Gender: " + str(results[0][5]) + '\n')
    f.write("Address: \n")
    f.write(str(results[0][6]) + '\n')
    f.write(str(results[0][7]) + '\n')
    f.write(str(results[0][8]) + '\n')
    f.write("Telephone Number: +" + str(results[0][9] + '\n'))

    f.write("--------------------------------------------\n")
    f.write("PROBLEMS: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT dateRequested, diagnosis FROM Appointment WHERE nhsNumber = 1234567890""")
    items = c.fetchall()
    for i in range(0,len(items)):
        f.write(str(items[i][0]) + "       " + str(items[i][1]) + '\n')

    f.write("--------------------------------------------\n")
    f.write("HEALTH STATUS: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT height, weight, bmi, smoking, alcoholUnit, drugs FROM questionnaireTable WHERE
    nhsNumber = 1234567890""")
    items = c.fetchall()
    f.write("Height: " + "                    " + str(items[0][0]) + '\n')
    f.write("Weight: " + "                    " + str(items[0][1]) + '\n')
    f.write("BMI: " + "                       " + str(items[0][2]) + '\n')
    f.write("Smoker: " + "                    " + str(items[0][3]) + '\n')
    f.write("Units of Alcohol/Week): " + "    " + str(items[0][4]) + '\n')
    f.write("Drug user: " + "                 " + str(items[0][5]) + '\n')

    f.write("--------------------------------------------\n")
    f.write("MEDICATION: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT Medicine.medicineName, Prescription.dosage, Appointment.dateRequested, Appointment.appointmentID
    FROM Medicine, Prescription, Appointment
    WHERE Appointment.appointmentID = Prescription.appointmentID
    AND Medicine.medicineID = Prescription.medicineID
    AND Appointment.nhsNumber = ?""", (nhsNumber,))
    items = c.fetchall()
    for i in range(0,len(items)):
        f.write(str(items[i][0]) + "        " + str(items[i][1]) + "        " + str(items[i][2] + "\n"))

    f.write("--------------------------------------------\n")
    f.write("CANCER HISTORY: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT cancerRelation, cancerType, cancerAge FROM cancer WHERE
            nhsNumber = ?""", (nhsNumber,))
    items = c.fetchall()
    f.write("Cancer Relation" + "        " + "Cancer Type" + "        " + "Cancer Age")
    for i in range(0, len(items)):
        f.write(str(items[i][0]) + "        " + str(items[i][1]) + "        " + str(items[i][2] + "\n"))

    f.write("--------------------------------------------\n")
    f.write("PRE-EXISTING CONDITIONS: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT conditionType FROM preExistingCondition WHERE
                nhsNumber = ?""", (nhsNumber,))
    items = c.fetchall()
    for i in range(0, len(items)):
        f.write(str(items[i][0]) + '\n')

    f.write("--------------------------------------------\n")
    f.write("MEDICINE ALLERGIES: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT medName FROM medAllergy WHERE
                    nhsNumber = ?""", (nhsNumber,))
    items = c.fetchall()
    for i in range(0, len(items)):
        f.write(str(items[i][0]) + '\n')

    f.write("--------------------------------------------\n")
    f.write("Vaccine History: \n")
    f.write("--------------------------------------------\n")
    c.execute("""SELECT Status, DTap, HepC, HepB, Measles, Mumps, Rubella, Varicella FROM vaccineHistory WHERE
            nhsNumber = ?""", (nhsNumber,))
    items = c.fetchall()
    f.write("Status: " + "        " + str(items[0][0]) + '\n')
    f.write("DTap: " + "          " + str(items[0][1]) + '\n')
    f.write("HepC: " + "          " + str(items[0][2]) + '\n')
    f.write("HepB: " + "          " + str(items[0][3]) + '\n')
    f.write("Measles: " + "       " + str(items[0][4]) + '\n')
    f.write("Mumps: " + "         " + str(items[0][5]) + '\n')
    f.write("Rubella: " + "       " + str(items[0][6]) + '\n')
    f.write("Varicella: " + "     " + str(items[0][7]) + '\n')




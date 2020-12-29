import sqlite3 as sql
import usefulfunctions as uf
from datetime import datetime

datetimeformat = "%Y-%m-%d %H:%M"

def patient_summary(nhsNumber):
    """
    This is the function for generating the patient summary. The patient summary is an important document used in 
    the NHS that aims to show doctors what current/ongoing problems the patient may be experiencing, what
    treatments the patient has undergone recently and any other relevant background information. 
    The layout and formatting of this summary is designed to reflect what is used in practice by the NHS as much as 
    possible. Similarly, it is also generated in a format that can be emailed and printed easily to allow it to 
    be exchanged between doctors, as done in the NHS. In this case, the .txt format was chosen. 

    Parameters: 
        nhsNumber - the NHS number of the patient that the summary is on. 
    """
    connection = sql.connect('UCH.db')
    c = connection.cursor()

    with open('patient_{}_summary.txt' .format(nhsNumber),'w') as f:
        c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", (nhsNumber,))
        results = c.fetchall()
        dateOfBirth = results[0][4]
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
        c.execute("""SELECT start, diagnosis FROM Appointment WHERE nhsNumber = ?""", (nhsNumber,))
        items = c.fetchall()

        for i in range(0,len(items)):
            date_unix = items[i][0]
            date_regular = uf.toregulartime(date_unix)
            date_regular = date_regular.strftime("%Y-%m-%d")
            diagnosis = items[i][1]
            if items[i][1] == '':
                diagnosis = "Diagnosis pending"
            f.write(str(date_regular) + "       " + str(diagnosis) + '\n')

        f.write("--------------------------------------------\n")
        f.write("HEALTH STATUS: \n")
        f.write("--------------------------------------------\n")
        c.execute("""SELECT height, weight, bmi, smoking, alcoholUnit, drugs FROM questionnaireTable WHERE
        nhsNumber = ?""", (nhsNumber,))
        items = c.fetchall()
        if items == []:
            f.write("The patient has not provided this information \n")
        else:
            f.write("Height: " + "                    " + str(items[0][0]) + '\n')
            f.write("Weight: " + "                    " + str(items[0][1]) + '\n')
            f.write("BMI: " + "                       " + str(items[0][2]) + '\n')
            f.write("Smoker: " + "                    " + str(items[0][3]) + '\n')
            f.write("Units of Alcohol/Week): " + "    " + str(items[0][4]) + '\n')
            f.write("Drug user: " + "                 " + str(items[0][5]) + '\n')

        f.write("--------------------------------------------\n")
        f.write("MEDICATION: \n")
        f.write("--------------------------------------------\n")
        c.execute("""
        SELECT M.medicineName, P.dosage, A.start, A.appointmentID
        FROM Medicine M
        LEFT JOIN Prescription P ON M.medicineID = P.medicineID 
        LEFT JOIN Appointment A ON A.appointmentID = P.appointmentID
        WHERE A.nhsNumber = ?"""
        , (nhsNumber,))
        items = c.fetchall()
        if items == []:
            f.write("The patient has no medication history \n")
        else:
            for i in range(0,len(items)):
                time_string = datetime.strftime(uf.toregulartime(items[i][2]),datetimeformat)
                if len(str(items[i][0])) > 30:
                    f.write('{:<60s}{:^10s}{:^20s} \n'.format(items[i][0], items[i][1], time_string))
                else:
                    f.write('{:<30s}{:^10s}{:^20s} \n'.format(items[i][0], items[i][1], time_string))
            # There are many medicines in the medicine database with long names. The longest is "Butalbital, Acetaminophen, Caffeine, and Codeine Phosphate " 
            # which is 59 characters long. In case a medecine with a long name is used, other columns are moved to the right to allow space for it. 

        f.write("--------------------------------------------\n")
        f.write("CANCER HISTORY: \n")
        f.write("--------------------------------------------\n")
        c.execute("""SELECT cancerRelation, cancerType, cancerAge FROM cancer WHERE
                nhsNumber = ?""", (nhsNumber,))
        items = c.fetchall()
        f.write(("Age:").ljust(20, ' ') + ("Relation:").ljust(25, ' ') + ("Type:") + "\n")
        for i in range(0, len(items)):
            f.write(str(items[i][2]).ljust(20, ' ') + str(items[i][0]).ljust(25, ' ') + str(items[i][1] + "\n"))

        f.write("--------------------------------------------\n")
        f.write("PRE-EXISTING CONDITIONS: \n")
        f.write("--------------------------------------------\n")
        c.execute("""SELECT conditionType FROM preExistingCondition WHERE
                    nhsNumber = ?""", (nhsNumber,))
        items = c.fetchall()
        if items == []:
            f.write("The patient has no recorded pre-existing conditions \n")
        else:
            for i in range(0, len(items)):
                f.write(str(items[i][0]) + '\n')

        f.write("--------------------------------------------\n")
        f.write("MEDICINE ALLERGIES: \n")
        f.write("--------------------------------------------\n")
        c.execute("""SELECT medName FROM medAllergy WHERE
                        nhsNumber = ?""", (nhsNumber,))
        items = c.fetchall()
        if items == []:
            f.write("The patient has no recorded allergies \n")
        else:
            for i in range(0, len(items)):
                f.write(str(items[i][0]) + '\n')

        f.write("--------------------------------------------\n")
        f.write("Vaccine History: \n")
        f.write("--------------------------------------------\n")
        c.execute("""SELECT Status, DTap, HepC, HepB, Measles, Mumps, Rubella, Varicella FROM vaccineHistory WHERE
                nhsNumber = ?""", (nhsNumber,))
        items = c.fetchall()
        if items == []:
            f.write("The patient has not provided this information \n")
        else:
            f.write("Status: " + "        " + str(items[0][0]) + '\n')
            f.write("DTap: " + "          " + str(items[0][1]) + '\n')
            f.write("HepC: " + "          " + str(items[0][2]) + '\n')
            f.write("HepB: " + "          " + str(items[0][3]) + '\n')
            f.write("Measles: " + "       " + str(items[0][4]) + '\n')
            f.write("Mumps: " + "         " + str(items[0][5]) + '\n')
            f.write("Rubella: " + "       " + str(items[0][6]) + '\n')
            f.write("Varicella: " + "     " + str(items[0][7]) + '\n')

    print("Summary downloaded, check your folder to see the file")

if __name__ == "__main__":
    patient_summary(1234567890)

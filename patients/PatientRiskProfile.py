import sqlite3 as sql


class PatientMedical:
    def __init__(self,):
        self.connection = sql.connect('patient.db')
        self.a = self.connection.cursor()
        self.vaccination_history = ["DTap", "HepC", "HepB",
                                    "Measles", "Mumps", "Rubella", "Varicella"]
        self.cancer_history = []
        self.status = ""

    def vaccination(self):
        print('Please enter your answers to the following questions with Yes/No')
        answers_to_vac = []
        print("[1]: provide your own vaccination history."
              "\n[2]: provide vaccination history for your child.")
        menu_selection = input("Please select based on menu: ")
        if menu_selection == "1":
            self.status = "own"
            self.a.execute("""INSERT INTO medicalHistory(Status)
                                            VALUES (?)""", [self.status])
            for name in self.vaccination_history:
                vaccine = input('Have you had the {} vaccination: '.format(name)).lower()
                answers_to_vac.append(vaccine)
                if vaccine == "no":
                    print("Please book an appointment with your GP to receive your {} vaccination "
                          "as soon as possible.".format(name))
                else:
                    print("Wonderful!")
            self.a.execute("""INSERT INTO medicalHistory (DTap, HepC, HepB,
                                        Measles, Mumps, Rubella, Varicella)
                                        VALUES (?, ?, ?, ?, ?, ?, ?) """, answers_to_vac)
        elif menu_selection == "2":
            self.status = input("Please enter the full name of your child: ")
            for name in self.vaccination_history:
                vaccine = input('Has your child had the {} vaccination: '.format(name)).lower()
                answers_to_vac.append(vaccine)
                if vaccine == "no":
                    print("Please book an appointment with a GP to receive your child's {} vaccination "
                          "as soon as possible.".format(name))
                else:
                    print("Wonderful!")
            answers_to_vac.append(self.status)
            self.a.execute("""INSERT INTO medicalHistory (DTap, HepC, HepB,
                                        Measles, Mumps, Rubella, Varicella, Status)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?) """, answers_to_vac)

    def cancer(self):
        self.a.execute("""CREATE TABLE IF NOT EXISTS cancer(
                            PatientID INTEGER PRIMARY KEY,
                            cancer DATATYPE text,
                            cancerType DATATYPE text,
                            cancerAge DATATYPE text,
                            cancerFamily DATATYPE text,
                            cancerTypeFamily DATATYPE text,
                            cancerAgeFamily DATATYPE text)""")
        print("Thank you! The following questions are concerned with your medical history and "
              "the medical history of your family.")
        print("[1]: provide your medical history"
              "\n[2]: provide the medical history of your family.")
        menu_choice = input("Please select based on menu: ")
        print('Please enter your answers to the following questions with Y/N')
        if menu_choice == "2":
            cancer = input('Has anyone in your immediate family, parents or siblings, '
                           'ever been diagnosed with cancer: ').lower()
            if cancer == "y":
                cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
                for cancer_name in cancer_type:
                    cancer_age = input('How old was the person diagnosed with {}: '.format(cancer_name))
                    row_record = [cancer, cancer_name, cancer_age]
                    self.cancer_history.append(tuple(row_record))
                self.a.executemany("""INSERT INTO cancer (cancerFamily, cancerTypeFamily, cancerAgeFamily) 
                VALUES (?, ?, ?)""", self.cancer_history)
            else:
                print("Wonderful! That means you do not likely have any genetic risk in any specific cancer "
                      "that we know so far based on your family medical history")
                self.a.execute("""INSERT INTO cancer(cancerFamily)
                                                VALUES (?)""", cancer)
        elif menu_choice == "1":
            cancer = input('Have you ever been diagnosed with cancer:').lower()
            if cancer == "y":
                cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
                for cancer_name in cancer_type:
                    cancer_age = input('How old were you when you were diagnosed with {}: '.format(cancer_name))
                    row_record2 = [cancer, cancer_name, cancer_age]
                    self.cancer_history.append(tuple(row_record2))
                self.a.executemany("""INSERT INTO cancer (cancer, cancerType, cancerAge) 
                VALUES (?, ?, ?)""", self.cancer_history)
            else:
                self.a.execute("""INSERT INTO cancer(cancerFamily)
                                                VALUES (?)""", cancer)

        self.a.execute("SELECT * FROM cancer")
        show2 = self.a.fetchall()
        print(show2)
        self.a.execute("SELECT * FROM medicalHistory")
        show3 = self.a.fetchall()
        print(show3)
        self.connection.commit()
        self.connection.close()
#
Erin = PatientMedical()
Erin.vaccination()
Erin.cancer()


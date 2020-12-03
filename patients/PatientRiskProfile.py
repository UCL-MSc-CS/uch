import sqlite3 as sql


class PatientMedical:
    def __init__(self,):
        self.connection = sql.connect('patient.db')
        self.a = self.connection.cursor()
        self.vaccination_history = ["DTap", "HepC", "HepB",
                                    "Measles", "Mumps", "Rubella", "Varicella"]
        self.cancer_history = []

    def vaccination(self):
        print('Please enter your answers to the following questions with Yes/No')
        count = 0
        answers_to_vac = []
        for name in self.vaccination_history:
            vaccine = input('Have you had the {} vaccination: '.format(name)).lower()
            answers_to_vac.append(vaccine)
            if vaccine == "no":
                print("Please book an appointment with your GP to receive your {} vaccination "
                      "as soon as possible.".format(name))
            else:
                print("Wonderful!")
            count += 1
        query = """INSERT INTO medicalHistory (DTap, HepC, HepB,
                                    Measles, Mumps, Rubella, Varicella)
                                    VALUES (?, ?, ?, ?, ?, ?, ?) """

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
                print(self.cancer_history)
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
                print(self.cancer_history)
                self.a.executemany("""INSERT INTO cancer (cancerFamily, cancerTypeFamily, cancerAgeFamily) 
                VALUES (?, ?, ?)""", self.cancer_history)
            else:
                self.a.execute("""INSERT INTO cancer(cancerFamily)
                                                VALUES (?)""", cancer)
        self.a.execute("SELECT * FROM cancer")
        show2 = self.a.fetchall()
        print(show2)
        self.connection.commit()
        self.connection.close()


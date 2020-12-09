import sqlite3 as sql


#  need to add exception handling and other additional features.
class PatientMedical:
    def __init__(self):
        self.connection = sql.connect('patient.db')
        self.a = self.connection.cursor()
        self.vaccination_history = ["DTap", "HepC", "HepB",
                                    "Measles", "Mumps", "Rubella", "Varicella"]
        self.cancer_history = []
        self.status = ""
        self.cancer_relation = ""

    def vaccination(self, patient_email):
        print('Please enter your answers to the following questions with Yes/No')
        answers_to_vac = []
        print("[1]: provide your own vaccination history."
            "\n[2]: provide vaccination history for your child.")
        menu_selection = input("Please select based on the menu: ")
        self.a.execute("SELECT patientEmail FROM PatientDetail")
        if menu_selection == "1":
            self.status = "own"
            patient_info = [patient_email, self.status]
            self.connection.commit()
            for name in self.vaccination_history:
                vaccine = input('Have you had the {} vaccination: '.format(name)).lower()
                answers_to_vac.append(vaccine)
                if vaccine == "no":
                    print("Please book an appointment with your GP to receive your {} vaccination "
                          "as soon as possible.".format(name))
                else:
                    print("Wonderful!")
            patient_info.extend(answers_to_vac)
            self.a.execute("""INSERT INTO medicalHistory (patientEmail, Status, DTap, HepC, HepB,
                                        Measles, Mumps, Rubella, Varicella)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, patient_info)
            self.connection.commit()
        elif menu_selection == "2":
            self.status = input("Please enter the full name of your child whose profile you would like to edit: ")
            patient_info = [patient_email, self.status]
            for name in self.vaccination_history:
                vaccine = input('Has your child had the {} vaccination: '.format(name)).lower()
                answers_to_vac.append(vaccine)
                if vaccine == "no":
                    print("Please book an appointment with a GP to receive your child's {} vaccination "
                          "as soon as possible.".format(name))
                else:
                    print("Wonderful!")
            patient_info.extend(answers_to_vac)
            self.a.execute("""INSERT INTO medicalHistory (patientEmail, Status, DTap, HepC, HepB,
                                        Measles, Mumps, Rubella, Varicella)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, patient_info)
            self.connection.commit()

    def cancer(self, patient_email):
        # cancerRelation: self or the family relation (i.e sister, brother, daughter, mother etc.)
        # query set up in the future if needed: WHERE cancerRelation != "1" AND != "0" AND != "None" AND cancerAge <50
        # patient has genetic risk in developing that type of cancer diagnosed. (additional feature)
        # add additional feature on traveling vaccine advice/ book appointment.
        print("Thank you! The following questions are concerned with your medical history and "
              "the medical history of your family.")
        print("[1]: provide your medical history"
            "\n[2]: provide the medical history of your family.")
        menu_choice = input("Please select based on the menu: ")
        print('Please enter your answers to the following questions with Y/N')
        if menu_choice == "1":
            cancer = input('Have you ever been diagnosed with cancer:').lower()
            if cancer == "y":
                self.cancer_relation = "1"  # 1 means the patient has had cancer before
                cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
                for cancer_name in cancer_type:
                    cancer_age = input('How old were you when you were diagnosed with {}: '.format(cancer_name))
                    row_record = [patient_email, self.cancer_relation, cancer_name, cancer_age]
                    self.cancer_history.append(tuple(row_record))
                self.a.executemany("""INSERT INTO cancer (patientEmail, cancerRelation, cancerType, cancerAge)
                            VALUES (?, ?, ?, ?)""", self.cancer_history)
                self.connection.commit()
            else:
                cancer_relation = "0"  # 0 means the patient has not had not have cancer before
                self.a.execute("""INSERT INTO cancer(patientEmail, cancerRelation)
                                                            VALUES (?, ?)""", [patient_email, cancer_relation])
                self.connection.commit()
        elif menu_choice == "2":
            cancer = input('Has anyone in your immediate family, parents, children, or siblings, '
                           'ever been diagnosed with cancer: ').lower()
            if cancer == "y":
                cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
                for cancer_name in cancer_type:
                    cancer_relation = input('What is your relation with this family member who was diagnosed with {}: '.format(cancer_name)).lower()
                    # error handling for multiple grandfathers, uncles, sisters etc.
                    # this is so depressing thinking someone's whole family has cancer....
                    cancer_age = input('How old was the family member diagnosed with {}: '.format(cancer_name))
                    # should I keep the reference of the cancer name or gender pronoun based on family relation?
                    # i.e. family relation = uncle, how old was he when he was diagnosed?
                    # do I even bother?
                    row_record = [patient_email, cancer_relation, cancer_name, cancer_age]
                    self.cancer_history.append(tuple(row_record))
                self.a.executemany("""INSERT INTO cancer (patientEmail, cancerRelation, cancerType, cancerAge)
                VALUES (?, ?, ?, ?)""", self.cancer_history)
                self.connection.commit()
            else:
                cancer_relation = "None"
                print("Wonderful! That means you do not likely have any genetic risk in any specific cancer "
                      "that we know so far based on your family medical history")
                self.a.execute("""INSERT INTO cancer(patientEmail, cancerFamily)
                                                VALUES (?, ?)""", [patient_email, cancer_relation])
                self.connection.commit()

    def show_profile(self, patientEmail):
        print("Which profile would you like to see? "
              "\n [1]: Your own risk profile"
              "\n [2]: Your children's risk profiles")
        profile = input("Please choose from the menu: ")
        count = 0
        if profile == "1":
            self.status = "own"
            self.a.execute("SELECT DTap, HepC, HepB, Measles, Mumps, Rubella, Varicella "
                           "FROM medicalHistory WHERE status = ? AND patientEmail = ? ", [self.status, patientEmail])
            your_query = self.a.fetchall()
            print("Your medical record: ")
            for vac in your_query:
                for answers in vac:
                    print(self.vaccination_history[count], ":", answers)
                    count += 1
        # add a cancer record for the patient himself or herself
        elif profile == "2":
            child_name = input("Please enter the full name of your child whose profile you would like to see: ")
            self.a.execute("SELECT DTap, HepC, HepB, Measles, Mumps, Rubella, Varicella "
                           "FROM medicalHistory WHERE status = ?", [child_name])
            child_query = self.a.fetchall()
            print("{}'s medical record: ".format(child_name))
            for vac in child_query:
                for answers in vac:
                    print(self.vaccination_history[count], ":", answers)
                    count += 1
        # add a cancer record for the patient's children in case with
        self.connection.commit()
        self.connection.close()


# Erin = PatientMedical()
# Erin.vaccination("ariannabourke@hotmail.com")
# Erin.cancer("ariannabourke@hotmail.com")
# Erin.show_profile("ariannabourke@hotmail.com")
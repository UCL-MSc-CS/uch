import sqlite3 as sql


class PatientMedical:
    def __init__(self,):
        self.connection = sql.connect('medicalHistory.db')
        self.a = self.connection.cursor()
        self.vaccination_history = ["DTap", "HepC", "HepB",
                                    "Measles", "Mumps", "Rubella", "Varicella"]
        self.cancer_history = {}

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
        self.a.execute(query, answers_to_vac)
        self.a.execute("SELECT * FROM medicalHistory")
        show = self.a.fetchall()
        print(show)

    def cancer_family(self):
        print("Thank you! The following questions are concerned with the medical history of your family.")
        print('Please enter your answers to the following questions with Y/N')
        cancer = input('Has anyone in your immediate family, parents or siblings, '
                       'ever been diagnosed with cancer: ').lower()
        if cancer == "y":
            cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
            for cancer_name in cancer_type:
                cancer_age = input('How old was the person diagnosed with {}: '.format(cancer_name))
                self.cancer_history[cancer_name] = cancer_age
            print(self.cancer_history)
        else:
            print("Wonderful! That means you do not likely have any genetic risk in any specific cancer that we know "
                  "so far based on your family medical history")

    # def cancer(self):
    #     print("Thank you! The following questions are concerned with your medical history.")
    #     print('Please enter your answers to the following questions with Y/N')
    #     cancer = input('Have you ever been diagnosed with cancer: ').lower()
    #     if cancer == "y":
    #         cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
    #         for cancer_name in cancer_type:
    #             cancer_age = input('How old were you when you were diagnosed with {}: '.format(cancer_name))
    #             self.cancer_history[cancer_name] = cancer_age
    #         print(self.cancer_history)

        self.connection.commit()
        self.connection.close()


Erin = PatientMedical()
Erin.vaccination()
# Erin.cancer()

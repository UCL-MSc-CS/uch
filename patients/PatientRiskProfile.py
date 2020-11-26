class PatientMedical:
    def __init__(self,):
        self.vaccination_history = {"DTap": "", "HepC": "", "HepB": "",
                                    "Measles": "", "Mumps": "", "Rubella": "", "Varicella": ""}
        self.cancer_history = {}

    def vaccination(self):
        print('Please enter your answers to the following questions with Yes/No')
        for index in self.vaccination_history:
            vaccine = input('Have you had the {} vaccination: '.format(index)).lower()
            self.vaccination_history[index] = vaccine
            if self.vaccination_history[index] == "no":
                print("Please book an appointment with your GP to receive your {} vaccination "
                      "as soon as possible.".format(index))
            else:
                print("Wonderful!")

    def cancer(self):
        print("Thank you! The following questions are concerned with the medical history of your family.")
        print('Please enter your answers to the following questions with Yes/No')
        cancer = input('Has anyone in your immediate family, parents or siblings, '
                       'ever been diagnosed with cancer: ').lower()
        if cancer == "yes":
            cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
            for cancer_name in cancer_type:
                cancer_age = input('How old was the person diagnosed with {}: '.format(cancer_name))
                self.cancer_history[cancer_name] = cancer_age
            print(self.cancer_history)
        else:
            print("Wonderful! That means you do not likely have any genetic risk in any specific cancer that we know "
                  "so far based on your family medical history")


Erin = PatientMedical()
Erin.vaccination()
Erin.cancer()

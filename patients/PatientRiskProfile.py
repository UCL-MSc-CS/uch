import sqlite3 as sql
import patients.patientMedicalFunctions as pf


"""Set up patient medical record"""
class PatientMedical:
    def __init__(self, nhsNumber):
        self.connection = sql.connect('UCH.db')
        self.a = self.connection.cursor()
        self.vaccination_history = ["DTap", "HepC", "HepB",
                                    "Measles", "Mumps", "Rubella", "Varicella"]
        self.cancer_history = []
        self.status = ""
        self.nhs_number_child = ""
        self.cancer_relation = ""
        self.child_name = ""

# Obtain information about the patient's vaccination history/parent patients can insert and modify children's records
    def vaccination(self, nhs_number):
        print('Please enter your answers to the following questions with Y/N: ')
        answers_to_vac = []
        while True:
            print("*"*44)
            print("Choose [1] provide your own vaccination history"
                "\nChoose [2] provide vaccination history for your child"
                "\nChoose [0] exit the menu")
            print("*"*44)
            while True:
                try:
                    menu_selection = input("Please select based on the menu: ")
                    if menu_selection == "0":
                        return 1
                    if not menu_selection:
                        raise pf.EmptyFieldError()
                    if menu_selection != "1" and menu_selection != "2" and menu_selection != "0":
                        raise pf.InvalidMenuSelectionError()
                except pf.EmptyFieldError:
                    error_message = pf.EmptyFieldError()
                    print(error_message)
                except pf.InvalidMenuSelectionError:
                    print("\n    <You entered an invalid value. Please type 1, 2, or 0 based on the menu>\n")
                else:
                    break
            if menu_selection == "1":
                self.status = "own"
                patient_info = [nhs_number, self.status]
                self.a.execute("SELECT nhsNumber FROM vaccineHistory WHERE nhsNumber = ?", [nhs_number])
                check_nhs = self.a.fetchall()
                if not check_nhs:
                    for name in self.vaccination_history:
                        while True:
                            try:
                                vaccine = input('Please enter Y/N. Have you had the {} vaccination: '.format(name)).lower()
                                if vaccine == "0":
                                    return 1
                                if not vaccine:
                                    raise pf.EmptyFieldError()
                                if vaccine != "y" and vaccine != "n":
                                    raise pf.InvalidAnswerError()
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            except pf.InvalidAnswerError:
                                print("\n    <You have entered a wrong value. Please type Y as yes and N as no>\n")
                            else:
                                break
                        if vaccine == "n":
                            vaccine = 0
                            answers_to_vac.append(vaccine)
                            print("Please book an appointment with your GP to receive your {} vaccination "
                                          "as soon as possible.".format(name))
                        if vaccine == "y":
                            vaccine = 1
                            answers_to_vac.append(vaccine)
                            print("Excellent! Please also remember to check back for any need for future boosters.")
                    patient_info.extend(answers_to_vac)
                    self.a.execute("""INSERT INTO vaccineHistory (nhsNumber, Status, DTap, HepC, HepB,
                                                    Measles, Mumps, Rubella, Varicella)
                                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, patient_info)
                    self.connection.commit()
                else:
                    print('Add a new update function')  # create and use update function
            if menu_selection == "2":  # Parents can add vaccination history to their underage children
                answers_to_vac = []
                while True:
                    try:
                        self.status = input("Please enter the full name of your child whose profile you would like to edit: ")
                        self.nhs_number_child = input("Please enter {}'s nhs number: ".format(self.status))
                        full_name = self.status.split(' ')
                        if self.status == "0":
                            return 1
                        if not self.status:
                            raise pf.EmptyFieldError()
                        if not self.nhs_number_child:
                            raise pf.EmptyFieldError()
                        if len(self.nhs_number_child) != 10:
                            raise pf.InvalidAnswerError()
                        if len(full_name) > 2 or len(full_name) == 1:
                            raise pf.InvalidNameFormatError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        error_message = "\n    <Invalid NHS number>\n"
                        print(error_message)
                    except pf.InvalidNameFormatError:
                        print("\n    <Wrong name format."
                              "Please enter your child's full name with a space separating the first and last name>\n")
                    else:
                        break
                self.a.execute("SELECT nhsNumber FROM vaccineHistory WHERE nhsNumber = ?", [self.nhs_number_child])
                check_child_nhs = self.a.fetchall()
                if not check_child_nhs:
                    patient_info = [self.nhs_number_child, self.status]
                    for name in self.vaccination_history:
                        while True:
                            try:
                                vaccine = input('Please enter Y/N. Has your {} had the {} vaccination: '.format(self.status, name)).lower()
                                if vaccine == "0":
                                    return 1
                                if not vaccine:
                                    raise pf.EmptyFieldError()
                                if vaccine != "y" and vaccine != "n":
                                    raise pf.InvalidAnswerError()
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            except pf.InvalidAnswerError:
                                print("\n    <You have entered a wrong value. Please type Y as yes and N as no>\n")
                            else:
                                break
                        if vaccine == "n":
                            vaccine = 0
                            answers_to_vac.append(vaccine)
                            print("Please book an appointment with a GP to receive {}'s {} vaccination "
                            "as soon as possible.".format(self.status, name))
                        if vaccine == "y":
                            vaccine = 1
                            answers_to_vac.append(vaccine)
                            print("Excellent! Please also remember to check back for any need for future boosters.")
                    patient_info.extend(answers_to_vac)
                    print(patient_info)
                    self.a.execute("""INSERT INTO vaccineHistory (nhsNumber, Status, DTap, HepC, HepB,
                                                        Measles, Mumps, Rubella, Varicella)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, patient_info)
                    self.connection.commit()
                else:
                    print('Add a new update function')  # create and use update function

# Obtain cancer related data from the patient, and parent patient can insert and modify children's records
    def cancer(self, nhs_number):
        # cancerRelation: self or the family relation (i.e sister, brother, daughter, mother etc.)
        # query set up in the future if needed: WHERE cancerRelation != "1" AND != "0" AND != "None" AND cancerAge <50
        # patient has genetic risk in developing that type of cancer diagnosed. (additional feature)
        # add additional feature on traveling vaccine advice/ book appointment.
        print("Thank you! The following questions are concerned with your medical history and "
              "the medical history of your family to assess the genetic risk of certain hereditary diseases.")
        while True:
            print("*"*44)
            print("Choose [1] provide your medical history"
                "\nChoose [2] provide family medical history"
                "\nChoose [3] provide medical history for your children"
                "\nChoose [0] exit")
            print("*"*44)
            while True:
                try:
                    menu_choice = input("Please select based on the menu: ")
                    if menu_choice == "0":
                        return 1
                    if not menu_choice:
                        raise pf.EmptyFieldError()
                    if menu_choice != "1" and menu_choice != "2" and menu_choice != "3" and menu_choice != "0":
                        raise pf.InvalidMenuSelectionError()
                except pf.EmptyFieldError:
                    error_message = pf.EmptyFieldError()
                    print(error_message)
                except pf.InvalidMenuSelectionError:
                    print("\n    <You entered an invalid value. Please type 1, 2, 3, or 0 based on the menu>\n")
                else:
                    break
            print('Please enter your answers to the following questions with Y/N.')
            if menu_choice == "1":
                self.a.execute("""
                                SELECT nhsNumber FROM preExistingCondition 
                                WHERE nhsNumber =? """, [nhs_number])
                patient_result = self.a.fetchall()
                if not patient_result:
                    while True:  # asking patient about existing medical conditions
                        try:
                            major_illness = input('Do you have any pre-existing conditions?'
                            '\nIf so, please enter the name of the pre-existing condition using comma to '
                            'separate different consitions. Otherwise, type N for no: ').lower().split(',')
                            if major_illness == ['']:
                                raise pf.EmptyFieldError()
                            answer_box = ["yes", "YES", "Yes", "y", "No", "NO", "no"]
                            for ele in major_illness:
                                if ele in answer_box:
                                    raise pf.InvalidConditionFormatError()
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        except pf.InvalidConditionFormatError:
                            error_message = pf.InvalidConditionFormatError()
                            print(error_message)
                        except ValueError:
                            print('\n    <Please enter a non-numeric value>\n')
                        else:
                            break
                    condition = []
                    for i in major_illness:
                        condition_record = tuple([nhs_number, i])
                        condition.append(condition_record)
                    self.a.executemany("""INSERT INTO preExistingCondition(nhsNumber, conditionType) VALUES (?, ?)""", condition)
                    self.connection.commit()
                self.a.execute("""SELECT nhsNumber FROM medAllergy WHERE nhsNumber =? """, [nhs_number])
                allergy_result = self.a.fetchall()
                if not allergy_result:
                    while True:  # asking patient about existing medicine allergy
                        try:
                            med_allergy = input('Do you have any allergies to any medicines?'
                            '\nIf so, please enter the name of the medicine using comma to '
                            'separate different types. Otherwise, type N for no: ').lower().split(',')
                            if med_allergy == ['']:
                                raise pf.EmptyFieldError()
                            answer_box = ["yes", "YES", "Yes", "y", "No", "NO", "no"]
                            for ele in med_allergy:
                                if ele in answer_box:
                                    raise pf.InvalidAllergyFormatError()
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        except pf.InvalidAllergyFormatError:
                            error_message = pf.InvalidAllergyFormatError()
                            print(error_message)
                        except ValueError:
                            print('\n    <Please enter a non-numeric value>\n')
                        else:
                            break
                    allergy = []
                    for i in med_allergy:
                        allergy_record = tuple([nhs_number, i])
                        allergy.append(allergy_record)
                    self.a.executemany("""INSERT INTO medAllergy(nhsNumber, medName) VALUES (?, ?)""", allergy)
                    self.connection.commit()
                while True:
                    try:
                        cancer = input('Have you ever been diagnosed with cancer: ').lower()
                        if not cancer:
                            raise pf.EmptyFieldError()
                        if cancer != "y" and cancer != "n":
                            raise pf.InvalidAnswerError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        print("\n    <Wrong value entered. Please type Y as yes and N as no>\n")
                    else:
                        break
                if cancer == "y":
                    self.cancer_relation = "1"  # 1 means the patient has had cancer before
                    print("Please use commas when entering multiple values.")
                    while True:
                        try:
                            cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
                            if not cancer_type:
                                raise pf.EmptyFieldError()
                        # what if user enters a numeric value
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        except pf.InvalidAnswerError:
                            print("\n    <Invalid answer. Please enter a non-numeric value>\n")
                        else:
                            break
                    for cancer_name in cancer_type:
                        c = cancer_name
                        if "cancer" in cancer_name:
                            c = cancer_name[-len(cancer_name):-6]
                        while True:
                            try:
                                cancer_age = int(input('How old were you when you were diagnosed with {} cancer: '.format(c)))
                                if not cancer_age:
                                    raise pf.EmptyFieldError()
                                if type(cancer_age) is not int:
                                    raise ValueError()
                                if cancer_age >= 150:
                                    raise pf.InvalidAnswerError()
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            except ValueError:
                                print("\n    <Invalid answer. Please enter a numeric value>\n")
                            except pf.InvalidAnswerError:
                                print("\n    <Invalid answer. Please enter the correct age>\n")
                            else:
                                break
                        row_record = [nhs_number, self.cancer_relation, cancer_name, cancer_age]
                        self.cancer_history.append(tuple(row_record))
                    self.a.executemany("""INSERT INTO cancer(nhsNumber, cancerRelation, cancerType, cancerAge)
                                VALUES (?, ?, ?, ?)""", self.cancer_history)
                    self.connection.commit()
                else:
                    self.cancer_relation = "0"  # 0 means the patient has not had cancer before
                    self.a.execute("""INSERT INTO cancer(nhsNumber, cancerRelation)
                                                                VALUES (?, ?)""", [nhs_number, self.cancer_relation])
                    self.connection.commit()
            elif menu_choice == "2":
                while True:
                    try:
                        cancer = input('Has anyone in your immediate family, parents, children, or siblings, '
                                       'ever been diagnosed with cancer: ').lower()
                        if not cancer:
                            raise pf.EmptyFieldError()
                        if cancer != "y" and cancer != "n":
                            raise pf.InvalidAnswerError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        print("\n    <You have entered a wrong value. Please type Y as yes and N as no>\n")
                    else:
                        break
                if cancer == "y":
                    while True:
                        try:
                            cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").split(",")
                            if not cancer_type:
                                raise pf.EmptyFieldError()
                            # what if user enters a numeric value?
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        except pf.InvalidAnswerError:
                            print("\n    <Invalid answer. Please enter a non-numeric value>\n")
                        else:
                            break
                    for cancer_name in cancer_type:
                        c = cancer_name
                        if "cancer" in cancer_name:
                            c = cancer_name[-len(cancer_name):-7]
                        while True:
                            try:
                                self.cancer_relation = input('What is your relation with this family member who was diagnosed with {} cancer: '.format(c)).lower()
                                if self.cancer_relation == "":
                                    raise pf.EmptyFieldError()
                                # if user enters a numeric value?
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            except pf.InvalidAnswerError:
                                print("\n    <Invalid answer. Please enter a non-numeric value>\n")
                            except pf.InvalidNameFormatError:
                                print("\n    <Please do not use any special characters or punctuations in your answer>\n")
                            else:
                                break
                        while True:
                            try:
                                cancer_age = int(input('How old was the family member diagnosed with {} cancer: '.format(c)))
                                if cancer_age == "":
                                    raise pf.EmptyFieldError()
                                # if user enters a non-numeric value?
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            except pf.InvalidAnswerError:
                                print("\n    <Invalid answer. Please enter a numeric value>\n")
                            except pf.InvalidNameFormatError:
                                print("\n    <Please do not use any special characters or punctuations in your answer>\n")
                            else:
                                break
                        row_record = [nhs_number, self.cancer_relation, cancer_name, cancer_age]
                        self.cancer_history.append(tuple(row_record))
                    self.a.executemany("""INSERT INTO cancer(nhsNumber, cancerRelation, cancerType, cancerAge)
                    VALUES (?, ?, ?, ?)""", self.cancer_history)
                    self.connection.commit()
                else:
                    self.cancer_relation = "None"
                    print("Wonderful! That means you do not likely have any genetic risk in any specific cancer "
                          "that we know so far based on your family medical history.")
                    self.a.execute("""INSERT INTO cancer(nhsNumber, cancerRelation)
                                                    VALUES (?, ?)""", [nhs_number, self.cancer_relation])
                    self.connection.commit()
            elif menu_choice == "3":
                while True:
                    try:
                        self.child_name = input("Please enter the full name of your child whose profile you would like to edit: ")
                        self.nhs_number_child = input("Please enter {}'s nhs number: ".format(self.child_name))
                        full_name = self.child_name.split(' ')
                        if self.child_name == "0":
                            return 1
                        if not self.child_name:
                            raise pf.EmptyFieldError()
                        if not self.nhs_number_child:
                            raise pf.EmptyFieldError()
                        if len(self.nhs_number_child) != 10:
                            raise pf.InvalidAnswerError()
                        if len(full_name) == 1 or len(full_name) < 2:
                            raise pf.InvalidNameFormatError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        error_message = "\n    <Invalid NHS number>\n"
                        print(error_message)
                    except pf.InvalidNameFormatError:
                        print("\n    <Wrong name format."
                              "Please enter your child's full name with a space separating the first and last name>\n")
                    else:
                        break
                self.a.execute("""SELECT nhsNumber FROM preExistingCondition WHERE nhsNumber = ?""", [self.nhs_number_child])
                check_child_nhs = self.a.fetchall()
                self.a.execute("""SELECT nhsNumber FROM medAllergy WHERE nhsNumber = ?""", [self.nhs_number_child])
                check_child_nhs2 = self.a.fetchall()
                if not check_child_nhs:  # if child's nhs number does not exist in database, insert
                    while True:  # asking about children's existing medical conditions
                        try:
                            major_illness = input('Does {} have any pre-existing conditions?'
                            '\nIf so, please enter the name of the pre-existing condition using comma to '
                            'separate different conditions. Otherwise, type N for no: '.format(self.child_name)).split(',')
                            if major_illness == ['']:
                                raise pf.EmptyFieldError()
                            answer_box = ["yes", "YES", "Yes", "y", "No", "NO", "no"]
                            for ele in major_illness:
                                if ele in answer_box:
                                    raise pf.InvalidConditionFormatError()
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        except pf.InvalidConditionFormatError:
                            error_message = pf.InvalidConditionFormatError()
                            print(error_message)
                        except ValueError:
                            print('\n    <Please enter a non-numeric value or leave this field blank>\n')
                        else:
                            break
                    condition = []
                    for i in major_illness:
                        condition_record = tuple([self.nhs_number_child, i])
                        condition.append(condition_record)
                    self.a.executemany("""INSERT INTO preExistingCondition(nhsNumber, conditionType) VALUES (?, ?)""", condition)
                    self.connection.commit()
                else:
                    print('Update function possibly')
                if not check_child_nhs2:
                    while True:  # asking about children's medicine allergy
                        try:
                            med_allergy = input('Does {} have any allergies to any medicines?'
                            '\nIf so, please enter the name of the medicine using comma to '
                            'separate different types. Otherwise, type N for no: '.format(self.child_name)).split(',')
                            if med_allergy == ['']:
                                raise pf.EmptyFieldError()
                            answer_box = ["yes", "YES", "Yes", "y", "No", "NO", "no"]
                            for ele in med_allergy:
                                if ele in answer_box:
                                    raise pf.InvalidAllergyFormatError()
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        except pf.InvalidAllergyFormatError:
                            error_message = pf.InvalidAllergyFormatError()
                            print(error_message)
                        except ValueError:
                            print('\n    <Please enter a non-numeric value>\n')
                        else:
                            break
                    allergy = []
                    for a in med_allergy:
                        allergy_record = tuple([self.nhs_number_child, a])
                        allergy.append(allergy_record)
                    self.a.executemany("""INSERT INTO medAllergy(nhsNumber, medName) VALUES (?, ?)""", allergy)
                    self.connection.commit()
                else:
                    print('Update function possibly')

# Display all types of medical related profile for the patient and the patient's children.
    def show_profile(self, nhs_number):
        while True:
            print("*"*44)
            print("Which profile would you like to see? "
                  "\nChoose [1] Your own medical history profile"
                  "\nChoose [2] Your children's medical profiles"
                  "\nChoose [0] exit")
            print("*"*44)
            while True:
                try:
                    profile = input("Please choose from the menu: ")
                    if profile == "0":
                        return 1
                    if not profile:
                        raise pf.EmptyFieldError()
                    if profile != "1" and profile != "2" and profile != "0":
                        raise pf.InvalidMenuSelectionError()
                except pf.EmptyFieldError:
                    error_message = pf.EmptyFieldError()
                    print(error_message)
                except pf.InvalidMenuSelectionError:
                    print("\n    <You entered an invalid value. Please type 1, 2, or 0 based on the menu>\n")
                else:
                    break
            count = 0
            if profile == "1":
                self.a.execute("""SELECT DTap, HepC, HepB, Measles, Mumps, Rubella, Varicella "
                               "FROM vaccineHistory WHERE nhsNumber = ? """, [nhs_number])
                your_query = self.a.fetchall()
                if your_query:
                    print("\n    Your vaccination record begins:\n")
                    for vac in your_query:
                        for answers in vac:
                            if answers == 1:
                                print(self.vaccination_history[count], ": Yes")
                            else:
                                print(self.vaccination_history[count], ": No")
                            count += 1

                    print('\n    Vaccination record ends\n')
                else:
                    print("\nYour vaccination history is empty. Please update your vaccination history as soon as possible.\n")
                print('Your medical history:')
                print('\n    <<Cancer record begins>>\n')
                pf.display_cancer_history(nhs_number)
                pf.display_preexisting_condition_history(nhs_number)
            if profile == "2":
                while True:
                    try:
                        print("Please use space to separate first and last names.")
                        child_name = input("Please enter the full name of your child whose profile you would like to see: ")
                        full_name = child_name.split(' ')
                        if child_name == "0":
                            return 1
                        if not child_name:
                            raise pf.EmptyFieldError()
                        if len(full_name) <= 1:
                            raise pf.InvalidNameFormatError()
                        self.nhs_number_child = input("Please enter {}'s nhs number: ".format(child_name))
                        if self.nhs_number_child == "0":
                            return 1
                        if not self.nhs_number_child:
                            raise pf.EmptyFieldError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidNameFormatError:
                        print("\n    <Invalid answer. Please enter your child's full name with a space separating the first and last name>\n")
                    else:
                        break
                self.a.execute("SELECT DTap, HepC, HepB, Measles, Mumps, Rubella, Varicella "
                               "FROM vaccineHistory WHERE nhsNumber = ? AND status = ?", [self.nhs_number_child, child_name])
                child_query = self.a.fetchall()
                if child_query:
                    print('\n    <<Vaccination record begins>>\n')
                    for vac in child_query:
                        for answers in vac:
                            if answers == 1:
                                print(self.vaccination_history[count], ": Yes")
                            else:
                                print(self.vaccination_history[count], ": No")
                            count += 1
                    print('\n    <<Vaccination record ends>>\n')
                else:
                    print("\nVaccination history is empty/Records do not exist\n")
                print("{}'s medical history:".format(child_name))
                # print('\n    <<Cancer record begins>>\n')
                # pf.display_cancer_history(self.nhs_number_child)
                pf.display_preexisting_condition_history(self.nhs_number_child)
            self.connection.commit()

    def close_connection(self):
        self.connection.close()


# Erin = PatientMedical()
# Erin.vaccination("0123456789")
# Erin.cancer("0123456789")
# Erin.show_profile("0123456789")

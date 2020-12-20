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
                    menu_selection = input("Please select an option: ")
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
                    print("\n    < You entered an invalid value. Please type 1, 2, or 0 based on the menu>\n")
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
                                print("\n    < You have entered a wrong value. Please type Y as yes and N as no>\n")
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
                    name = 'your'
                    pf.update_patient_medical(name, nhs_number)  # create and use update function
            if menu_selection == "2":  # Parents can add vaccination history to their underage children
                answers_to_vac = []
                while True:
                    try:
                        self.status = input("Please enter the first name and last name "
                                            "of your child whose profile you would like to edit: ")
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
                        error_message = "\n    < Invalid NHS number>\n"
                        print(error_message)
                    except pf.InvalidNameFormatError:
                        print("\n    < Wrong name format."
                              "\nPlease only enter your child's first name and last name "
                              "separated with a space>\n")
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
                                print("\n    < You have entered a wrong value. Please type Y as yes and N as no>\n")
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
                    self.a.execute("""INSERT INTO vaccineHistory (nhsNumber, Status, DTap, HepC, HepB,
                                                        Measles, Mumps, Rubella, Varicella)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, patient_info)
                    self.connection.commit()
                else:
                    children_name = self.status + "'s"
                    pf.update_patient_medical(children_name, self.nhs_number_child)  # To update child's existing record

    def pre_existing_con(self, nhs_number):
        print("The following questions are concerned with your or your children's pre-existing conditions ")
        print("If neither you or your children has any known pre-existing conditions, please press 0 to exit")
        while True:
            print("*" * 44)
            print("Choose [1] provide your own pre-existing conditions if any"
                  "\nChoose [2] provide any pre-existing conditions for your children"
                  "\nChoose [0] exit")
            print("*" * 44)
            while True:
                try:
                    menu_choice = input("Please select an option: ")
                    if menu_choice == "0":
                        return 1
                    if not menu_choice:
                        raise pf.EmptyFieldError()
                    if menu_choice != "1" and menu_choice != "2" and menu_choice != "0":
                        raise pf.InvalidMenuSelectionError()
                except pf.EmptyFieldError:
                    error_message = pf.EmptyFieldError()
                    print(error_message)
                except pf.InvalidMenuSelectionError:
                    print("\n    < You entered an invalid value. Please type 1, 2, 3, or 0 based on the menu>\n")
                else:
                    break
            if menu_choice == "1":
                self.a.execute("""
                                SELECT * FROM preExistingCondition 
                                WHERE nhsNumber =? """, [nhs_number])
                patient_result = self.a.fetchall()

                while True:  # asking patient about existing medical conditions
                    try:
                        major_illness = input('Do you have any pre-existing conditions?'
                                                '\nIf so, please enter the name of the pre-existing condition using comma to '
                                                'separate different conditions. Otherwise, please enter 0: ').lower().split(',')
                        if major_illness == ["0"]:
                            return 1
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
                    # except ValueError:
                    #     print('\n    < Please enter a non-numeric value>\n')
                    else:
                        break
                condition = []
                for i in major_illness:
                    condition_record = tuple([nhs_number, i])
                    condition.append(condition_record)
                if not patient_result:
                    self.a.executemany("""INSERT INTO preExistingCondition(nhsNumber, conditionType) VALUES (?, ?)""",
                                       condition)
                    self.connection.commit()
                else:
                    determinator = []
                    for each_row in patient_result:
                        for each_record in condition:
                            if each_record[0] in each_row and each_record[1] in each_row:
                                print('Sorry, you have updated this condition before')
                                determinator.append('1')
                                break
                    if not determinator:
                        self.a.executemany("""
                                            INSERT INTO preExistingCondition(nhsNumber, conditionType) VALUES (?, ?)""",
                                            condition)
                        self.connection.commit()
            if menu_choice == "2":
                while True:
                    try:
                        self.child_name = input("Please enter the full name of your child whose profile you would like to edit: ").lower()
                        self.nhs_number_child = int(input("Please enter {}'s nhs number: ".format(self.child_name)))
                        full_name = self.child_name.split(' ')
                        if self.child_name == "0":
                            return 1
                        if not self.child_name:
                            raise pf.EmptyFieldError()
                        if not self.nhs_number_child:
                            raise pf.EmptyFieldError()
                        if len(str(self.nhs_number_child)) != 10:
                            raise pf.InvalidAnswerError()
                        if len(full_name) == 1 or len(full_name) < 2:
                            raise pf.InvalidNameFormatError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        error_message = "\n    < Invalid NHS number>\n"
                        print(error_message)
                    except pf.InvalidNameFormatError:
                        print("\n    < Wrong name format."
                              "Please enter your child's first name and last name separated with a space>\n")
                    except ValueError:
                        print('\n    < NHS number needs to be 10 - digit numeric values. Please enter again>\n')
                    else:
                        break
                self.a.execute("""SELECT * FROM preExistingCondition WHERE nhsNumber = ?""", [self.nhs_number_child])
                check_child_nhs = self.a.fetchall()
                while True:  # asking about children's existing medical conditions
                    try:
                        major_illness = input('Does {} have any pre-existing conditions?'
                        '\nIf so, please enter the name of the pre-existing condition using comma to '
                        'separate different conditions. Otherwise, please enter 0: '.format(self.child_name)).lower().split(',')
                        if major_illness == ['0']:
                            return 1
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
                    # except ValueError:
                    #     print('\n    < Please enter a non-numeric value or 0>\n')
                    else:
                        break
                condition = []
                for i in major_illness:
                    condition_record = tuple([self.nhs_number_child, i])
                    condition.append(condition_record)
                if not check_child_nhs:  # if child's nhs number does not exist in database, insert
                    self.a.executemany("""INSERT INTO preExistingCondition(nhsNumber, conditionType) VALUES (?, ?)""", condition)
                    self.connection.commit()
                else:
                    determinator = []
                    for each_row in check_child_nhs:
                        for each_record in condition:
                            if each_record[0] in each_row and each_record[1] in each_row:
                                print('Sorry, you have updated this condition before')
                                determinator.append('1')
                                break
                    if not determinator:
                        self.a.executemany("""
                                            INSERT INTO preExistingCondition(nhsNumber, conditionType) VALUES (?, ?)""",
                                            condition)
                        self.connection.commit()


    def med_allergy(self, nhs_number):
        print("The following questions are concerned with information about your or your children's medicine allergies if any")
        print("If neither you or your children has any known allergies to any medicine, please press 0 to exit")
        while True:
            print("*" * 44)
            print("Choose [1] provide information about your own medicine allergies if any"
                  "\nChoose [2] provide information about your or your children's medicine allergies if any"
                  "\nChoose [0] exit")
            print("*" * 44)
            while True:
                try:
                    menu_choice = input("Please select an option: ")
                    if menu_choice == "0":
                        return 1
                    if not menu_choice:
                        raise pf.EmptyFieldError()
                    if menu_choice != "1" and menu_choice != "2" and menu_choice != "0":
                        raise pf.InvalidMenuSelectionError()
                except pf.EmptyFieldError:
                    error_message = pf.EmptyFieldError()
                    print(error_message)
                except pf.InvalidMenuSelectionError:
                    print("\n    < You entered an invalid value. Please type 1, 2, or 0 based on the menu>\n")
                else:
                    break
            if menu_choice == "1":
                self.a.execute("""SELECT * FROM medAllergy WHERE nhsNumber =? """, [nhs_number])
                allergy_result = self.a.fetchall()
                while True:  # asking patient about existing medicine allergy
                    try:
                        med_allergy = input('Do you have any allergies to any medicines?'
                                                '\nIf so, please enter the name of the medicine using comma to '
                                                'separate different types. Otherwise, please enter 0: ').lower().split(',')
                        if med_allergy == ['0']:  # could be a bug. check
                            return 1
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
                    # except ValueError:
                    #     print('\n    < Please enter a non-numeric value>\n')
                    else:
                        break
                allergy = []
                for i in med_allergy:
                    allergy_record = tuple([nhs_number, i])
                    allergy.append(allergy_record)
                if not allergy_result:
                    self.a.executemany("""INSERT INTO medAllergy(nhsNumber, medName) VALUES (?, ?)""", allergy)
                    self.connection.commit()
                else:
                    determinator = []
                    for each_row in allergy_result:
                        for each_record in allergy:
                            if each_record[0] in each_row and each_record[1] in each_row:
                                print('Sorry, you have updated allergy for this medicine before')
                                determinator.append('1')
                                break
                    if not determinator:
                        self.a.executemany("""INSERT INTO medAllergy(nhsNumber, medName) VALUES (?, ?)""", allergy)
                        self.connection.commit()
            if menu_choice == "2":
                while True:
                    try:
                        self.child_name = input("Please enter the full name of your child whose profile you would like to edit: ").lower()
                        self.nhs_number_child = int(input("Please enter {}'s nhs number: ".format(self.child_name)))
                        full_name = self.child_name.split(' ')
                        if self.child_name == "0":
                            return 1
                        if not self.child_name:
                            raise pf.EmptyFieldError()
                        if not self.nhs_number_child:
                            raise pf.EmptyFieldError()
                        if len(str(self.nhs_number_child)) != 10:
                            raise pf.InvalidAnswerError()
                        if len(full_name) == 1 or len(full_name) < 2:
                            raise pf.InvalidNameFormatError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        error_message = "\n    < Invalid NHS number>\n"
                        print(error_message)
                    except pf.InvalidNameFormatError:
                        print("\n    < Wrong name format."
                              "Please enter your child's first name and last name separated with a space>\n")
                    except ValueError:
                        print('\n    < NHS number needs to be 10 - digit numeric values. Please enter again>\n')
                    else:
                        break
                self.a.execute("""SELECT * FROM medAllergy WHERE nhsNumber = ?""", [self.nhs_number_child])
                check_child_nhs2 = self.a.fetchall()
                while True:  # asking about children's medicine allergy
                    try:
                        med_allergy = input('Does {} have any allergies to any medicines?'
                                            '\nIf so, please enter the name of the medicine using comma to '
                                            'separate different types. Otherwise, please enter 0: '.format(self.child_name)).lower().split(',')
                        if med_allergy == ['0']:  # could be a bug if. check
                            return 1
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
                    # except ValueError:
                    #     print('\n    < Please enter a non-numeric value>\n')
                    else:
                        break
                allergy = []
                for a in med_allergy:
                    allergy_record = tuple([self.nhs_number_child, a])
                    allergy.append(allergy_record)
                if not check_child_nhs2:
                    self.a.executemany("""INSERT INTO medAllergy(nhsNumber, medName) VALUES (?, ?)""", allergy)
                    self.connection.commit()
                else:
                    determinator = []
                    for each_row in check_child_nhs2:
                        for each_record in allergy:
                            if each_record[0] in each_row and each_record[1] in each_row:
                                print('Sorry, you have updated allergy for this medicine before')
                                determinator.append('1')
                                break
                    if not determinator:
                        self.a.executemany("""INSERT INTO medAllergy(nhsNumber, medName) VALUES (?, ?)""", allergy)
                        self.connection.commit()

# Obtain cancer related data from the patient, and parent patient can insert and modify children's records
    def cancer(self, nhs_number):
        # cancerRelation: 1 (patient had cancer before),
                        # 0 (patient has not had cancer before),
                        # None, no immediate family has had cancer before
                        # or the family relation (i.e sister, brother, daughter, mother etc.) with whome has had cancer
        # query set up in the future if needed: WHERE cancerRelation != "1" AND != "0" AND != "None" AND cancerAge <50
        print("Thank you! The following questions are concerned with your medical history and "
              "the medical history of your family"
              "\n These questions are to assess the genetic risk of certain hereditary diseases.")
        while True:
            print("*"*44)
            print("Choose [1] provide your own cancer history"
                "\nChoose [2] provide family cancer history if any"
                "\nChoose [0] exit")
            print("*"*44)
            while True:
                try:
                    menu_choice = input("Please select an option: ")
                    if menu_choice == "0":
                        return 1
                    if not menu_choice:
                        raise pf.EmptyFieldError()
                    if menu_choice != "1" and menu_choice != "2" and menu_choice != "0":
                        raise pf.InvalidMenuSelectionError()
                except pf.EmptyFieldError:
                    error_message = pf.EmptyFieldError()
                    print(error_message)
                except pf.InvalidMenuSelectionError:
                    print("\n    < You entered an invalid value. Please type 1, 2, or 0 based on the menu>\n")
                else:
                    break
            print('Please enter your answers to the following questions with Y/N.')
            if menu_choice == "1":
                self.cancer_history = []
                while True:
                    try:
                        cancer = input('Have you ever been diagnosed with cancer: ').lower()
                        if cancer == '0':
                            return 1
                        if not cancer:
                            raise pf.EmptyFieldError()
                        if cancer != "y" and cancer != "n":
                            raise pf.InvalidAnswerError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        print("\n    < Wrong value entered. Please type Y as yes and N as no>\n")
                    else:
                        break
                if cancer == "y":
                    self.cancer_relation = "1"  # 1 means the patient has had cancer before
                    print("Please use commas when entering multiple values.")
                    while True:
                        try:
                            cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").lower().split(",")
                            if cancer_type == ['0']:
                                return 1
                            if cancer_type == ['']:
                                raise pf.EmptyFieldError()
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        # except pf.InvalidAnswerError:
                        #     print("\n    < Invalid answer. Please enter a non-numeric value>\n")
                        else:
                            break
                    for cancer_name in cancer_type:
                        c = cancer_name
                        if "cancer" in cancer_name:
                            c = cancer_name[-len(cancer_name):-6]
                        while True:
                            try:
                                cancer_age = int(input('How old were you when you were diagnosed with {} cancer: '.format(c)))
                                if cancer_age == 0:
                                    return 1
                                if not cancer_age:
                                    raise pf.EmptyFieldError()
                                # if type(cancer_age) is not int:
                                #     raise ValueError()
                                if cancer_age < 0 or cancer_age >= 150:
                                    raise pf.InvalidAnswerError()
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            except pf.InvalidAnswerError:
                                print("\n    < Invalid answer. Please enter the correct age>\n")
                            except ValueError:
                                print("\n    < Invalid answer. Please enter a numeric value>\n")
                            else:
                                break
                        row_record = [nhs_number, self.cancer_relation, cancer_name, cancer_age]
                        self.cancer_history.append(tuple(row_record))  # This is a list of tuples containing patient's cancer info that was just entered
                    self.a.execute("""
                                    SELECT * FROM cancer WHERE nhsNumber =?
                                    """, [nhs_number])
                    query_result = self.a.fetchall()
                    if not query_result:
                        self.a.executemany("""INSERT INTO cancer(nhsNumber, cancerRelation, cancerType, cancerAge)
                                    VALUES (?, ?, ?, ?)""", self.cancer_history)
                        self.connection.commit()
                    else:  # something is wrong in this else statement
                        determinator = []
                        for each_row in query_result:
                            for each_record in self.cancer_history:
                                if each_record[0] in each_row and each_record[1] in each_row and \
                                        each_record[2] in each_row and str(each_record[3]) in each_row:
                                    print('Sorry, you already updated this information before')
                                    determinator.append('1')
                                    break
                        if not determinator:
                            self.a.executemany("""INSERT INTO cancer(nhsNumber, cancerRelation, cancerType, cancerAge)
                                                                VALUES (?, ?, ?, ?)""", self.cancer_history)
                            self.connection.commit()

                else:
                    self.cancer_relation = "0"  # 0 means the patient has not had cancer before
                    self.cancer_history = [nhs_number, self.cancer_relation]
                    self.a.execute("""
                                    SELECT * FROM cancer WHERE nhsNumber =?
                                    """, [nhs_number])
                    query_result = self.a.fetchall()
                    if not query_result:
                        self.a.execute("""INSERT INTO cancer(nhsNumber, cancerRelation) 
                                          VALUES (?, ?)""", self.cancer_history)
                        self.connection.commit()
                    else:
                        determinator = []
                        for each_row in query_result:
                            if self.cancer_history[0] in each_row and self.cancer_history[1] in each_row:
                                print('Sorry, you already updated that you have never had cancer before')
                                determinator.append('1')
                                break
                        if not determinator:
                            self.a.execute("""INSERT INTO cancer(nhsNumber, cancerRelation) 
                                              VALUES (?, ?)""", self.cancer_history)
                            self.connection.commit()
            elif menu_choice == "2":
                self.cancer_history = []
                while True:
                    try:
                        cancer = input('Has anyone in your immediate family, parents, children, or siblings, '
                                       'ever been diagnosed with cancer: ').lower()
                        if cancer == '0':
                            return 1
                        if not cancer:
                            raise pf.EmptyFieldError()
                        if cancer != "y" and cancer != "n":
                            raise pf.InvalidAnswerError()
                    except pf.EmptyFieldError:
                        error_message = pf.EmptyFieldError()
                        print(error_message)
                    except pf.InvalidAnswerError:
                        print("\n    < You have entered a wrong value. Please type Y as yes and N as no>\n")
                    else:
                        break
                if cancer == "y":
                    while True:
                        try:
                            cancer_type = input("Please tell us the type(s) of cancer that was diagnosed: ").lower().split(",")
                            if cancer_type == ['0']:
                                return 1
                            if cancer_type == ['']:
                                raise pf.EmptyFieldError()
                        except pf.EmptyFieldError:
                            error_message = pf.EmptyFieldError()
                            print(error_message)
                        # except pf.InvalidAnswerError:
                        #     print("\n    < Invalid answer. Please enter a non-numeric value>\n")
                        else:
                            break
                    for cancer_name in cancer_type:
                        c = cancer_name
                        if "cancer" in cancer_name:
                            c = cancer_name[-len(cancer_name):-7]
                        while True:
                            try:
                                self.cancer_relation = input('What is your relation with this family member who was diagnosed with {} cancer: '.format(c)).lower()
                                if self.cancer_relation == '0':
                                    return 1
                                if self.cancer_relation == "":
                                    raise pf.EmptyFieldError()
                            except pf.EmptyFieldError:
                                error_message = pf.EmptyFieldError()
                                print(error_message)
                            # except pf.InvalidAnswerError:
                            #     print("\n    < Invalid answer. Please enter a non-numeric value>\n")
                            # except pf.InvalidNameFormatError:
                            #     print("\n    < Please do not use any special characters or punctuations in your answer>\n")
                            else:
                                break
                        while True:
                            try:
                                cancer_age = int(input('How old was the family member diagnosed with {} cancer: '.format(c)))
                                if cancer_age == 0:
                                    return 1
                                if cancer_age < 0 or cancer_age >= 150:
                                    raise pf.InvalidAnswerError()
                            #     if cancer_age == "":
                            #         raise pf.EmptyFieldError()
                            # except pf.EmptyFieldError:
                            #     error_message = pf.EmptyFieldError()
                            #     print(error_message)
                            except ValueError:
                                print("\n    < Invalid answer. Please enter a numeric value>\n")
                            except pf.InvalidAnswerError:
                                print("\n    < Invalid answer. Please enter a correct>\n")
                            # except pf.InvalidNameFormatError:
                            #     print("\n    < Please do not use any special characters or punctuations in your answer>\n")
                            else:
                                break
                        row_record = [nhs_number, self.cancer_relation, cancer_name, cancer_age]
                        self.cancer_history.append(tuple(row_record))
                    choice_cancer_relation = [1, 0, 'None']
                    self.a.execute("""
                                    SELECT * FROM cancer WHERE nhsNumber =? AND 
                                    cancerRelation != '1' AND 
                                    cancerRelation != '0' AND 
                                    cancerRelation != 'None'
                                    """, [nhs_number])
                    query_result = self.a.fetchall()
                    if not query_result:
                        self.a.executemany("""INSERT INTO cancer(nhsNumber, cancerRelation, cancerType, cancerAge)
                                    VALUES (?, ?, ?, ?)""", self.cancer_history)
                        self.connection.commit()
                    else:  # something is wrong in this else statement
                        determinator = []
                        for each_row in query_result:
                            print(each_row)
                            for each_record in self.cancer_history:
                                print(each_record)
                                if each_record[0] in each_row and each_record[1] in each_row and \
                                        each_record[2] in each_row and str(each_record[3]) in each_row:
                                    print('Sorry, you already updated this information before')
                                    determinator.append('1')
                                    break
                        if not determinator:
                            self.a.executemany("""INSERT INTO cancer(nhsNumber, cancerRelation, cancerType, cancerAge)
                                                                VALUES (?, ?, ?, ?)""", self.cancer_history)
                            self.connection.commit()
                else:
                    self.cancer_relation = "None"  # None means there is no cancer history in the patient's family
                    print("Wonderful! That means you do not likely have any genetic risk in any specific cancer "
                          "that we know so far based on your family medical history.")
                    self.cancer_history = [nhs_number, self.cancer_relation]
                    self.a.execute("""
                                    SELECT * FROM cancer WHERE nhsNumber =?
                                    """, [nhs_number])
                    query_result = self.a.fetchall()
                    if not query_result:
                        self.a.execute("""INSERT INTO cancer(nhsNumber, cancerRelation) VALUES (?, ?)""", self.cancer_history)
                        self.connection.commit()
                    else:
                        determinator = []
                        for each_row in query_result:
                            if self.cancer_history[0] in each_row and self.cancer_history[1] in each_row:
                                print('Sorry, you already updated this information before')
                                determinator.append('1')
                                break
                        if determinator == []:
                            self.a.execute("""INSERT INTO cancer(nhsNumber, cancerRelation) 
                                            VALUES (?, ?)""", self.cancer_history)
                            self.connection.commit()


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
                    profile = input("Please select an option: ")
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
                    print("\n    < You entered an invalid value. Please type 1, 2, or 0 based on the menu>\n")
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
                        print("\n    < Invalid answer. Please enter your child's full name with a space separating the first and last name>\n")
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

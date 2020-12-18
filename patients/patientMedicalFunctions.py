import sqlite3 as sql
connection = sql.connect('UCH.db')
a = connection.cursor()

"""Exceptions set up"""


class InvalidMenuSelectionError(Exception):
    pass


class InvalidNameFormatError(Exception):
    pass


class InvalidAnswerError(Exception):
    pass


class EmptyFieldError(Exception):
    def __init__(self):
        self.message = '\n    <Please enter a value>\n'
        super().__init__(self.message)


class InvalidConditionFormatError(Exception):
    def __init__(self):
        self.message = '\n    <Please enter N for no or the name of the condition>\n'
        super().__init__(self.message)


class InvalidAllergyFormatError(Exception):
    def __init__(self):
        self.message = '\n    <Please enter N for no or the name of the medicine>\n'
        super().__init__(self.message)


def update_patient_medical():
    pass


def display_cancer_history(nhs_number):
    a.execute("""
                SELECT * FROM cancer 
                WHERE nhsNumber =? AND 
                cancerRelation = 1 
                """, [nhs_number])
    patient_med_record = a.fetchall()
    a.execute("""
                SELECT * FROM cancer
                WHERE nhsNumber =? AND 
                cancerRelation IN (SELECT cancerRelation FROM cancer WHERE cancerRelation !=0 AND cancerRelation !=1 AND cancerRelation != ?)
                """, [nhs_number, 'None'])
    pati_rec = a.fetchall()
    if not patient_med_record and not pati_rec:
        print('\nNo patient or family cancer history\n')
    if not pati_rec and patient_med_record:
        print('No family cancer history\n')  # Show patient's cancer record
        rows = 0
        record = 0
        cancer_table = [nhs_number, 'Patient or family', 'Cancer type', 'Age']
        while rows < len(patient_med_record):
            count = 0
            for column in cancer_table:
                if column == nhs_number:
                    column = "NHS Number"
                    print(column, ':', patient_med_record[record][count])
                elif patient_med_record[record][count] == '1':
                    print(column, ':', 'the Patient')
                else:
                    print(column, ':', patient_med_record[record][count])
                count += 1
            print("*" * 18)  # separating each record of the patient
            record += 1
            rows += 1
        else:
            print('\n    <<Cancer record ends>>\n')
    if not patient_med_record and pati_rec:
        print('No cancer history for the patient\n')  # Show the family cancer record
        rows = 0
        record = 0
        cancer_table = [nhs_number, 'Patient or family', 'Cancer type', 'Age diagnosed']
        while rows < len(pati_rec):
            count = 0
            for column in cancer_table:
                if column == nhs_number:
                    pass
                else:
                    print(column, ':', pati_rec[record][count])
                count += 1
            print("*" * 18)  # separating each record of the patient
            record += 1
            rows += 1
        else:
            print('\n    <<Cancer record ends>>\n')
    else:
        rows = 0
        record = 0
        cancer_table = [nhs_number, 'Patient or family', 'Cancer type', 'Age']
        while rows < len(patient_med_record):
            count = 0
            for column in cancer_table:
                if column == nhs_number:
                    column = "NHS Number"
                    print(column, ':', patient_med_record[record][count])
                elif patient_med_record[record][count] == '1':
                    print(column, ':', 'the Patient')
                else:
                    print(column, ':', patient_med_record[record][count])
                count += 1
            print("*"*18)  # separating each record of the patient
            record += 1
            rows += 1

        rows = 0
        record = 0
        cancer_table = [nhs_number, 'Patient or family', 'Cancer type', 'Age diagnosed']
        while rows < len(pati_rec):
            count = 0
            for column in cancer_table:
                if column == nhs_number:
                    pass
                else:
                    print(column, ':', pati_rec[record][count])
                count += 1
            print("*" * 18)  # separating each record of the patient
            record += 1
            rows += 1
        else:
            print('\n    <<Cancer record ends>>\n')


def display_preexisting_condition_history(nhs_number):  # Display for pre-existing condition
    a.execute("""SELECT * FROM preExistingCondition WHERE nhsNumber =? """, [nhs_number])
    patient_med_record = a.fetchall()
    if not patient_med_record:
        print('    <<Pre-existing condition record begins>>\n')
        print('\nNo history of pre-existing conditions\n')
        print('\n    <<Pre-existing condition record ends>>\n')
    else:
        print('    <<Pre-existing condition record begins>>\n')
        rows = 0
        record = 0
        cancer_table = [nhs_number, 'Type of condition']
        while rows < len(patient_med_record):
            count = 0
            for column in cancer_table:
                if column == nhs_number:
                    column = "NHS Number"
                    print(column, ':', patient_med_record[record][count])
                else:
                    print(column, ':', patient_med_record[record][count])
                count += 1
            print("*" * 18)  # separating each record of the patient
            record += 1
            rows += 1
        else:
            print('\n    <<Pre-existing condition record ends>>\n')


def medical_history_menu():
    print('Choose [1] provide vaccination history for you or your children'
          '\nChoose [2] provide other medical history for you or your children'
          '\nChoose [0] exit')

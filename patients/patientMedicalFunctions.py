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
        self.message = '    <Please enter a value>'
        super().__init__(self.message)


def update_patient_medical():
    pass


def display_medical_history(nhs_number):
    a.execute("""
                SELECT * FROM cancer 
                WHERE nhsNumber =? AND 
                cancerRelation IN (SELECT cancerRelation FROM vaccineHistory WHERE cancerRelation != 0) 
                AND cancerRelation IN (SELECT cancerRelation FROM vaccineHistory 
                WHERE cancerRelation != None)""", [nhs_number])
    patient_med_record = a.fetchall()
    if not patient_med_record:
        print('No patient or family cancer history')
    else:
        rows = 0
        record = 0
        cancer_table = [nhs_number, 'cancer relation', 'cancer type', 'age']
        while rows < len(patient_med_record):
            count = 0
            for column in cancer_table:
                print(column + ':' + patient_med_record[record][count])
                count += 1
            print("*"*10)  # separating each record of the patient
            record += 1
            rows += 1
        # add display for pre-existing condition

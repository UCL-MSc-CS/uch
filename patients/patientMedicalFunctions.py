import sqlite3 as sql
connection = sql.connect('UCH.db')  # establish the connection to the UCH database file
a = connection.cursor()


class InvalidMenuSelectionError(Exception):
    """
    Error class for when the user enters a numeric value not given by the menu selection.
    """
    pass


class InvalidNameFormatError(Exception):
    """
    Error class for when the user enters the wrong format for names.
    """
    pass


class InvalidAnswerError(Exception):
    """
    Error class for when the user enters an invalid answer.
    """
    pass


class EmptyFieldError(Exception):
    """
    Error class for when the user enters an empty field.
    """
    def __init__(self):
        """
        The constructor for EmptyFieldError class.
        """
        self.message = '\n    < Please enter a value >\n'
        super().__init__(self.message)


class InvalidConditionFormatError(Exception):
    """
    Error class for when the user enters a wrong format for the pre-existing condition function.
    """
    def __init__(self):
        """
        The constructor for InvalidConditionFormatError class.
        """
        self.message = '\n    < Please enter N for no or the name of the condition >\n'
        super().__init__(self.message)


class InvalidAllergyFormatError(Exception):
    """
    Error class for when the user enters a wrong format for the medicine allergy function.
    """
    def __init__(self):
        """
        The constructor for InvalidAllergyFormatError class.
        """
        self.message = '\n    < Please enter N for no or the name of the medicine >\n'
        super().__init__(self.message)


def update_patient_medical(name, nhs_number):
    """
    The function allows the patient to update the specified vaccination record.

    Patient will choose which vaccination result he or she would like to update based on the menu provided. The function
    will replace the '0' in the database for the specified vaccine with '1'. '0' means no and '1' means yes. The
    function also prevents the patient from entering repeated information. If patient forgets that he or she has updated
    the answer to a vaccine to yes before, the function will display a message informing the patient. This function is
    also used to update the patient's children's vaccination records.

    Parameters:
        name: 'you' or the name of the child.
        nhs_number: the patient's or the child's NHS number.
    Returns:
        1 (int): exit the function when patient enters 0.
    """

    print('Our system shows that you have provided {} vaccination history before'
          '\nPlease update any specific vaccination on the menu below'.format(name))
    while True:
        a.execute("""
                    SELECT * FROM vaccineHistory WHERE nhsNumber =?
                    """, [nhs_number])
        update_record = a.fetchall()
        count_record = 2
        new_record = []
        vaccination_history = ["DTap", "HepC", "HepB",
                               "Measles", "Mumps", "Rubella", "Varicella"]
        print('*'*44)
        print('Choose [1] DTap'
            '\nChoose [2] HepC'
            '\nChoose [3} HepB'
            '\nChoose [4] Measles'
            '\nChoose [5] Mumps'
            '\nChoose [6] Rubella'
            '\nChoose [7] Varicella'
              '\nChoose [0] exit')
        print('*' * 44)
        while True:
            try:
                menu = int(input('Please choose 1 vaccine you would like to update from the menu above: '))
                if menu == 0:
                    return 1
                if menu not in range(1, 8):
                    raise InvalidMenuSelectionError()
            except InvalidMenuSelectionError:
                print('\n    < Please enter a single number from the above menu >\n')
            except ValueError:
                print('\n    < Please enter a single numeric value >\n')
            else:
                break

        while count_record <= 8:
            new_record.append(update_record[0][count_record])
            count_record += 1
        if new_record[menu-1] == 0:
            new_record[menu-1] = 1
            new_record.insert(7, nhs_number)
            a.execute("""
                        UPDATE vaccineHistory
                        SET DTap = ?, HepC = ?, HepB = ?, Measles = ?, Mumps = ?, Rubella = ?, Varicella = ?
                        WHERE nhsNumber = ?
                        """, new_record)
        else:
            print('You have had this vaccination before'
                  '\nFor any booster update, our GP will automatically update this information for you')
        connection.commit()


def display_cancer_history(nhs_number):
    """
    This function will display the cancer history of the patient and the patient's immediate family.

    Parameters:
        nhs_number: patient's NHS number.
    """

    a.execute("""
                SELECT * FROM cancer 
                WHERE nhsNumber =? AND 
                cancerRelation = 1 
                """, [nhs_number])
    patient_med_record = a.fetchall()  # list of tuples of cancers patient previously had
    a.execute("""
                SELECT * FROM cancer
                WHERE nhsNumber =? AND 
                cancerRelation IN (SELECT cancerRelation FROM cancer WHERE cancerRelation !=0 AND cancerRelation !=1 AND cancerRelation != ?)
                """, [nhs_number, 'None'])
    pati_rec = a.fetchall()  # list of tuples of cancers patient's immediate family previously had
    if not patient_med_record and not pati_rec:  # if no cancer history exist in the database under the entered NHS number
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
            print("*" * 18)  # separating each row of record
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
            print("*" * 18)  # separating each row of record
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
            print("*"*18)  # separating each row of record
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
            print("*" * 18)  # separating each row of record
            record += 1
            rows += 1
        else:
            print('\n    <<Cancer record ends>>\n')


def display_preexisting_condition_history(nhs_number):
    """
    This function displays all the pre-existing conditions the patient and the patient's children have.

    Parameters:
        nhs_number: the NHS number of the patient or patient's specified child.
    """

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
            print("*" * 18)  # separating each row of record
            record += 1
            rows += 1
        else:
            print('\n    <<Pre-existing condition record ends>>\n')

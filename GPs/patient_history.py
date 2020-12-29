import patients.patient_medical_functions as pm

"""
Used to display patient history.

Can display cancer history as well as pre-existing conditions.
"""
def patient_history(nhs_number):
    while True:
        print("--------------------------------------------")
        print("\t Patient History Menu")
        print("--------------------------------------------")
        print("Choose [1] to display cancer history")
        print("Choose [2] to display pre-existing condition history")
        print("Choose [0] to return to appointment menu")
        option = input("Please select an option: ")
        if option == "1":
            pm.display_cancer_history(nhs_number)
        elif option == "2":
            pm.display_preexisting_condition_history(nhs_number)
        elif option == "0":
            print("Returning to appointment menu.....")
            print("********************************************")
            break
        else:
            print("\n\t< Invalid option chosen. Please try again >\n")
        print("********************************************")
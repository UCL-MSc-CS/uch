import patients.patientMedicalFunctions as pm

def patienthistory(doctoremail,appointmentid,nhsNumber):
    while True:
        print("--------------------------------------------")
        print("\t Patient History Menu")
        print("--------------------------------------------")
        print("Choose [1] to display cancer history")
        print("Choose [2] to display prexisting condition history")
        print("Choose [0] to return to appointment menu")
        option = input(":")
        if option == "1":
            pm.display_cancer_history(nhsNumber)
        elif option == "2":
            pm.display_preexisting_condition_history(nhsNumber)
        elif option == "0":
            print("Returning to appointment menu.....")
            print("********************************************")
            break
        else:
            print("\t<Invalid option chosen. Please try again>")
        print("********************************************")
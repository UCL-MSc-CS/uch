import admins
import patients.patientMain as pm
import GPs.gp_main as gpm
import sys
import useful_functions as uf
import os.path
from database import initialise_database


class Menus():
    """This is a class containing menus used on the first page and the Admin side of the program."""

    def master_menu(self):
        print("--------------------------------------------")
        print("         UCH Management System   ")
        print("--------------------------------------------")
        print("Welcome, please login")
        print("Choose [1] for Admin")
        print("Choose [2] for Patient")
        print("Choose [3] for GP")
        print("Choose [0] to close the program")

    def admin_menu(self):
        uf.banner('Admin')
        print("Choose [1] to add a new doctor")
        print("Choose [2] to deactivate/reactivate or delete a profile")
        print("Choose [3] to confirm/un-confirm patient registrations")
        print("Choose [4] to check in/out a patient")
        print("Choose [5] to change patient details")
        print("Choose [0] when finished navigating menu")

    def admin_submenu2(self):
        print("********************************************")
        print("choose [1] to deactivate a profile")
        print("choose [2] to reactivate a profile")
        print("choose [3] to delete a profile")
        print("choose [0] when finished navigating menu.")
        print("********************************************")

    def admin_submenuCheckIO(self):
        print("Choose [1] to check patient in")
        print("Choose [2] to check patient out")
        print("Choose [0] to go back")

    def manage_details(self):
        print("Choose [1] to change patient record")
        print("Choose [2] to delete patient record")
        print("Choose [0] to go back")

    def manage_details2(self):
        print("Choose [1] to alter entire patient record")
        print("Choose [2] to alter part of patient record")
        print("Choose [0] to go back")


""" This is the main loop"""
while True:
    try:

        if os.path.isfile('UCH.db') and os.path.getsize('UCH.db') > 0:
            pass
        else:
            print("Initializing the Database please allow a few seconds before login begins...")
            initialise_database()

        masterlogin = Menus()
        masterlogin.master_menu()

        selection1 = int(input("Please select an option: "))
        while selection1 == 0 or selection1 == 1 or selection1 == 2 or selection1 == 3:
            while selection1 == 2:
                p_choice = pm.task()
                if p_choice == 0:
                    masterlogin.master_menu()
                    selection1 = int(input("Please select an option: "))

            while selection1 == 3:
                gpChoice = gpm.gp_start()
                if gpChoice == "exitGPLogin":
                    masterlogin.master_menu()
                    selection1 = int(input("Please select an option: "))

            while selection1 == 1:
                ad = admins.AdminFunctions()
                logged_in = ad.admin_login()

                while logged_in == True:

                    AdminM = Menus()
                    AdminM.admin_menu()
                    ad.check_registrations()

                    try:
                        selection = int(input("Please select an option: "))

                        while selection != 0:
                            while selection == 1:
                                print("********************************************")
                                selection = ad.add_doctor()
                                
                            while selection == 2:
                                AdminM.admin_submenu2()
                                ipt = ''
                                while ipt == '':
                                    try:
                                        ipt = int(input("Please select an option: "))
                                    except ValueError:
                                        print("\n   < Please provide a numerical input >\n")

                                while ipt != 1 and ipt != 2 and ipt != 3 and ipt != 0:
                                    try:
                                        print('\n   < Not a valid input, please enter a number between 0 and 2>\n')
                                        ipt = int(input("Please select an option: "))
                                    except ValueError:
                                        continue
                                if ipt == 1:
                                    selection = ad.deactivate_doctor()
                                if ipt == 2:
                                    selection = ad.reactivate_doctor()
                                if ipt == 3:
                                    selection = ad.delete_doctor()
                                if ipt == 0:
                                    selection = 0

                            while selection == 3:
                                print("********************************************")
                                print("choose [1] to confirm a registration")
                                print("choose [2] to un-confirm a registration")
                                print("choose [0] when finished navigating menu.")
                                print("********************************************")
                                ipt = ''
                                while ipt == '':
                                    try:
                                        ipt = int(input("Please select an option: "))
                                    except ValueError:
                                        print("   < Please provide a numerical input >")

                                while ipt != 1 and ipt != 2 and ipt != 0:
                                    print('Not a valid input')
                                    ipt = int(input("Please select an option: "))
                                if ipt == 1:
                                    selection = ad.confirm_registrations()
                                if ipt == 2:
                                    selection = ad.unconfirm_registrations()
                                if ipt == 0:
                                    selection = 0
                                
                            if selection == 4:
                                print("********************************************")
                                AdminM.admin_submenuCheckIO()
                                print("********************************************")
                                try:
                                    CheckOpt = int(input("Choice: "))
                                    if CheckOpt == 1:
                                        ad.c_in()  # Calling check-in function from admins
                                    elif CheckOpt == 2:
                                        ad.c_out()  # Calling check-out function from admins
                                    elif CheckOpt == 0:
                                        selection = 0
                                    else:
                                        print("< Not a valid option >")
                                except ValueError:

                                    print("< Not a valid choice >")

                            elif selection == 5:
                                print("********************************************")
                                AdminM.manage_details()
                                print("********************************************")
                                try:
                                    det_choice = int(input("Choice: "))
                                    back_var = 0
                                    if det_choice == 1:
                                        while back_var == 0:
                                            try:
                                                print("********************************************")
                                                AdminM.manage_details2()
                                                print("********************************************")
                                                det_choice2 = int(input("Choice: "))
                                                if det_choice2 == 1:
                                                    ad.manage_det()  # Calling function that changes all details
                                                elif det_choice2 == 2:
                                                    ad.man_ind_det()  # Calling function that changes individual details
                                                elif det_choice2 == 0:
                                                    back_var = 1
                                                    break
                                                elif det_choice2 != 1 and det_choice2 != 2 and det_choice2 != 0:
                                                    raise ValueError
                                            except ValueError:
                                                print("< Not a valid choice >")
                                    elif det_choice == 2:
                                        ad.del_pat()
                                    elif det_choice == 0:
                                        selection = 0
                                    elif det_choice != 0 and det_choice != 1 and det_choice != 2:
                                        print("< Not a valid option >")
                                except ValueError:
                                    print("< Not a valid option >")

                            elif selection > 5 or selection < 0:
                                print("Not a valid selection, please enter a number between 0 and 5")
                                break
                            if selection == 0:
                                AdminM.admin_menu()
                                ad.check_registrations()
                                selection = int(input("Please select an option: "))

                        if selection == 0:
                            logged_in = "restart"
                    except ValueError:
                        print("\n   < Please enter a number > \n")
                while logged_in == False:
                    print("\n   < Incorrect password > \n")
                    logged_in = "entering details"
                if logged_in == "restart":
                    ad.commit_and_close()
                    masterlogin.master_menu()
                    selection1 = int(input("Please select an option: "))
            if selection1 == 0:
                raise KeyboardInterrupt
        if selection1 != 0 or selection1 != 1 or selection1 != 2 or selection1 != 3:
            print("\n   < Please enter a number between 0 and 3 >\n")
            continue

    except ValueError:
        print("\n   < Please enter a number >\n")
    except KeyboardInterrupt:
        print("Closing program")
        sys.exit()
    except EOFError:
        print("Closing program")
        sys.exit()

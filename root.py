import pandas as pd
import Admins
import sqlite3 as sql
from datetime import datetime as dt
import time
import patients.patientMain as pm
import GPs.GPMain as gpm
import sys
import usefulfunctions as uf

class Menus():
    def MasterMenu(self):
        print("Welcome, please login")
        print("Choose [1] for Admin")
        print("Choose [2] for Patient")
        print("Choose [3] for GP")

    def adminmenu(self):
        uf.banner('Admin')
        print("Choose [1] to add a new doctor")
        print("Choose [2] to deactivate or delete a profile")
        print("Choose [3] to confirm/un-confirm patient registrations")
        print("Choose [4] to check in/out a patient")
        print("Choose [5] to change patient details")
        print("Choose [0] when finished navigating menu")

    def admin_submenu2(self):
        print("********************************************")
        print("choose [1] to deactivate a profile")
        print("choose [2] to delete a profile")
        print("choose [0] when finished navigating menu.")
        print("********************************************")

    def admin_submenuCheckIO(self):
        print("Choose [1] to check patient in")
        print("Choose [2] to check patient out")
        print("Choose [0] to go back")

    def managedetails(self):
        print("Choose [1] to change patient record")
        print("Choose [2] to delete patient record")
        print("Choose [0] to go back")

    def managedetails2(self):
        print("Choose [1] to alter entire patient record")
        print("Choose [2] to alter part of patient record")
        print("Choose [0] to go back")




""" This is the main loop"""
while True:
    try:
        masterlogin = Menus()
        masterlogin.MasterMenu()


        selection1 = int(input("Please select an option: "))
        while selection1 != 0:
            if selection1 == 2:
                selection1 = pm.task()
            elif selection1 == 3:
                # # todo replace hard code with function call.
                # email = input("Please enter your email address: ")
                # password = input("Please enter your password: ")

                # with sql.connect("UCH.db") as db:
                #     c = db.cursor()
                # find_doctor = ("SELECT * FROM GP WHERE gpEmail =? AND password =?")

                # # avoid using %s as this is vulnerable to injection attacks.
                # c.execute(find_doctor, [(email), (password)])
                # results = c.fetchall()

                # if results:
                #     for i in results:
                #         print("Welcome " + i[2])
                #     selection1 = 0

                # else:
                #     print("Email and password not recognised")
                #     again = input("Do you want to try again?(y/n)")
                #     if again.lower() == "n":
                #         print("Goodbye")
                #         time.sleep(1)
                #         selection1 = 0
                gpm.gpStart()


            while selection1 == 1:
                ad = Admins.adminFunctions()
                logged_in = ad.admin_login()

                while logged_in == True:

                    AdminM = Menus()
                    AdminM.adminmenu()
                    ad.check_registrations()
                    
                    try:
                        selection = int(input("please select an option: "))

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
                                        print("   < Please provide a numerical input >")

                                while ipt != 1 and ipt != 2 and ipt != 0:
                                    print('Not a valid input')
                                    ipt = int(input("please select an option: "))
                                if ipt == 1:
                                    selection = ad.deactivate_doctor()
                                if ipt == 2:
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
                                    ipt = int(input("please select an option: "))
                                if ipt == 1:
                                    selection = ad.confirm_registrations()
                                if ipt == 2:
                                    selection = ad.unconfirm_registrations()
                                if ipt == 0:
                                    selection = 0
                                
                            #checking patient in or out

                            if selection == 4:
                                AdminM.admin_submenuCheckIO()
                                try:
                                    CheckOpt = int(input("choice: "))
                                    if CheckOpt == 1:
                                        ad.cin()
                                    elif CheckOpt == 2:
                                        ad.cout()
                                        print("successfully checked patient out")
                                    elif CheckOpt == 0:
                                        selection = 0
                                    else:
                                        print("< Not a valid option >")
                                except ValueError:
                                    print("< Not a valid choice >")

                            #updating/deleting patient details
                            elif selection == 5:
                                print("********************************************")
                                AdminM.managedetails()
                                print("********************************************")
                                try:
                                    detchoice = int(input("choice: "))
                                    backvar = 0
                                    if detchoice == 1:
                                        while backvar == 0:
                                            try:
                                                print("********************************************")
                                                AdminM.managedetails2()
                                                print("********************************************")
                                                detchoice2 = int(input("choice: "))
                                                if detchoice2 == 1:
                                                    ad.managedet()
                                                elif detchoice2 == 2:
                                                    ad.manIndDet()
                                                elif detchoice2 == 0:
                                                    backvar = 1
                                                    break
                                                elif detchoice2 != 1 and detchoice2 != 2 and detchoice2 != 0:
                                                    raise ValueError
                                            except ValueError:
                                                print("< Not a valid choice >")
                                    elif detchoice == 2:
                                        ad.delpatdet()
                                    elif detchoice == 0:
                                        selection = 0
                                    elif detchoice != 0 and detchoice != 1 and detchoice != 2:
                                        print("< Not a valid option >")
                                except ValueError:
                                    print("< Not a valid option >")

                            elif selection > 5 or selection < 0:
                                print("Not a valid selection, please enter a number between 0 and 5")
                                AdminM.adminmenu()
                                ad.check_registrations()
                                selection = int(input("please select an option: "))
                            if selection == 0:
                                AdminM.adminmenu()
                                ad.check_registrations()
                                selection = int(input("please select an option: "))


                            # print("exiting menu")
                        if selection == 0:
                            logged_in = "restart"
                    except ValueError:
                        print("\n   < Please enter a number > \n")
                while logged_in == False:
                    print("\n   < Incorrect username/password > \n")
                    logged_in = "entering details"
                if logged_in == "restart":
                    ad.commit_and_close()
                    masterlogin.MasterMenu()
                    selection1 = int(input("please select an option: "))
    except ValueError:
        print("\n   < Please enter a number >\n")
    except KeyboardInterrupt:
        print("Closing program")
        sys.exit()
    except EOFError:
        print("Closing program")
        sys.exit()

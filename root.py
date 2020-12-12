import pandas as pd
import Admins
import sqlite3 as sql
from datetime import datetime as dt
import time
import patients.patientMain as pm
import GPs.GPMain as gpm

class Menus():
    def MasterMenu(self):
        print("Welcome, please login")
        print("choose [1] for Admin")
        print("choose [2] for Patient")
        print("choose [3] for GP")

    def adminmenu(self):
        print("Welcome admin")
        print("choose [1] to add a new GP/Physician")
        print("choose [2] to deactivate or delete a profile")
        print("choose [3] to confirm patient registration")
        print("choose [4] to check patient details")
        print("choose [5] to append patient check in/out")
        print("choose [6] to change patient details")
        print("choose [0] when finished navigating menu")

    def admin_submenu2(self):
        print("choose [1] to deactivate a profile")
        print("choose [2] to delete a profile")
        print("choose [0] when finished navigating menu.")

    def admin_submenuCheckIO(self):
        print("choose [1] to check patient in")
        print("choose [2] to check patient out")
        print("choose [0] to go back")

    def managedetails(self):
        print("choose [1] to change patient record")
        print("choose [2] to delete patient record")
        print("choose [0] to go back")

    def managedetails2(self):
        print("choose [1] to alter entire patient record")
        print("choose [2] to alter part of patient record")
        print("choose [0] to go back")




""" This is the main loop"""
masterlogin = Menus()
masterlogin.MasterMenu()


selection1 = int(input("choice: "))
while selection1 != 0:
    if selection1 == 2:
        pm.task()
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
        print(logged_in)

        while logged_in == True:
            ad.check_registrations()

            AdminM = Menus()
            AdminM.adminmenu()
            
            try:
                selection = int(input("please select an option: "))
                if selection == 0:
                    logged_in = "restart"

                while selection != 0:
                    while selection == 1:
                        print("registering new physician")
                        create = int(input("choose [1] to input physician or [2] to exit: "))
                        while create != 1 and create != 2:
                            print('please enter 1 or 2')
                            create = int(input("choose [1] to input physician or [2] to exit: "))
                        if create == 1:
                            selection = ad.add_doctor()
                        elif create == 2:
                            selection = 0
                    while selection == 2:
                        AdminM.admin_submenu2()
                        ipt = int(input("please select an option: "))
                        while ipt != 1 and ipt != 2 and ipt != 0:
                            print('not a valid input')
                            ipt = int(input("please select an option: "))
                        if ipt == 1:
                            selection = ad.deactivate_doctor()
                        if ipt == 2:
                            selection = ad.delete_doctor()
                        if ipt == 0:
                            selection = 0
                    if selection == 3:
                        ad.confirm_registrations()
                        selection = 0
                    #checking patient in or out

                    elif selection == 5:
                        AdminM.admin_submenuCheckIO()
                        CheckOpt = int(input("choice: "))
                        if CheckOpt == 1:
                            ad.cin()
                        elif CheckOpt == 2:
                            ad.cout()
                            print("successfully checked patient out")
                        elif CheckOpt == 0:
                            selection = 0
                        else:
                            print("not a valid option")

                    #updating/deleting patient details
                    elif selection == 6:
                        AdminM.managedetails()
                        detchoice = int(input("choice: "))

                        if detchoice == 1:
                            AdminM.managedetails2()
                            detchoice2 = int(input("choice: "))
                            if detchoice2 == 1:
                                ad.managedet()
                            elif detchoice2 == 2:
                                ad.manIndDet()
                            elif detchoice2 == 0:
                                selection = 6
                            elif detchoice2 != 1 and detchoice2 != 2 and detchoice2 != 0:
                                print("Not a valid choice")
                        elif detchoice == 2:
                            ad.delpatdet()
                        elif detchoice == 0:
                            selection = 0
                        elif detchoice != 0 and detchoice != 1 and detchoice != 2:
                            print("Not a valid option")



                    else:
                        print("not a valid selection")

                        AdminM.adminmenu()
                        selection = int(input("please select an option: "))

                    print("exiting menu")
                while logged_in == False:
                    print("incorrect username/password")
                    logged_in = "entering details"
                if logged_in == "restart":
                    ad.commit_and_close()
                    masterlogin.MasterMenu()
                    selection1 = int(input("please select an option: "))
            except ValueError:
                print("please enter a number")

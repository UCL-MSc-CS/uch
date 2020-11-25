import pandas as pd
import class_example
import Admins

cl = class_example.printstuff()
cl.printhello()


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
        print("choose [0] when finished navigating menu")

    def admin_submenu2(self):
        print("choose [1] to deactivate a profile")
        print("choose [2] to delete a profile")
        print("choose [0] when finished navigating menu")


""" This is the main loop"""
masterlogin = Menus()
masterlogin.MasterMenu()


selection1 = int(input("choice: "))
while selection1 != 0:
    if selection1 == 2:
        #call code for patient
        pass
    elif selection1 == 3:
        #call code for GP
        pass

    elif selection1 == 1:
        username = input('Username: ')
        password = input('Password: ')

        admin_df = pd.read_excel("Admins Data.xlsx", index_col= 0)
        user_series = pd.Series([password], index = [username])
        system_series = admin_df.loc[username]

        if str(system_series['Password']) == user_series[username]:
            logged_in = True
            print('logged in')
            while logged_in == True:
                ad = Admins.adminFunctions()
                ad.check_registrations()

                AdminM = Menus()
                AdminM.adminmenu()

                selection = int(input("please select an option: "))

                while selection != 0:
                    if selection == 1:
                        ad.add_doctor()
                    elif selection == 2:
                        AdminM.admin_submenu2()
                        ipt = int(input("choice: "))
                        if ipt == 1:
                            ad.deactivate_doctor()
                        if ipt == 2:
                            pass
                        if ipt == 0:
                            selection = 0
                    elif selection == 3:
                        ad.confirm_registrations()

                    else:
                        print("not a valid selection")

                        AdminM.adminmenu()
                        selection = int(input("please select an option: "))

                print("exiting menu")
                ad.commit_and_close()
            else:
                print("not a valid selection")
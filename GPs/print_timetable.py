from datetime import datetime, timedelta
import useful_functions as uf
from GPs.print_day import print_day

"""
For a given week, print out all the days in that week and their appointments.

Called from the main "print_timetable()" function below.
"""
def print_days(date, gp_email):
    start_date = date - timedelta(days=date.weekday())
    end_date = start_date + timedelta(days=6)
    for single_date in uf.date_range(start_date, end_date):
        print_day(single_date, gp_email)


"""
Main timetable menu for a Doctor.

Can view: 
The current week, 
Next week, 
Or enter a date of which the entire week that date belongs to will be displayed.

Be careful, the timetable only displays accepted/confirmed patient appointments.
Will not display patient appointments that are booked as pending/declined as these categories are not 
considered to have been added to the GPs schedule yet.
Asks for user input after printing the timetable to stop the terminal from immediately jumping back to the main menu.
"""
def print_timetable(gp_email):
    while True:
        now = datetime.today()
        today = datetime(now.year, now.month, now.day)
        print("--------------------------------------------")
        print("\t Doctor Timetable")
        print("--------------------------------------------")
        print("Select option below to view weekly timetable:")
        print("Choose [1] to view this week")
        print("Choose [2] to view next week")
        print("Choose [3] to view any other week.")
        print("Choose [0] to return to the main menu.")
        option = input("Please select an option: ")
        try:
            if int(option) == 1:
                print_days(today, gp_email)
                choice=input("\nPress [0] to go back to Timetable menu, any other button to return to Main menu....")
                if choice == '0':
                    continue
                else:
                    break
            elif int(option) == 2:
                print_days(today + timedelta(7), gp_email)
                choice=input("\nPress [0] to go back to Timetable menu, any other button to return to Main menu....")
                if choice == '0':
                    continue
                else:
                    break
            elif int(option) == 3:
                selected_date = uf.validate_date("Please enter a date to view its weekly timetable")
                if selected_date == 'exit':
                    continue
                print_days(selected_date, gp_email)
                choice=input("\nPress [0] to go back to Timetable menu, any other button to return to Main menu....")
                if choice == '0':
                    continue
                else:
                    break
            elif int(option) == 0:
                break
            else:
                print("\n\t< Invalid option choice, please try again >\n")
        except ValueError:
            print("\n\t< You didn't enter a number please try again >\n")

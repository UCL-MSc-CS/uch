from datetime import datetime, timedelta
import usefulfunctions as uf
from GPs.printday import printday


def printdays(date, doctoremail):
    start_date = date - timedelta(days=date.weekday())
    end_date = start_date + timedelta(days=6)
    for single_date in uf.daterange(start_date, end_date):
        printday(single_date, doctoremail)


def printtimetable(doctoremail):
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
        option = input(":")
        try:
            if int(option) == 1:
                printdays(today, doctoremail)
                input("\nPress any button to continue....")
                break
            elif int(option) == 2:
                printdays(today + timedelta(7), doctoremail)
                input("\nPress any button to continue....")
                break
            elif int(option) == 3:
                selected_date = uf.validatedate("Please enter a date to view its weekly timetable")
                printdays(selected_date, doctoremail)
                input("\nPress any button to continue....")
                break
            elif int(option) == 0:
                break
            else:
                print("\t<Invalid option choice, please try again>")
        except:
            print("\t<You didn't enter a number please try again>")

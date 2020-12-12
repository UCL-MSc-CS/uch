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
        print("Select option below to view weekly timetable:")
        print("choose [1] to view this week")
        print("choose [2] to view next week")
        print("choose [3] to view any other week.")
        print("choose [4] to return to the main menu.")
        option = input(":")
        try:
            if int(option) == 1:
                printdays(today, doctoremail)
                input("\n\nPress any button to continue....")
                break
            elif int(option) == 2:
                printdays(today + timedelta(7), doctoremail)
                input("\n\nPress any button to continue....")
                break
            elif int(option) == 3:
                selected_date = uf.validatedate("Please enter a date to view its weekly timetable")
                printdays(selected_date, doctoremail)
                input("\n\nPress any button to continue....")
                break
            elif int(option) == 4:
                break
            else:
                print("invalid option choice, please try again")
        except:
            print("You didn't enter a number please try again")

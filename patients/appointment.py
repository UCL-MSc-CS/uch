import sqlite3 as sql
import calendar


class Appointment:

    def __init__(self):
        self.connection = sql.connect('AppCalendar.db')
        self.c = self.connection.cursor()

    def chooseDoctor(self):
        pass

    def bookAppointment(self):
        print(calendar.month(2021, 1))
        day = int(input("Please select a day in January: "))
        # amend error handling
        if day <= 0 or day > 31:
            day = int(input("This is not a valid day."
                            "\nPlease select a day in January: "))
        date = "{:0>2}/01/2021".format(day)

        print("This is the current availability on your chosen date: ")
        self.c.execute("SELECT time, bookedStatus FROM Appointment WHERE date =?", [date])
        appointments = self.c.fetchall()
        for app in appointments:
            print(app[0] + "\t\t" + app[1])

        options = int(input("Choose [1] to select a time or [2] to select another date or [3] to exit: "))
        if options == 1:
            time = input("Please choose a time from the available appointments: ")
            # add in error handling
            chosen = [time, date]
            self.c.execute("UPDATE Appointment SET bookedStatus = 'Booked' WHERE time =? and date=?", chosen)
            self.connection.commit()
            self.connection.close()
            print("You have booked an appointment on {} at {}".format(date, time))

        if options == 2:
            self.bookAppointment()

        if options == 3:
            pass

    def cancelAppointment(self):
        pass



ari = Appointment()
ari.bookAppointment()


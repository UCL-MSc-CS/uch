import sqlite3 as sql
import calendar
import random
from datetime import time as x, date as xyz, datetime, timedelta
import time
import patientFunctions as pf


class Appointment:

    def __init__(self):
        self.connection = sql.connect('patient.db')
        self.c = self.connection.cursor()

    def bookAppointment(self, patientEmail):
        print("**********"
              "\n[1] to book an appointment"
              "\n[2] to view your confirmed appointments"
              "\n[3] to cancel an appointment"
              "\n[0] to exit to the main menu: ")
        options = int(input("Please choose from the options above: "))
        if options == 1:
            a = self.chooseDoctor(patientEmail)
            if a == 1:
                y = self.chooseSpecificDr(patientEmail)
                x = self.chooseDate(patientEmail)
                self.displayAvailable(patientEmail, x, y)
                self.chooseTime(patientEmail, x, y)
            if a == 2:
                y = self.chooseAnyDr(patientEmail)
                x = self.chooseDate(patientEmail)
                self.displayAvailable(patientEmail, x, y)
                self.chooseTime(patientEmail, x, y)
            if a == 3:
                y = self.chooseDrGender(patientEmail)
                x = self.chooseDate(patientEmail)
                self.displayAvailable(patientEmail, x, y)
                self.chooseTime(patientEmail, x, y)
            if a == 0:
                self.returnToAppMenu(patientEmail)

        if options == 2:
            self.viewAppConfirmations(patientEmail)
        if options == 3:
            self.cancelAppointment(patientEmail)
        if options == 0:
            # exit to main menu
            pass

    def chooseDoctor(self, patientEmail):
        print("**********"
              "\n[1] To book an appointment with a specific doctor"
              "\n[2] To book an appointment with any doctor"
              "\n[3] To book an appointment with a doctor of a specific gender"
              "\n[0] To exit to the appointment menu"
              "\n**********")
        dr_options = int(input("Please choose from the options above: "))
        return dr_options

    def chooseSpecificDr(self, patientEmail):
        print("**********"
              "\nThe doctors currently available at the practice are: ")
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        gpDetails = pf.chooseDr(dr_names)
        return gpDetails

    def chooseAnyDr(self, patientEmail):
        self.c.execute("SELECT firstname, lastname, gpEmail FROM GP")
        dr_names = self.c.fetchall()
        gp_list = []
        for dr in dr_names:
            gp_list.append(dr)
        gpchoice = random.choice(gp_list)
        gp_chosen_email = gpchoice[2]
        gp_chosen_name = gpchoice[1]
        gpDetails = [gp_chosen_email, gp_chosen_name]

        print("The doctor you have been assigned is Dr {}".format(gp_chosen_name))
        return gpDetails

    def chooseDrGender(self, patientEmail):
        print("**********"
              "\n[1] To book an appointment with a male doctor"
              "\n[2] to book an appointment with a female doctor"
              "\n[3] to book an appointment with a non-binary doctor")
        gp_options = int(input("Please choose from the options above: "))

        if gp_options == 1:
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'male' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        if gp_options == 2:
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'female' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails
        if gp_options == 3:
            self.c.execute("SELECT firstname, lastname, gpEmail FROM GP WHERE gender = 'non-binary' ")
            dr_names = self.c.fetchall()
            gpDetails = pf.chooseDr(dr_names)
            return gpDetails

    def chooseDate(self, patientEmail):
        print("**********"
              "\n [1] January     \t[2] February      \t[3] March"
              "\n [4] April     \t\t[5] May           \t[6] June"
              "\n [7] July      \t\t[8] August        \t[9] September "
              "\n [10] October    \t[11] November     \t[12] December")
        mm = int(input("Please choose the month would you would like your appointment in 2021: "))
        print("----------")
        print(calendar.month(2021, mm))
        print("----------")
        day = input("Please select a day (as dd): ")
        date = "2021-{}-{}".format(mm, day)
        return date

    def displayAvailable(self, patientEmail, date, gpDetails):
        print("\nThis is the current availability for Dr {} on your chosen date: ".format(gpDetails[1]))
        start_obj = pf.toDateObjApp00(date)
        start = pf.tounixtime(start_obj)
        end = pf.generateEndTime(date)

        self.c.execute("SELECT start, appointmentStatus FROM Appointment WHERE start >=? and end <? and gpEmail =?",
                       [start, end, gpDetails[0]])
        appointments = self.c.fetchall()
        times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
                 "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
        if not appointments:
            for i in times:
                print(i + " available")
        else:
            dict_time_status = {}
            for items in appointments:
                ts = pf.toregulartime(items[0])
                string_time = ts.strftime("%H:%M")
                dict_time_status[string_time] = items[1]
            for time in times:
                if time in dict_time_status:
                    print(time + ' ' + dict_time_status[time])
                else:
                    print(time + ' available')

    def chooseTime(self, patientEmail, date, gpDetails):
        print("**********"
              "\n[1] to select a time"
              "\n[2] to select another date"
              "\n[3] to exit to the main menu: ")
        options = int(input("**********"
                            "\nPlease choose from the options above: "))
        if options == 1:
            time = input("Please choose a time from the available appointments: ")
            day_str = date + ' ' + time
            dt_object = pf.toDateTimeObj(day_str)
            start = pf.tounixtime(dt_object)

            end = start + (30 * 60)
            gpLastName = gpDetails[1]
            gpEmail = gpDetails[0]
            reason = 'Appointment'
            appointmentStatus = 'Pending'
            dateRequested = pf.tounixtime(datetime.today())
            patientComplaints = ''
            doctorFindings = ''
            diagnosis = ''
            furtherInspections = ''
            doctorAdvice = ''
            checkIn = None
            checkOut = None

            self.c.execute("INSERT INTO Appointment VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           ([gpEmail, gpLastName, patientEmail, start, end, reason, appointmentStatus,
                             dateRequested, patientComplaints, doctorFindings, diagnosis, furtherInspections,
                             doctorAdvice, checkIn, checkOut]))
            self.connection.commit()
            print("You have requested to book an appointment on {} at {}, "
                  "\nyou will receive confirmation of your appointment shortly,".format(date, time))
            if input("Type yes to return to the appointment menu: ").lower() == 'yes':
                self.bookAppointment(patientEmail)

        if options == 2:
            self.chooseDate(patientEmail)
        if options == 3:
            self.returnToAppMenu(patientEmail)

    def cancelAppointment(self, patientEmail):
        print("**********"
              "\nThese are your booked and pending appointment requests: ")
        self.c.execute("SELECT appointmentID, start, gpLastName, appointmentStatus FROM Appointment "
                       "WHERE patientEmail =? ",
                       [patientEmail])
        appointments = self.c.fetchall()

        for app in appointments:
            dt = app[1]
            dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
            print("Appointment ID: " + str(app[0]) + "\t" + "date & time: " + dt + "\t\t" + "with: Dr "
                  + app[2] + "\t\t" + "status: " + app[3])

        print("**********"
              "\n[1] To cancel a booked or pending appointment request"
              "\n[2] To exit to the appointment menu"
              "\n**********")
        options = int(input("Please choose from the options above: "))

        if options == 1:
            cancel = input("\nPlease enter the appointment ID you would like to cancel: ")
            self.c.execute("DELETE FROM Appointment WHERE appointmentID =?", [cancel])
            self.connection.commit()
            print("You have cancelled your appointment")
            self.returnToAppMenu(patientEmail)

        if options == 2:
            self.returnToAppMenu(patientEmail)

    def viewAppConfirmations(self, patientEmail):
        print("**********"
              "\nThese are your confirmed booked appointments: ")
        self.c.execute("SELECT appointmentID, start, gpLastName FROM Appointment "
                       "WHERE patientEmail =? and appointmentStatus = 'Unavailable' ",
                       [patientEmail])
        appointments = self.c.fetchall()

        for app in appointments:
            dt = app[1]
            dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
            print("Appointment ID: " + str(app[0]) + "\t" + "date and time: " + dt + "\t\t" + "with: Dr " + app[2])
        self.returnToAppMenu(patientEmail)

    def returnToAppMenu(self, patientEmail):
        if input("Type yes to return to the appointment menu: ").lower() == 'yes':
            self.bookAppointment(patientEmail)


# ari = Appointment()
# ari.bookAppointment("ariannabourke@hotmail.com")


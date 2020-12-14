from datetime import datetime
import usefulfunctions as uf
import timetablefunctions as db
from GPs.printday import printday

dateformatstring = "%Y-%m-%d"

def clearhours(doctoremail):
    print("--------------------------------------------")
    print("\t Doctor Clear Hours")
    print("--------------------------------------------")
    date = uf.validatedate("Enter a date you would like to cancel an appointment.")
    printday(date,doctoremail)
    datestring = datetime.strftime(date,dateformatstring)
    appointments = []
    for appointment in db.timetableblock(doctoremail, datestring):
        appointments.append(appointment[4])
    print("\n\nPlease enter the appointment ids you would like to cancel separated by commas:")
    userinput = input(":")
    ids = userinput.split(",")
    for id in ids:
        try:
            idnum = int(id)
            if idnum in appointments:
                db.deleteappointment(idnum)
                print("Successfully deleted Appointment " + str(idnum))
            else:
                print("\t <Appointment of ID: "+str(idnum)+" doesn't exist on the given date.>")
        except:
            print("\t< "+ id + " is not a valid number>")
    print("********************************************")
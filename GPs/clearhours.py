from datetime import datetime
import uch.usefulfunctions as uf
import uch.timetablefunctions as db
from uch.GPs.printday import printday

dateformatstring = "%Y-%m-%d"

def clearhours(doctoremail):
    date = uf.validatedate("Enter a date you would like to cancel an appointment.")
    printday(date,doctoremail)
    datestring = datetime.strftime(date,dateformatstring)
    appointments = []
    for appointment in db.timetableblock(doctoremail, datestring):
        appointments.append(appointment[4])
    print("\n\n Enter the appointment ids you would like to cancel separated by commas:")
    userinput = input(":")
    ids = userinput.split(",")
    for id in ids:
        try:
            idnum = int(id)
            if idnum in appointments:
                db.deleteappointment(idnum)
                print("Successfully deleted Appointment " + str(idnum))
        except:
            print(id + " is not a valid number")
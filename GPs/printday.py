from datetime import datetime
import usefulfunctions as uf
import timetablefunctions as db

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"


def printday(day,doctoremail):
    print("--------------------------------------------")
    print(datetime.strftime(day, "%A %d %b %Y"))
    print("--------------------------------------------")
    datestring = datetime.strftime(day, dateformatstring)
    appointments = db.timetableblock(doctoremail, datestring)
    print("id" + "\t" + "reason")
    for appointment in appointments:
        reason = appointment[0]
        start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
        end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
        nhsNumber = str(appointment[3]).zfill(10)
        appointmentid = str(appointment[4])
        print(appointmentid + "\t" + reason + "\t" + start + "-" + end + "\t" + nhsNumber)
    print("\n")
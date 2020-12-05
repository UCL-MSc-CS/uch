from datetime import datetime
import uch.usefulfunctions as uf
import uch.timetablefunctions as db

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"


def printday(day,doctoremail):
    print("\n--------------------\n" + datetime.strftime(day, "%A %d %b %Y") + "\n--------------------")
    datestring = datetime.strftime(day, dateformatstring)
    appointments = db.timetableblock(doctoremail, datestring)
    print("id" + "\t" + "reason")
    for appointment in appointments:
        reason = appointment[0]
        start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
        end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
        patientemail = appointment[3]
        appointmentid = str(appointment[4])
        print(appointmentid + "\t" + reason + "\t" + start + "-" + end + "\t" + patientemail)
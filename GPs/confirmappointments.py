from datetime import datetime
import usefulfunctions as uf
import timetablefunctions as db

dateformatstring = "%Y-%m-%d"
timeformatstring = "%H:%M"

def confirmappointments(doctoremail):
    # todo once doctor has accepted the appointment, all pending appointments for other doctors get auto-rejected
    # todo make sure patient cannot have more than one pending appointment at a time (?)
    confirmdate = uf.validatedate("Please enter a date for confirming appointments")
    datestring = datetime.strftime(confirmdate,dateformatstring)
    continueconfirming = True
    while continueconfirming:
        pendingappointments = db.getallpendingappointments(doctoremail,datestring)

        pendingids = []
        for appointment in pendingappointments:
            pendingids.append(appointment[4])

        if not pendingids:
            print("\n\t<There are no pending appointments to confirm on " + datestring + ">\n")
            break

        print("--------------------------------------------")
        print(datetime.strftime(confirmdate, "%A %d %b %Y"))
        print("--------------------------------------------")
        print("id" + "\t" + "reason")
        for appointment in pendingappointments:
            reason = appointment[0]
            start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
            end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
            nhsNumber = str(appointment[3]).zfill(10)
            appointmentid = str(appointment[4])
            status = db.checkslotavailable(datestring, start, end, [doctoremail])
            if status[0] != 'unavailable':
                print(appointmentid + "\t" + reason + "\t" + start + "-" + end + "\t" + nhsNumber)
            else:
                db.declineappointment(appointmentid)
                pendingids.remove(appointment[4])

        id = input("Please enter the id of an appointment you would like to confirm (type 'x' to exit): ")
        try:
            if id.lower() == 'x':
                break
            idnum = int(id)
            if idnum in pendingids:
                db.acceptappointment(idnum)
                print("Accepted appointment with id " + id)
            else:
                print("\t<You entered an invalid id number!>")
        except:
            print("\t<That is not a integer value>")

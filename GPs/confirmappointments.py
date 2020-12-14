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
        print("\n--------------------\n" + datetime.strftime(confirmdate, "%A %d %b %Y") + "\n--------------------")
        print("id" + "\t" + "reason")
        for appointment in pendingappointments:
            reason = appointment[0]
            start = datetime.strftime(uf.toregulartime(appointment[1]), timeformatstring)
            end = datetime.strftime(uf.toregulartime(appointment[2]), timeformatstring)
            patientemail = appointment[3]
            appointmentid = str(appointment[4])
            status = db.checkslotavailable(datestring, start, end, [doctoremail])
            if status[0] != 'unavailable':
                print(appointmentid + "\t" + reason + "\t" + start + "-" + end + "\t" + patientemail)
            else:
                db.declineappointment(appointmentid)
                pendingids.remove(appointment[4])
        id = input("please enter the id of an appointment you would like to confirm: ")

        try:
            idnum = int(id)
            if idnum in pendingids:
                db.acceptappointment(idnum)
                print("Accepted appointment with id " + id)
            else:
                print("You entered an invalid id number!")
        except:
            print("That is not a integer value")

        choosecontinue = input("Would you like to continue confirming appointments y/n ? :")
        if choosecontinue.lower() == 'y':
            continueconfirming = True
        elif choosecontinue.lower() == 'n':
            continueconfirming = False
        else:
            print("Invalid option chosen, exiting appointment confirmation....")
            continueconfirming = False

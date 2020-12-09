import sqlite3
from datetime import datetime, timedelta
import usefulfunctions as uf
from pathlib import Path

datetimeformat = "%Y-%m-%d %H:%M"


# connect to your database
def connecttodb():

    path = str(Path(__file__).parent.absolute()) + "/UCH.db"
    connection = sqlite3.connect(path)  # DO NOT add this file to Git!!!
    cursor = connection.cursor()
    conncursordict = {"connection": connection, "cursor": cursor}
    return conncursordict


# disconnect from your database
def closeconn(conn):
    conn.commit()
    conn.close()


# returns the number of rows altered since you last opened a connection
def find_rows_changed(conn):
    conn["cursor"].execute("SELECT changes()")
    return conn['cursor'].fetchone()[0]


"""
place all functions below in the following template....

def functionname(args):
    conn = connecttodb()

    *your code here.....*

    closeconn(conn["connection"])

"""

# gets the doctor's last name given an email address.
def getdoclastname(docemail):
    conn = connecttodb()

    sql = """SELECT lastName FROM GP WHERE gpEmail = ?"""
    values = (docemail,)
    conn['cursor'].execute(sql,values)
    results = conn['cursor'].fetchone()
    lastname = results[0]

    closeconn(conn["connection"])
    return lastname

# allows one to book time into the system's calendar
# the gpEmailArray is a list with all the GPs you wish to create an appointment for
def book_time(date, startTime, endTime, reason, patientEmail, gpEmailArray):
    conn = connecttodb()

    start = uf.tounixtime(datetime.strptime(date + " " + startTime, datetimeformat))
    end = uf.tounixtime(datetime.strptime(date + " " + endTime, datetimeformat))
    dateRequested = uf.tounixtime(datetime.today())
    appointmentStatus = ''

    if reason == 'Appointment':
        appointmentStatus = 'Pending'

    for gpEmail in gpEmailArray:
        gpLastName = getdoclastname(gpEmail)
        values = (
            None, gpEmail, gpLastName, patientEmail, start, end, reason, appointmentStatus, dateRequested, '', '', '', '', '', None,
            None)
        conn["cursor"].execute(
            """
            INSERT INTO Appointment
            Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, values
        )

    closeconn(conn["connection"])


# Books an appointment, autosets reason to "Appointment" to make life easy
def book_appointment(date, startTime, endTime, patientEmail, gpEmailArray):
    book_time(date, startTime, endTime, "Appointment", patientEmail, gpEmailArray)


# returns a list of available gps during a timeframe that you have provided, else will return "unavailable"
def checkslotavailable(date, startTime, endTime, gpemailarray):
    conn = connecttodb()

    startunix = uf.tounixtime(datetime.strptime(date + " " + startTime, datetimeformat))
    endunix = uf.tounixtime(datetime.strptime(date + " " + endTime, datetimeformat))

    sql = """
        SELECT gpEmail FROM Appointment 
        WHERE 
            (
                (start <= ? AND end > ? ) OR
                (start < ? AND end >= ?) OR
                (start > ? AND end < ?)
            ) AND
            appointmentStatus not in ('Pending','Unavailable')
    """
    values = (startunix,startunix,endunix,endunix,startunix,endunix)

    conn['cursor'].execute(sql,values)
    busygps = conn['cursor'].fetchall()
    closeconn(conn["connection"])
    freegps = []

    for gpemail in gpemailarray:
        isbusy = False
        for gp in busygps:
            if gpemail == gp[0]:
                isbusy = True
        if not isbusy:
            freegps.append(gpemail)

    if freegps:
        return freegps
    else:
        return ["unavailable"]


# I use this to return everything i need to print out appointments for a dr. on a given day
def timetableblock(gpemail, date):
    conn = connecttodb()

    start = uf.tounixtime(datetime.strptime(date + " 00:00", datetimeformat))
    end = uf.tounixtime(datetime.strptime(date + " 00:00", datetimeformat) + timedelta(1))

    sql= """
    
        SELECT reason,start,end,patientEmail,appointmentID FROM Appointment 
        WHERE 
            gpEmail = ? AND
            start >= ? AND 
            end <= ? AND
            appointmentStatus not in ('Pending','Unavailable')
        ORDER BY start asc
    """
    values = (gpemail,start,end)

    conn['cursor'].execute(sql,values)
    results = conn['cursor'].fetchall()

    closeconn(conn["connection"])
    return results

# this is used to open today's appointments that have been confirmed.
def TodayAppointments(gpemail):
    conn = connecttodb()
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)
    start = uf.tounixtime(today)
    end = uf.tounixtime(today + timedelta(1))

    sql = """

        SELECT reason,start,end,patientEmail,appointmentID FROM Appointment 
        WHERE 
            gpEmail = ? AND
            start >= ? AND 
            end <= ? AND
            appointmentStatus = 'Available'
        ORDER BY start asc
    """
    values = (gpemail, start, end)

    conn['cursor'].execute(sql, values)
    results = conn['cursor'].fetchall()

    closeconn(conn["connection"])
    return results


# call this when you'd like to cancel an appointment
def deleteappointment(appointmentId):
    conn = connecttodb()
    conn['cursor'].execute("""
        DELETE FROM Appointment
        WHERE appointmentID = ?
    """, (appointmentId,))
    closeconn(conn["connection"])


# used by doctors to find pending appointments to confirm/decline.
def getallpendingappointments(gpemail, date):
    conn = connecttodb()

    start = str(uf.tounixtime(datetime.strptime(date + " 00:00", datetimeformat)))
    end = str(uf.tounixtime(datetime.strptime(date + " 00:00", datetimeformat) + timedelta(1)))

    conn['cursor'].execute(
        """
     SELECT reason,start,end,patientEmail,appointmentID 
     FROM Appointment 
     WHERE
        appointmentStatus = 'Pending' AND
        (start >= ? AND end <= ?) AND
        gpEmail = ?
     """
        , (start, end, gpemail))

    results = conn['cursor'].fetchall()
    closeconn(conn["connection"])
    return results


# confirm/accept and appointment
def acceptappointment(appointmentId):
    conn = connecttodb()

    conn['cursor'].execute("""
    UPDATE 
        Appointment
    SET
       appointmentStatus = 'Available'
    WHERE
        appointmentID = ? 
    """, (appointmentId,))

    closeconn(conn["connection"])


# decline/reject an appointment
def declineappointment(appointmentId):
    conn = connecttodb()

    conn['cursor'].execute("""
    UPDATE 
        Appointment
    SET
       appointmentStatus = 'Unavailable'
    WHERE
        appointmentID = ? 
    """, (appointmentId,))

    closeconn(conn["connection"])

def getDoctorNotes(appointmentId):
    conn = connecttodb()

    conn['cursor'].execute("""
        SELECT 
            patientComplaints,
            doctorFindings,
            diagnosis,
            furtherInspections,
            doctorAdvice,
            appointmentID
        FROM
            Appointment
        WHERE
            appointmentID = ?
        """, (appointmentId,))

    results = list(conn['cursor'].fetchone())
    closeconn(conn["connection"])
    return results

# This saves/updates the doctor's notes
def saveDoctorNotes(doctorsnotes):
    conn = connecttodb()
    # patientComplaints = tuple[0]
    # doctorFindings = tuple[1]
    # diagnosis = tuple[2]
    # furtherInspections = tuple[3]
    # doctorAdvice = tuple[4]

    doctorsnotestuple = tuple(doctorsnotes)

    conn['cursor'].execute("""
        UPDATE
            Appointment
        SET
            patientComplaints = ?,
            doctorFindings = ?,
            diagnosis = ?,
            furtherInspections = ?,
            doctorAdvice = ?
        WHERE
            appointmentID = ? 
        """, doctorsnotestuple)

    closeconn(conn["connection"])



# book_appointment("2020-12-05", "15:00", "16:30", "cooldude@gmail.com", ["test@gmail.com"])
# book_appointment("2020-12-05", "14:00", "15:00", "iamsick@gmail.com", ["test@gmail.com"])
# book_appointment("2020-12-07", "17:30", "18:30", "whyunotreatme@gmail.com", ["test@gmail.com"])
# print(checkslotavailable("2020-12-04","10:30","12:30",["drgrey@gmail.com"]))


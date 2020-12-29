import sqlite3
from datetime import datetime, timedelta
import useful_functions as uf
from pathlib import Path

datetimeformat = "%Y-%m-%d %H:%M"


# connect to your database
def connect_to_db():

    path = str(Path(__file__).parent.absolute()) + "/UCH.db"
    connection = sqlite3.connect(path)  # DO NOT add this file to Git!!!
    cursor = connection.cursor()
    conncursordict = {"connection": connection, "cursor": cursor}
    return conncursordict


# disconnect from your database
def close_connection(conn):
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
def get_gp_last_name(docemail):
    conn = connect_to_db()

    sql = """SELECT lastName FROM GP WHERE gpEmail = ?"""
    values = (docemail,)
    conn['cursor'].execute(sql,values)
    results = conn['cursor'].fetchone()
    lastname = results[0]

    close_connection(conn["connection"])
    return lastname

# allows one to book time into the system's calendar
# the gpEmailArray is a list with all the GPs you wish to create an appointment for
def book_time(date, startTime, endTime, reason, nhsNumber, gpEmailArray):
    conn = connect_to_db()

    start = uf.regular_to_unix_time(datetime.strptime(date + " " + startTime, datetimeformat))
    end = uf.regular_to_unix_time(datetime.strptime(date + " " + endTime, datetimeformat))
    dateRequested = uf.regular_to_unix_time(datetime.today())
    appointmentStatus = ''

    if reason == 'Appointment':
        appointmentStatus = 'Pending'

    for gpEmail in gpEmailArray:
        gpLastName = get_gp_last_name(gpEmail)
        values = (
            None, gpEmail, gpLastName, nhsNumber, start, end, reason, appointmentStatus, dateRequested, '', '', '', '', '', None,
            None)
        conn["cursor"].execute(
            """
            INSERT INTO Appointment
            Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, values
        )

    close_connection(conn["connection"])


# Books an appointment, autosets reason to "Appointment" to make life easy
def book_appointment(date, startTime, endTime, nhsNumber, gpEmailArray):
    book_time(date, startTime, endTime, "Appointment", nhsNumber, gpEmailArray)


# returns a list of available gps during a timeframe that you have provided, else will return "unavailable"
def check_slot_available(date, startTime, endTime, gpemailarray):
    conn = connect_to_db()

    startunix = uf.regular_to_unix_time(datetime.strptime(date + " " + startTime, datetimeformat))
    endunix = uf.regular_to_unix_time(datetime.strptime(date + " " + endTime, datetimeformat))

    sql = """
        SELECT gpEmail FROM Appointment 
        WHERE 
            (
                (start <= ? AND end > ? ) OR
                (start < ? AND end >= ?) OR
                (start > ? AND end < ?)
            ) AND
            appointmentStatus not in ('Pending','Declined')
    """
    values = (startunix,startunix,endunix,endunix,startunix,endunix)

    conn['cursor'].execute(sql,values)
    busygps = conn['cursor'].fetchall()
    close_connection(conn["connection"])
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


# Returns information to print out appointments for a gp on a given day
def timetable_block(gpemail, date):
    conn = connect_to_db()

    start = uf.regular_to_unix_time(datetime.strptime(date + " 00:00", datetimeformat))
    end = uf.regular_to_unix_time(datetime.strptime(date + " 00:00", datetimeformat) + timedelta(1))

    sql= """
    
        SELECT reason,start,end,nhsNumber,appointmentID FROM Appointment 
        WHERE 
            gpEmail = ? AND
            start >= ? AND 
            end <= ? AND
            appointmentStatus not in ('Pending','Declined')
        ORDER BY start asc
    """
    values = (gpemail,start,end)

    conn['cursor'].execute(sql,values)
    results = conn['cursor'].fetchall()

    close_connection(conn["connection"])
    return results

# this is used to open today's appointments that have been confirmed.
def todays_appointments(gpemail):
    conn = connect_to_db()
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)
    start = uf.regular_to_unix_time(today)
    end = uf.regular_to_unix_time(today + timedelta(1))

    sql = """

        SELECT reason,start,end,nhsNumber,appointmentID FROM Appointment 
        WHERE 
            gpEmail = ? AND
            start >= ? AND 
            end <= ? AND
            appointmentStatus = 'Accepted'
        ORDER BY start asc
    """
    values = (gpemail, start, end)

    conn['cursor'].execute(sql, values)
    results = conn['cursor'].fetchall()

    close_connection(conn["connection"])
    return results

#call this function when you want to delete non-patient time/decline an appointment if its a patient appointment
def clear_booked_time(appointmentId):
    conn = connect_to_db()
    conn['cursor'].execute("""
            SELECT reason 
            FROM Appointment
            WHERE appointmentID = ?
        """, (appointmentId,))
    appointment_type = conn['cursor'].fetchone()[0]
    close_connection(conn["connection"])
    if appointment_type == "Appointment":
        decline_appointment(appointmentId)
    else:
        delete_booked_time(appointmentId)

# call this when you'd like to cancel an appointment
def delete_booked_time(appointmentId):
    conn = connect_to_db()
    conn['cursor'].execute("""
        DELETE FROM Appointment
        WHERE appointmentID = ?
    """, (appointmentId,))
    close_connection(conn["connection"])


# used by doctors to find pending appointments to confirm/decline.
def get_all_pending_appointments(gpemail, date):
    conn = connect_to_db()

    start = str(uf.regular_to_unix_time(datetime.strptime(date + " 00:00", datetimeformat)))
    end = str(uf.regular_to_unix_time(datetime.strptime(date + " 00:00", datetimeformat) + timedelta(1)))

    conn['cursor'].execute(
        """
     SELECT reason,start,end,nhsNumber,appointmentID 
     FROM Appointment 
     WHERE
        appointmentStatus = 'Pending' AND
        (start >= ? AND end <= ?) AND
        gpEmail = ?
     """
        , (start, end, gpemail))

    results = conn['cursor'].fetchall()
    close_connection(conn["connection"])
    return results


# confirm/accept and appointment
def accept_appointment(appointmentId):
    conn = connect_to_db()

    conn['cursor'].execute("""
    UPDATE 
        Appointment
    SET
       appointmentStatus = 'Accepted'
    WHERE
        appointmentID = ? 
    """, (appointmentId,))

    close_connection(conn["connection"])


# decline/reject an appointment
def decline_appointment(appointmentId):
    conn = connect_to_db()

    conn['cursor'].execute("""
    UPDATE 
        Appointment
    SET
       appointmentStatus = 'Declined'
    WHERE
        appointmentID = ? 
    """, (appointmentId,))

    close_connection(conn["connection"])

def get_doctor_notes(appointmentId):
    conn = connect_to_db()

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
    close_connection(conn["connection"])
    return results

# This saves/updates the doctor's notes
def save_doctor_notes(doctorsnotes):
    conn = connect_to_db()

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

    close_connection(conn["connection"])

# This pulls basic patient information for the doctor
def get_patient_info(appointmentId):
    conn = connect_to_db()

    conn['cursor'].execute("""
            SELECT 
                A.nhsNumber,
                P.patientEmail,
                P.firstName,
                P.lastName,
                P.dateOfBirth,
                P.gender,
                P.addressLine1,
                P.addressLine2,
                P.postcode,
                P.telephoneNumber,
                A.appointmentID,
                Q.height,
                Q.weight,
                Q.bmi
            FROM
                Appointment A
            LEFT JOIN PatientDetail P ON A.nhsNumber = P.nhsNumber
            LEFT JOIN questionnaireTable Q ON P.nhsNumber = A.nhsNumber
            WHERE
                appointmentID = ?
            """, (appointmentId,))

    results = list(conn['cursor'].fetchone())
    close_connection(conn["connection"])
    return results

#call this function to autodecline any pending appointments when a doctor wants to book non-patient time
def auto_decline_pending(datestring, startstring, endstring, doctoremail):
    conn = connect_to_db()

    start = str(uf.regular_to_unix_time(datetime.strptime(datestring + " " + startstring, datetimeformat)))
    end = str(uf.regular_to_unix_time(datetime.strptime(datestring + " " + endstring, datetimeformat)))

    conn['cursor'].execute(
        """
     SELECT appointmentID 
     FROM Appointment 
     WHERE
        reason = "Appointment" AND
        appointmentStatus = 'Pending' AND
        (
                (start <= ? AND end > ? ) OR
                (start < ? AND end >= ?) OR
                (start > ? AND end < ?)
        ) AND
        gpEmail = ?
     """
        , (start, start, end, end, start, end, doctoremail))

    results = conn['cursor'].fetchall()
    close_connection(conn["connection"])

    conflicting_appointments = []
    for result in results:
        conflicting_appointments.append(result[0])

    for appointmentID in conflicting_appointments:
        decline_appointment(appointmentID)

    if conflicting_appointments:
        #You HAVE auto-declined appointments
        return True
    else:
        #You HAVE NOT declined anything
        return False


# used only for testing
if __name__ == "__main__":
    today = datetime.strftime(datetime.today(),"%Y-%m-%d")
    book_appointment(today, "15:00", "16:30", "1234567890", ["matthew.shorvon@ucl.ac.uk"])
    book_appointment(today, "14:00", "15:00", "1234567890", ["matthew.shorvon@ucl.ac.uk"])
    book_appointment(today, "17:30", "18:30", "1234567890", ["matthew.shorvon@ucl.ac.uk"])
    #print(checkslotavailable("2020-12-14","13:30","14:01",["drgrey@gmail.com","matthew.shorvon@ucl.ac.uk"]))
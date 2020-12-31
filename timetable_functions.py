import sqlite3
from datetime import datetime, timedelta
import useful_functions as uf
from pathlib import Path
import logging

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M"


def connect_to_db():
    """
    Connect to your database
    """
    path = str(Path(__file__).parent.absolute()) + "/UCH.db"
    connection = sqlite3.connect(path)  # DO NOT add this file to Git!!!
    cursor = connection.cursor()
    conncursordict = {"connection": connection, "cursor": cursor}
    return conncursordict


def close_connection(conn):
    """
    Disconnect from your database
    """
    conn.commit()
    conn.close()


def find_rows_changed(conn):
    """
    Returns the number of rows altered since you last opened a connection
    """
    conn["cursor"].execute("SELECT changes()")
    return conn['cursor'].fetchone()[0]


"""
place all functions below in the following template....

def functionname(args):
    conn = connecttodb()

    *your code here.....*

    closeconn(conn["connection"])

"""

def get_gp_last_name(docemail):
    """
    Gets the doctor's last name given an email address.
    """
    conn = connect_to_db()

    sql = """SELECT lastName FROM GP WHERE gpEmail = ?"""
    values = (docemail,)
    conn['cursor'].execute(sql,values)
    results = conn['cursor'].fetchone()
    lastname = results[0]

    close_connection(conn["connection"])
    logging.info("Retrieving Doctor's last name. Dr. " + lastname)
    return lastname

def book_time(date, startTime, endTime, reason, nhsNumber, gpEmailArray):
    """
    Allows one to book time into the system's calendar.
    the gpEmailArray is a list with all the GPs you wish to create an appointment for
    """
    conn = connect_to_db()

    start = uf.regular_to_unix_time(datetime.strptime(date + " " + startTime, DATE_TIME_FORMAT))
    end = uf.regular_to_unix_time(datetime.strptime(date + " " + endTime, DATE_TIME_FORMAT))
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
        logging.info("Booking {} time to Dr.{}'s timetable on {} {}-{}".format(reason,gpLastName,date,startTime,endTime))

    close_connection(conn["connection"])


def book_appointment(date, startTime, endTime, nhsNumber, gpEmailArray):
    """
    Books a patient appointment, auto-sets reason to "Appointment" to make life easy
    """
    book_time(date, startTime, endTime, "Appointment", nhsNumber, gpEmailArray)


def check_slot_available(date, startTime, endTime, gpemailarray):
    """
    Returns a list of available gps during a timeframe that you have provided, else will return "unavailable""
    """
    conn = connect_to_db()
    logging.info("Checking timeslot {} {}-{} to see if it is available".format(date,startTime,endTime))

    startunix = uf.regular_to_unix_time(datetime.strptime(date + " " + startTime, DATE_TIME_FORMAT))
    endunix = uf.regular_to_unix_time(datetime.strptime(date + " " + endTime, DATE_TIME_FORMAT))

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
        logging.info('Available GPs found')
        return freegps
    else:
        logging.info('No GPs free during this time')
        return ["unavailable"]


def timetable_block(gpemail, date):
    """
    Returns information to print out appointments for a gp on a given day
    """
    conn = connect_to_db()

    start = uf.regular_to_unix_time(datetime.strptime(date + " 00:00", DATE_TIME_FORMAT))
    end = uf.regular_to_unix_time(datetime.strptime(date + " 00:00", DATE_TIME_FORMAT) + timedelta(1))

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

def todays_appointments(gpemail):
    """
    This is used to open today's appointments that have been confirmed.
    """
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

def clear_booked_time(appointmentId):
    """
    Call this function when you want to delete non-patient time/decline an appointment if its a patient appointment
    """
    conn = connect_to_db()
    conn['cursor'].execute("""
            SELECT reason 
            FROM Appointment
            WHERE appointmentID = ?
        """, (appointmentId,))
    appointment_type = conn['cursor'].fetchone()[0]
    close_connection(conn["connection"])
    if appointment_type == "Appointment":
        logging.info("Declining patient appointment of ID: " + str(appointmentId))
        decline_appointment(appointmentId)
    else:
        logging.info("Deleting appointment of ID: " + str(appointmentId))
        delete_booked_time(appointmentId)

def delete_booked_time(appointmentId):
    """
    Call this when you'd like to cancel an appointment
    """
    conn = connect_to_db()
    conn['cursor'].execute("""
        DELETE FROM Appointment
        WHERE appointmentID = ?
    """, (appointmentId,))
    close_connection(conn["connection"])


def get_all_pending_appointments(gpemail, date):
    """
    Used by doctors to find pending appointments to confirm/decline.
    """
    conn = connect_to_db()

    start = str(uf.regular_to_unix_time(datetime.strptime(date + " 00:00", DATE_TIME_FORMAT)))
    end = str(uf.regular_to_unix_time(datetime.strptime(date + " 00:00", DATE_TIME_FORMAT) + timedelta(1)))

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


def accept_appointment(appointmentId):
    """
    Confirm/accept an appointment
    """
    conn = connect_to_db()
    logging.info("Accepting appointment of ID: " + str(appointmentId))

    conn['cursor'].execute("""
    UPDATE 
        Appointment
    SET
       appointmentStatus = 'Accepted'
    WHERE
        appointmentID = ? 
    """, (appointmentId,))

    close_connection(conn["connection"])


def decline_appointment(appointmentId):
    """
    Decline/reject an appointment
    """
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
    """
    Used to get the appointment notes for a particular appointment
    """
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

def save_doctor_notes(doctorsnotes):
    """
    This saves/updates the doctor's notes to the database.
    """
    conn = connect_to_db()
    logging.info("Saving Doctor's notes for patient appointment ID: " + doctorsnotes[5])

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

def get_patient_info(appointmentId):
    """
    This pulls basic patient information for the doctor, given an appointment ID
    """
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

def auto_decline_pending(datestring, startstring, endstring, doctoremail):
    """
    Call this function to auto-decline any pending appointments when a doctor wants to book non-patient time
    """
    conn = connect_to_db()

    start = str(uf.regular_to_unix_time(datetime.strptime(datestring + " " + startstring, DATE_TIME_FORMAT)))
    end = str(uf.regular_to_unix_time(datetime.strptime(datestring + " " + endstring, DATE_TIME_FORMAT)))

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
        logging.info("Auto-Declining pending patient appointment of ID: "+str(appointmentID)+" due to time being booked")
        decline_appointment(appointmentID)

    if conflicting_appointments:
        #You HAVE auto-declined appointments
        return True
    else:
        #You HAVE NOT declined anything
        return False


if __name__ == "__main__":
    """
    Used only for testing
    """
    today = datetime.strftime(datetime.today(),"%Y-%m-%d")
    book_appointment(today, "15:00", "16:30", "1234567890", ["chenuka.ratwatte@ucl.ac.uk"])
    book_appointment(today, "14:00", "15:00", "1234567890", ["chenuka.ratwatte@ucl.ac.uk"])
    book_appointment(today, "17:30", "18:30", "1234567890", ["chenuka.ratwatte@ucl.ac.uk"])
    #print(checkslotavailable("2020-12-14","13:30","14:01",["drgrey@gmail.com","matthew.shorvon@ucl.ac.uk"]))
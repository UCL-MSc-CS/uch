import sqlite3
from pathlib import Path
from datetime import datetime,timedelta
import time

datetimeformat = "%Y-%m-%d %H:%M"

def find_rows_changed(conn):
    conn["cursor"].execute("SELECT changes()")
    return conn['cursor'].fetchone()[0]

def tounixtime(dt):
    result = int(time.mktime(dt.timetuple()))
    return result

def connecttodb():
    path = str(Path(__file__).parent.absolute()) + "/UCLHospital.db"
    connection = sqlite3.connect(path)  # DO NOT add this file to Git!!!
    cursor = connection.cursor()
    conncursordict = {"connection":connection,"cursor":cursor}
    return conncursordict

def closeconn(conn):
    conn.commit()
    conn.close()

"""
place all functions below in the following template....

def functionname(args):
    conn = connecttodb()
    
    *your code here.....*
    
    closeconn(conn["connection"])

"""


def bookslot(gpId,date,startTime,endTime,reason,appointment):
    conn = connecttodb()

    start = tounixtime(datetime.strptime(date +" "+startTime,datetimeformat))
    end = tounixtime(datetime.strptime(date +" "+endTime,datetimeformat))
    values = (gpId,start,end,reason,appointment)
    conn["cursor"].execute(
        """
        INSERT INTO DoctorTimetable
        Values(?,?,?,?,?)
        """, values
    )
    closeconn(conn["connection"])

#TOdo make the below function more efficient.

def deletetime(gpId,startdate,starttime,enddate,endtime):
    startdatetime = datetime.strptime(startdate +" "+starttime,datetimeformat)
    enddatetime = datetime.strptime(enddate+" "+endtime,datetimeformat)
    start = str(tounixtime(startdatetime))
    end = str(tounixtime(enddatetime))

    #delete time fully contained in bounds
    fulldelete(gpId, start, end)

    #split into two if time encompasses bounds
    splittime(gpId, start, end)

    #trim beggining off if required
    trimbeggining(gpId, start, end)

    #trim end off if required
    trimend(gpId, start, end)

def fulldelete(gpId,start,end):
    conn = connecttodb()

    deletestatement = "DELETE FROM DoctorTimetable WHERE "
    condition1 = "gpId = " + str(gpId) + " AND "
    condition2 = "start >= " + start + " AND end <= " + end
    combined = deletestatement + condition1 + condition2
    conn['cursor'].execute(combined)


    rowschanged = find_rows_changed(conn)
    if(rowschanged>0):
        print("Completely deleted " + str(rowschanged) + " rows")

    closeconn(conn["connection"])

def trimbeggining(gpId,start,end):
    conn = connecttodb()

    updatestatement = "UPDATE DoctorTimetable "
    setstatement = "SET start = " + end + " WHERE "
    condition1 = "gpId = " + str(gpId) + " AND "
    condition2 = "start >= " + start + " AND end > " + end + " AND start < " + end
    combined = updatestatement + setstatement + condition1 + condition2
    conn['cursor'].execute(combined)

    rowschanged = find_rows_changed(conn)
    if(rowschanged>0):
        print("Trimmed start of " + str(rowschanged) + " rows")

    closeconn(conn["connection"])

def trimend(gpId,start,end):
    conn = connecttodb()

    updatestatement = "UPDATE DoctorTimetable "
    setstatement = "SET end = " + start + " WHERE "
    condition1 = "gpId = " + str(gpId) + " AND "
    condition2 = "start < " + start + " AND end <= " + end + " AND end > " + start
    combined = updatestatement + setstatement + condition1 + condition2
    conn['cursor'].execute(combined)

    rowschanged = find_rows_changed(conn)
    if(rowschanged>0):
        print("Trimmed end of " + str(rowschanged) + " rows")

    closeconn(conn["connection"])

def splittime(gpId,start,end):
    conn = connecttodb()

    selectstatement = "SELECT rowid,end,reason,Appointment from DoctorTimetable WHERE "
    condition1 = "gpId = " + str(gpId) + " AND "
    condition2 = "start < " + start + " AND end > " + end
    combined = selectstatement + condition1 + condition2
    conn['cursor'].execute(combined)
    results = conn['cursor'].fetchall()
    for row in results:
        rowid = str(row[0])
        originalend = row[1]
        originalreason = row[2]
        originalappointment = row[3]

        updatestatement = "UPDATE DoctorTimetable "
        setstatement = "SET end = " + start + " "
        condition1 = "WHERE rowid = " + rowid
        combined = updatestatement + setstatement + condition1
        conn['cursor'].execute(combined)

        values = (gpId, end, originalend, originalreason, originalappointment)
        conn["cursor"].execute(
            """
            INSERT INTO DoctorTimetable
            Values(?,?,?,?,?)
            """, values
        )

    rowschanged = find_rows_changed(conn)/2
    if(rowschanged>0):
        print("Split " + str(rowschanged) + " rows")

    closeconn(conn["connection"])


def checkiftimebooked(gpId,startdate,starttime,enddate,endtime):
    conn = connecttodb()

    start = tounixtime(datetime.strptime(startdate +" "+starttime,datetimeformat))
    end = tounixtime(datetime.strptime(enddate+" "+endtime,datetimeformat))

    selectstatement = "SELECT rowId FROM DoctorTimetable WHERE "
    condition1 = "gpId = " + str(gpId) + " AND "
    condition2 = "start <= " + str(end) + " AND end >= " + str(start)
    limit = " limit 1"
    combined = selectstatement + condition1 + condition2 + limit

    conn['cursor'].execute(combined)

    if conn['cursor'].fetchone() == None:
        result = False
    else:
        result = True
    closeconn(conn["connection"])
    return result

def timetableblock(gpId,date):
    conn = connecttodb()

    start = tounixtime(datetime.strptime(date + " 00:00", datetimeformat))
    end = tounixtime(datetime.strptime(date + " 00:00", datetimeformat) + timedelta(1))

    selectstatement = "SELECT reason,start,end,Appointment FROM DoctorTimetable WHERE "
    condition1 = "gpId = " + str(gpId) + " AND "
    condition2 = "start >= " + str(start) + " AND end <= " + str(end) + " "
    orderexpression = "ORDER BY start asc"
    combined = selectstatement + condition1 + condition2 + orderexpression
    conn['cursor'].execute(combined)
    results = conn['cursor'].fetchall()

    closeconn(conn["connection"])
    return results

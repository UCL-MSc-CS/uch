import tkinter
from tkinter import *
from tkcalendar import *
from selecttime import App
from datetime import datetime

availabilitydate = datetime.strptime("0001/01/01","%Y/%m/%d")

def grab_date():
    my_label.config(text=cal.get_date())

def submitdate():
    submitteddate = cal.get_date()
    availabilitydate = datetime.strptime(submitteddate,"%d/%m/%Y")
    user = "Dr. Victor Von Doom"
    title = "Doctor Availability"
    year = str(availabilitydate.year)
    month = str(availabilitydate.month)
    filetitle = user + '-' + title + ' ' + year + '-' + month + ".csv"
    timepage = tkinter.Tk()
    App(timepage, availabilitydate, filetitle).pack()
    timepage.title(title)
    timepage.mainloop()

root = Tk()
root.title('UCH.com')
root.geometry("600x400")

today=datetime.today()

cal = Calendar(root, selectmode="day", year=today.year, month=today.month, day=today.day, date_pattern= 'dd/mm/yyyy')
cal.pack(pady=20)

my_label = Label(root, text="")
my_label.pack(pady=20)

my_button = Button(root, text="Add availability", command=submitdate)
my_button.pack(pady=20)

root.mainloop()

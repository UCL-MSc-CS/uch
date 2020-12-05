import tkinter
from tkinter import *
from tkcalendar import *
from selecttime import App
from datetime import datetime

def grab_date():
    my_label.config(text=cal.get_date())

def submitdate():
    submitteddate = cal.get_date()
    unavailabledate = datetime.strptime(submitteddate,"%d/%m/%Y")
    #ToDo: extract username from login
    user = "Dr. Victor Von Doom"
    title = "Doctor Unavailability"
    year = str(unavailabledate.year)
    month = str(unavailabledate.month)
    filetitle = user + '-' + title + ' ' + year + '-' + month + ".csv"
    timepage = tkinter.Tk()
    App(timepage, unavailabledate, filetitle).pack()
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

my_button = Button(root, text="Add unavailability", command=submitdate)
my_button.pack(pady=20)

root.mainloop()

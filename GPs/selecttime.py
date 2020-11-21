import tkinter as tk
from tkinter.font import Font
from datetime import datetime, timedelta
import os

def file_is_empty(path):
    return os.stat(path).st_size==0

globalvar = []


class App(tk.Frame):

    def __init__(self, parent,date,filetitle):
        super().__init__(parent)

        globalvar.append(date)
        globalvar.append(filetitle)

        self.Maindesc = tk.Label(self, text="Please select your unavailability for "+ datetime.strftime(date,"%d/%b/%Y"),
                                 font=Font(family='Calibri', weight='bold'))
        self.Maindesc.grid(row=0, column=0)

        self.Startlabel = tk.Label(self, text="Please enter start time for this date: ",
                                   font=Font(family='Calibri', weight='bold'))
        self.Startlabel.grid(row=1, column=0)

        self.hourstr = tk.StringVar(self, '10')
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hourstr, width=2, state="readonly",
                               font=Font(family='Calibri', weight='bold'))

        self.minstr = tk.StringVar(self, '30')
        self.minstr.trace("w", self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minstr, width=2, state="readonly",
                              font=Font(family='Calibri', weight='bold'))

        self.hour.grid(row=1, column=1)
        self.min.grid(row=1, column=2)

        self.Endlabel = tk.Label(self, text="Please enter end time for this date: ",
                                 font=Font(family='Calibri', weight='bold'))
        self.Endlabel.grid(row=2, column=0)

        self.hourstrend = tk.StringVar(self, '10')
        self.hourend = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hourstrend, width=2,
                                  state="readonly", font=Font(family='Calibri', weight='bold'))

        self.minstrend = tk.StringVar(self, '30')
        self.minstrend.trace("w", self.trace_var_end)
        self.last_value_end = ""
        self.minend = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minstrend, width=2,
                                 state="readonly", font=Font(family='Calibri', weight='bold'))

        self.hourend.grid(row=2, column=1)
        self.minend.grid(row=2, column=2)

        self.submitButton = tk.Button(self, text="Submit!", state="normal", padx=50, pady=10, command=self.submitdata,
                                      font=Font(family='Calibri', weight='bold')).grid(row=3, column=0)

    def trace_var(self, *args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get()) + 1 if self.hourstr.get() != "23" else 0)
        if self.last_value == "0" and self.minstr.get() == "59":
            self.hourstr.set(int(self.hourstr.get()) - 1 if self.hourstr.get() != "0" else 0)
        self.last_value = self.minstr.get()


    def trace_var_end(self, *args):
        if self.last_value_end == "59" and self.minstrend.get() == "0":
            self.hourstrend.set(int(self.hourstrend.get()) + 1 if self.hourstrend.get() != "23" else 0)
        self.last_value_end = self.minstrend.get()
        if self.last_value_end == "0" and self.minstrend.get() == "59":
            self.hourstrend.set(int(self.hourstrend.get()) - 1 if self.hourstrend.get() != "0" else 0)
        self.last_value = self.minstrend.get()


    def submitdata(self):
        submittedpage = tk.Tk()
        submittedpage.title("Data submission")
        start_time = datetime.strptime(self.hour.get() + ':' + self.min.get(), "%H:%M")
        end_time = datetime.strptime(self.hourend.get() + ':' + self.minend.get(), "%H:%M")
        if end_time > start_time:
            ValidLabel = tk.Label(submittedpage, text="Chose Valid times!")
            ValidLabel.grid(row=1, column=0)
            filetitle = globalvar[1]
            with open(filetitle, "w+") as file:
                if file_is_empty(filetitle):
                    pass
                fileline = (
                                datetime.strftime(globalvar[0],'%Y/%b/%d') + ',' +
                                datetime.strftime(start_time,"%H:%M") +'-'+
                                datetime.strftime(end_time,"%H:%M")
                )
                file.write('\n'+fileline)

        else:
            ValidLabel = tk.Label(submittedpage, text="Please choose a start before an end!")
            ValidLabel.grid(row=1, column=0)
from tkinter import *
from timetablefunctions import getDoctorNotes, saveDoctorNotes
import time
from tkinter import messagebox



def appointmentnotes(doctoremail,appointmentid):
    # todo (longterm) use classes to display a label

    doctorsNotes = getDoctorNotes(appointmentid)
    global globalDoctorsNotes
    globalDoctorsNotes = doctorsNotes
    patientComplaint = doctorsNotes[0]
    doctorFindings = doctorsNotes[1]
    diagnosis = doctorsNotes[2]
    furtherInspections = doctorsNotes[3]
    doctorAdvice = doctorsNotes[4]

    global root
    root = Tk()
    root.title('Appointment notes for appointment ID: ' + str(appointmentid))
    root.geometry("600x800")

    complaintLabel = Label(root, text="Patient Complaint")
    complaintLabel.pack()
    global patientComplaintTextBox
    patientComplaintTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    patientComplaintTextBox.insert(END, patientComplaint)
    patientComplaintTextBox.pack(pady=20, padx=20)

    findingsLabel = Label(root, text="Doctor Findings")
    findingsLabel.pack()
    global findingsTextBox
    findingsTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    findingsTextBox.insert(END, doctorFindings)
    findingsTextBox.pack(pady=20, padx=20)

    diagnosisLabel = Label(root, text="Diagnosis")
    diagnosisLabel.pack()
    global diagnosisTextBox
    diagnosisTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    diagnosisTextBox.insert(END, diagnosis)
    diagnosisTextBox.pack(pady=20, padx=20)

    inspectionsLabel = Label(root, text="Further Inspections")
    inspectionsLabel.pack()
    global inspectionsTextBox
    inspectionsTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    inspectionsTextBox.insert(END, furtherInspections)
    inspectionsTextBox.pack(pady=20, padx=20)

    adviceLabel = Label(root, text="Doctor's Advice")
    adviceLabel.pack()
    global adviceTextBox
    adviceTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    adviceTextBox.insert(END, doctorAdvice)
    adviceTextBox.pack(pady=20, padx=20)

    # button_frame = Frame(root)
    # button_frame.pack()
    save_button = Button(root, text="Save Notes", command=saveNotes)
    save_button.pack(pady=20)
    root.mainloop()


def saveNotes():
    globalDoctorsNotes[0] = patientComplaintTextBox.get(1.0, END)
    globalDoctorsNotes[1] = findingsTextBox.get(1.0, END)
    globalDoctorsNotes[2] = diagnosisTextBox.get(1.0, END)
    globalDoctorsNotes[3] = inspectionsTextBox.get(1.0, END)
    globalDoctorsNotes[4] = adviceTextBox.get(1.0, END)
    saveDoctorNotes(globalDoctorsNotes)
    response = messagebox.askyesno("Your notes have been saved!", "Your notes have been saved. Are you finished editing your notes?")
    if response == 1:
        root.destroy()
    else:
        pass


appointmentnotes('test@gmail.com', 2)



from tkinter import *
from timetable_functions import get_doctor_notes, save_doctor_notes, get_patient_info
from prescription_med_functions import get_patient_allergies
from tkinter import messagebox, ttk


def appointment_notes(appointmentid):
    """Loads up appointment notes window"""

    # ------------------------- Pulls up data from UCH.db -------------------------
    # Pulls up existing appointment notes
    doctorsNotes = get_doctor_notes(appointmentid)
    patientComplaint = doctorsNotes[0]
    doctorFindings = doctorsNotes[1]
    diagnosis = doctorsNotes[2]
    furtherInspections = doctorsNotes[3]
    doctorAdvice = doctorsNotes[4]

    # Pulls up patient information
    patientInfo = get_patient_info(appointmentid)
    nhsNumber = patientInfo[0]
    patientEmail = patientInfo[1]
    firstName = patientInfo[2]
    lastName = patientInfo[3]
    dateOfBirth = patientInfo[4]
    gender = patientInfo[5]
    addressLine1 = patientInfo[6]
    addressLine2 = patientInfo[7]
    postcode = patientInfo[8]
    telephoneNumber = patientInfo[9]
    height = patientInfo[11]
    weight = patientInfo[12]
    bmi = patientInfo[13]

    # Pulls up patient Allergies
    allergyList = get_patient_allergies(nhsNumber)


    # ------------------------- Creates a tkinter window and lays out frame structure -------------------------
    global root
    root = Tk()
    root.title('Appointment ID: ' + str(appointmentid))
    root.geometry("1280x800")
    root.configure(background='SlateGray1')
    root.after(1000, root.focus_force)

    # Creates mainframe that encompasses all subframes
    mainFrame = Frame(root)
    mainFrame.grid()

    # Creates title frame
    titleFrame = Frame(mainFrame, bd=20, width=1350, padx=20, relief=RIDGE, background='SlateGray1')
    titleFrame.pack(side=TOP)
    appointmentTitle = Label(titleFrame, font=('arial', 20, 'bold'),
                             text='Appointment notes for patient: ' + firstName + ' ' + lastName, padx=2,
                             background='SlateGray1')
    appointmentTitle.grid()

    # Creates button frame
    buttonFrame = Frame(mainFrame, bd=20, width=1350, height=50, padx=20, relief=RIDGE, background='SlateGray1')
    buttonFrame.pack(side=BOTTOM)

    # Creates frame for where all appointment data resides
    dataFrame = Frame(mainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE, background='SlateGray1')
    dataFrame.pack(side=BOTTOM)

    # Creates a left frame for where all text boxes reside
    dataFrameLeft = LabelFrame(dataFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE,
                               font=('arial', 14, 'bold'), text='Appointment notes:', background='SlateGray1')
    dataFrameLeft.pack(side=LEFT)

    # Creates a right frame for where patient information resides
    dataFrameRight = LabelFrame(dataFrame, bd=10, width=450, height=340, padx=20, relief=RIDGE,
                                font=('arial', 14, 'bold'), text='Patient information:', background='SlateGray1')
    dataFrameRight.pack(side=RIGHT)


    # ------------------------- Creates text boxes for GP input -------------------------
    complaintLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Reason for visit:", padx=2,
                           background='SlateGray1')
    complaintLabel.grid(row=0, column=0, sticky=W)
    global patientComplaintTextBox
    patientComplaintTextBox = Text(dataFrameLeft, width=85, height=4, bd=1, bg="gray90", font=("arial", 12, 'bold'))
    patientComplaintTextBox.insert(END, patientComplaint)
    patientComplaintTextBox.grid(row=0, column=1)

    findingsLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Doctor Findings:", padx=2,
                          background='SlateGray1')
    findingsLabel.grid(row=1, column=0, sticky=W)
    global findingsTextBox
    findingsTextBox = Text(dataFrameLeft, width=85, height=4, bd=1, bg="gray90", font=("arial", 12, 'bold'))
    findingsTextBox.insert(END, doctorFindings)
    findingsTextBox.grid(row=1, column=1)

    diagnosisLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Diagnosis:", padx=2,
                           background='SlateGray1')
    diagnosisLabel.grid(row=2, column=0, sticky=W)
    global diagnosisTextBox
    diagnosisTextBox = Text(dataFrameLeft, width=85, height=4, bd=1, bg="gray90", font=("arial", 12, 'bold'))
    diagnosisTextBox.insert(END, diagnosis)
    diagnosisTextBox.grid(row=2, column=1)

    inspectionLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Further Inspections:", padx=2,
                            background='SlateGray1')
    inspectionLabel.grid(row=3, column=0, sticky=W)
    global inspectionsTextBox
    inspectionsTextBox = Text(dataFrameLeft, width=85, height=4, bd=1, bg="gray90", font=("arial", 12, 'bold'))
    inspectionsTextBox.insert(END, furtherInspections)
    inspectionsTextBox.grid(row=3, column=1)

    adviceLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Doctor's Advice:", padx=2,
                        background='SlateGray1')
    adviceLabel.grid(row=4, column=0, sticky=W)
    global adviceTextBox
    adviceTextBox = Text(dataFrameLeft, width=85, height=4, bd=1, bg="gray90", font=("arial", 12, 'bold'))
    adviceTextBox.insert(END, doctorAdvice)
    adviceTextBox.grid(row=4, column=1)


    # ------------------------- Creates patient information tabs -------------------------
    # Create notebook for tabs feature
    s = ttk.Style()
    s.configure('TNotebook.Tab', font=('URW Gothic L', '11', 'bold'))
    my_notebook = ttk.Notebook(dataFrameRight)
    my_notebook.pack()

    # Create tabs
    my_frame1 = Frame(my_notebook, width=300, height=250, bg="SlateGray2")
    my_frame2 = Frame(my_notebook, width=300, height=250, bg="SlateGray2")

    # Pack the frame the fill the container (my_notebook)
    my_frame1.pack(fill="both", expand=1)
    my_frame2.pack(fill="both", expand=1)

    # Add tabs into notebook
    my_notebook.add(my_frame1, text = 'Basic Information')
    my_notebook.add(my_frame2, text = 'Medical Allergies')


    # ------------------------- Display basic patient information within tab 1 -------------------------
    nhsNoLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="NHS Number:", padx=2, background='SlateGray2')
    nhsNoLabel.grid(row=0, column=0, sticky=W)
    nhsNoInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=str(nhsNumber), padx=2, background='SlateGray2')
    nhsNoInfo.grid(row=0, column=1, sticky=W)

    patientEmailLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Patient Email:", padx=2,
                              background='SlateGray2')
    patientEmailLabel.grid(row=1, column=0, sticky=W)
    patientEmailInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=patientEmail, padx=2,
                             background='SlateGray2')
    patientEmailInfo.grid(row=1, column=1, sticky=W)

    fNameLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="First Name:", padx=2, background='SlateGray2')
    fNameLabel.grid(row=2, column=0, sticky=W)
    fNameInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=firstName, padx=2, background='SlateGray2')
    fNameInfo.grid(row=2, column=1, sticky=W)

    fNameLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="First Name:", padx=2, background='SlateGray2')
    fNameLabel.grid(row=2, column=0, sticky=W)
    fNameInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=firstName, padx=2, background='SlateGray2')
    fNameInfo.grid(row=2, column=1, sticky=W)

    lNameLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Last Name:", padx=2, background='SlateGray2')
    lNameLabel.grid(row=3, column=0, sticky=W)
    lNameInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=lastName, padx=2, background='SlateGray2')
    lNameInfo.grid(row=3, column=1, sticky=W)

    dobLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Date of Birth:", padx=2, background='SlateGray2')
    dobLabel.grid(row=4, column=0, sticky=W)
    dobInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=dateOfBirth, padx=2, background='SlateGray2')
    dobInfo.grid(row=4, column=1, sticky=W)

    genderLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Gender:", padx=2, background='SlateGray2')
    genderLabel.grid(row=5, column=0, sticky=W)
    genderInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=gender, padx=2, background='SlateGray2')
    genderInfo.grid(row=5, column=1, sticky=W)

    address1Label = Label(my_frame1, font=('arial', 12, 'bold'), text="Address Line 1:", padx=2,
                          background='SlateGray2')
    address1Label.grid(row=6, column=0, sticky=W)
    address1Info = Label(my_frame1, font=('arial', 12, 'bold'), text=addressLine1, padx=2, background='SlateGray2')
    address1Info.grid(row=6, column=1, sticky=W)

    address2Label = Label(my_frame1, font=('arial', 12, 'bold'), text="Address Line 2:", padx=2,
                          background='SlateGray2')
    address2Label.grid(row=7, column=0, sticky=W)
    address2Info = Label(my_frame1, font=('arial', 12, 'bold'), text=addressLine2, padx=2, background='SlateGray2')
    address2Info.grid(row=7, column=1, sticky=W)

    postcodeLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Postcode:", padx=2, background='SlateGray2')
    postcodeLabel.grid(row=8, column=0, sticky=W)
    postcodeInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=postcode, padx=2, background='SlateGray2')
    postcodeInfo.grid(row=8, column=1, sticky=W)

    telephoneLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Telephone Number:", padx=2,
                           background='SlateGray2')
    telephoneLabel.grid(row=9, column=0, sticky=W)
    telephoneInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=telephoneNumber, padx=2,
                          background='SlateGray2')
    telephoneInfo.grid(row=9, column=1, sticky=W)

    heightLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Height:", padx=2,
                           background='SlateGray2')
    heightLabel.grid(row=10, column=0, sticky=W)
    if height:
        heightInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=str(height), padx=2,
                              background='SlateGray2')
    else:
        heightInfo = Label(my_frame1, font=('arial', 12, 'bold'), text='N/A', padx=2,
                           background='SlateGray2')
    heightInfo.grid(row=10, column=1, sticky=W)


    weightLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Weight:", padx=2,
                           background='SlateGray2')

    weightLabel.grid(row=11, column=0, sticky=W)

    if weight:
        weightInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=str(weight), padx=2,
                            background='SlateGray2')
    else:
        weightInfo = Label(my_frame1, font=('arial', 12, 'bold'), text='N/A', padx=2,
                        background='SlateGray2')
    weightInfo.grid(row=11, column=1, sticky=W)

    bmiLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="BMI:", padx=2,
                        background='SlateGray2')
    bmiLabel.grid(row=12, column=0, sticky=W)
    if bmi:
        bmiInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=str(bmi), padx=2,
                        background='SlateGray2')
    else:
        bmiInfo = Label(my_frame1, font=('arial', 12, 'bold'), text='N/A', padx=2,
                        background='SlateGray2')
    bmiInfo.grid(row=12, column=1, sticky=W)


    # ------------------------- Display patient allergies within tab 2 -------------------------
    # Places allergies treeview in my_frame2
    allergyTree = ttk.Treeview(my_frame2, height='5')

    # Defines our columns
    allergyTree['columns'] = ("#","Medicine Name")

    # Formats our columns
    allergyTree.column('#0', width=0, stretch=NO)
    allergyTree.column("#", anchor=CENTER, width=40)
    allergyTree.column("Medicine Name", anchor=W, width=220)

    # Creates headings
    allergyTree.heading("#0", text="", anchor=W)
    allergyTree.heading("#", text="#", anchor=CENTER)
    allergyTree.heading("Medicine Name", text="Medicine Name", anchor=W)

    # Inserts data from database into treeview
    count = 1
    for record in allergyList:
        allergyTree.insert(parent='', index='end', text="",values=(count, record))
        count += 1

    #Packs to the screen
    allergyTree.pack(pady=20)


    # ------------------------- Creates button to save notes -------------------------
    saveButton = Button(buttonFrame, text='Save Notes', font=('arial', 12, 'bold'), width=9, command=save_notes,
                        background='SlateGray1')
    saveButton.grid(row=0, column=0)


    # ------------------------- Runs tkinter -------------------------
    root.after(1000, root.focus_force)
    root.mainloop()


def save_notes():
    """Saves text box notes into UCH.db"""

    globalDoctorsNotes[0] = patientComplaintTextBox.get(1.0, END)
    globalDoctorsNotes[1] = findingsTextBox.get(1.0, END)
    globalDoctorsNotes[2] = diagnosisTextBox.get(1.0, END)
    globalDoctorsNotes[3] = inspectionsTextBox.get(1.0, END)
    globalDoctorsNotes[4] = adviceTextBox.get(1.0, END)
    save_doctor_notes(globalDoctorsNotes)
    response = messagebox.askyesno("Your notes have been saved!",
                                   "Your notes have been saved. Confirm if you want to exit.")
    if response == 1:
        root.after(1, root.destroy())
    else:
        pass

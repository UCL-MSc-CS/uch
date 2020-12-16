from tkinter import *
from timetablefunctions import getDoctorNotes, saveDoctorNotes, getPatientInfo
from tkinter import messagebox, ttk
from functools import partial
from GPs.prescription import prescription


def appointmentnotes(doctoremail, appointmentid):
    # todo (longterm) use classes to display a label
    # todo make sure doctor email is used to ensure patient confidentiality

    # Existing doctor's notes
    doctorsNotes = getDoctorNotes(appointmentid)
    global globalDoctorsNotes
    globalDoctorsNotes = doctorsNotes
    patientComplaint = doctorsNotes[0]
    doctorFindings = doctorsNotes[1]
    diagnosis = doctorsNotes[2]
    furtherInspections = doctorsNotes[3]
    doctorAdvice = doctorsNotes[4]

    # Patient information
    patientInfo = getPatientInfo(appointmentid)
    print(patientInfo)

    global globalPatientInfo
    globalPatientInfo = patientInfo
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

    firstName = 'Rich'
    lastName = 'Brian'

    global root
    root = Tk()
    root.title('Appointment ID: ' + str(appointmentid))
    root.geometry("1350x550+0+0")
    root.configure(background='SlateGray1')

    mainFrame = Frame(root)
    mainFrame.grid()

    titleFrame = Frame(mainFrame, bd=20, width=1350, padx=20, relief=RIDGE, background='SlateGray1')
    titleFrame.pack(side=TOP)

    appointmentTitle = Label(titleFrame, font=('arial', 40, 'bold'),
                             text='Appointment notes for patient: ' + firstName + ' ' + lastName, padx=2,
                             background='SlateGray1')
    appointmentTitle.grid()

    frameDetail = Frame(mainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE, background='SlateGray1')
    frameDetail.pack(side=BOTTOM)

    buttonFrame = Frame(mainFrame, bd=20, width=1350, height=50, padx=20, relief=RIDGE, background='SlateGray1')
    buttonFrame.pack(side=BOTTOM)

    dataFrame = Frame(mainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE, background='SlateGray1')
    dataFrame.pack(side=BOTTOM)

    dataFrameLeft = LabelFrame(dataFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE,
                               font=('arial', 14, 'bold'), text='Appointment notes:', background='SlateGray1')
    dataFrameLeft.pack(side=LEFT)

    dataFrameRight = LabelFrame(dataFrame, bd=10, width=450, height=340, padx=20, relief=RIDGE,
                                font=('arial', 14, 'bold'), text='Patient information:', background='SlateGray1')
    dataFrameRight.pack(side=RIGHT)

    complaintLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Patient Complaint:", padx=2,
                           background='SlateGray1')
    complaintLabel.grid(row=0, column=0, sticky=W)
    global patientComplaintTextBox
    patientComplaintTextBox = Text(dataFrameLeft, width=85, height=4, font=("arial", 12, 'bold'))
    patientComplaintTextBox.insert(END, patientComplaint)
    patientComplaintTextBox.grid(row=0, column=1)

    findingsLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Doctor Findings:", padx=2,
                          background='SlateGray1')
    findingsLabel.grid(row=1, column=0, sticky=W)
    global findingsTextBox
    findingsTextBox = Text(dataFrameLeft, width=85, height=4, font=("arial", 12, 'bold'))
    findingsTextBox.insert(END, doctorFindings)
    findingsTextBox.grid(row=1, column=1)

    diagnosisLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Diagnosis:", padx=2,
                           background='SlateGray1')
    diagnosisLabel.grid(row=2, column=0, sticky=W)
    global diagnosisTextBox
    diagnosisTextBox = Text(dataFrameLeft, width=85, height=4, font=("arial", 12, 'bold'))
    diagnosisTextBox.insert(END, diagnosis)
    diagnosisTextBox.grid(row=2, column=1)

    inspectionLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Further Inspections:", padx=2,
                            background='SlateGray1')
    inspectionLabel.grid(row=3, column=0, sticky=W)
    global inspectionsTextBox
    inspectionsTextBox = Text(dataFrameLeft, width=85, height=4, font=("arial", 12, 'bold'))
    inspectionsTextBox.insert(END, furtherInspections)
    inspectionsTextBox.grid(row=3, column=1)

    adviceLabel = Label(dataFrameLeft, font=('arial', 12, 'bold'), text="Doctor's Advice:", padx=2,
                        background='SlateGray1')
    adviceLabel.grid(row=4, column=0, sticky=W)
    global adviceTextBox
    adviceTextBox = Text(dataFrameLeft, width=85, height=4, font=("arial", 12, 'bold'))
    adviceTextBox.insert(END, doctorAdvice)
    adviceTextBox.grid(row=4, column=1)

    saveButton = Button(buttonFrame, text='Save Notes', font=('arial', 12, 'bold'), width=9, command=saveNotes,
                        background='SlateGray1')
    saveButton.grid(row=0, column=0)

    saveButton = Button(buttonFrame, text='Open prescription', font=('arial', 12, 'bold'), width=20,
                        command=partial(prescription, doctoremail, appointmentid), background='SlateGray1')
    saveButton.grid(row=0, column=1)

    # ------------------------- Patient Information -------------------------

    # Create notebook for tabs feature
    my_notebook = ttk.Notebook(dataFrameRight)
    my_notebook.pack()

    # Create blue and red tab
    my_frame1 = Frame(my_notebook, width=300, height=250, bg="SlateGray2")
    my_frame2 = Frame(my_notebook, width=300, height=250, bg="SlateGray2")

    # Pack the frame the fill the container (my_notebook)
    my_frame1.pack(fill="both", expand=1)
    my_frame2.pack(fill="both", expand=1)

    # Add tabs into notebook
    my_notebook.add(my_frame1, text = 'Basic Information')
    my_notebook.add(my_frame2, text = 'Questionnaire Answers')


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

    postcodeLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Postcode", padx=2, background='SlateGray2')
    postcodeLabel.grid(row=8, column=0, sticky=W)
    postcodeInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=postcode, padx=2, background='SlateGray2')
    postcodeInfo.grid(row=8, column=1, sticky=W)

    telephoneLabel = Label(my_frame1, font=('arial', 12, 'bold'), text="Telephone Number", padx=2,
                           background='SlateGray2')
    telephoneLabel.grid(row=9, column=0, sticky=W)
    telephoneInfo = Label(my_frame1, font=('arial', 12, 'bold'), text=telephoneNumber, padx=2,
                          background='SlateGray2')
    telephoneInfo.grid(row=9, column=1, sticky=W)

    # firstName = patientInfo[2]
    #     lastName = patientInfo[3]
    #     dateOfBirth = patientInfo[4]
    #     gender = patientInfo[5]
    #     addressLine1 = patientInfo[6]
    #     addressLine2 = patientInfo[7]
    #     postcode = patientInfo[8]
    #     telephoneNumber = patientInfo[9]

    # complaintLabel = Label(root, text="Patient Complaint")
    # complaintLabel.pack()
    # global patientComplaintTextBox
    # patientComplaintTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    # patientComplaintTextBox.insert(END, patientComplaint)
    # patientComplaintTextBox.pack(pady=20, padx=20)
    #
    # findingsLabel = Label(root, text="Doctor Findings")
    # findingsLabel.pack()
    # global findingsTextBox
    # findingsTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    # findingsTextBox.insert(END, doctorFindings)
    # findingsTextBox.pack(pady=20, padx=20)
    #
    # diagnosisLabel = Label(root, text="Diagnosis")
    # diagnosisLabel.pack()
    # global diagnosisTextBox
    # diagnosisTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    # diagnosisTextBox.insert(END, diagnosis)
    # diagnosisTextBox.pack(pady=20, padx=20)
    #
    # inspectionsLabel = Label(root, text="Further Inspections")
    # inspectionsLabel.pack()
    # global inspectionsTextBox
    # inspectionsTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    # inspectionsTextBox.insert(END, furtherInspections)
    # inspectionsTextBox.pack(pady=20, padx=20)
    #
    # adviceLabel = Label(root, text="Doctor's Advice")
    # adviceLabel.pack()
    # global adviceTextBox
    # adviceTextBox = Text(root, width=30, height=10, font=("Helvetica", 16))
    # adviceTextBox.insert(END, doctorAdvice)
    # adviceTextBox.pack(pady=20, padx=20)
    #
    #
    # # button_frame = Frame(root)
    # # button_frame.pack()
    # save_button = Button(root, text="Save Notes", command=saveNotes)
    # save_button.pack(pady=20)
    #
    root.mainloop()


def saveNotes():
    globalDoctorsNotes[0] = patientComplaintTextBox.get(1.0, END)
    globalDoctorsNotes[1] = findingsTextBox.get(1.0, END)
    globalDoctorsNotes[2] = diagnosisTextBox.get(1.0, END)
    globalDoctorsNotes[3] = inspectionsTextBox.get(1.0, END)
    globalDoctorsNotes[4] = adviceTextBox.get(1.0, END)
    saveDoctorNotes(globalDoctorsNotes)
    response = messagebox.askyesno("Your notes have been saved!",
                                   "Your notes have been saved. Are you finished editing your notes?")
    if response == 1:
        root.destroy()
    else:
        pass


appointmentnotes('matthew.shorvon@ucl.ac.uk', 1)

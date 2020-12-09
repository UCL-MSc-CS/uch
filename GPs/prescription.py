from tkinter import *
from tkinter import messagebox, ttk

def prescription():

    root = Tk()
    root.title('Prescription')
    root.geometry("1350x700+0+0")
    root.configure(background='SlateGray1')

    cmbNameTablets = StringVar()
    Ref = StringVar()
    Dose = StringVar()
    NumberTablets = StringVar()
    Lot = StringVar()
    IssuedDate = StringVar()
    ExpDate = StringVar()
    DailyDose = StringVar()
    PossibleSideEffects = StringVar()
    FurtherInformation = StringVar()
    StorageAdvice = StringVar()
    DrivingUsingMachines = StringVar()
    HowtoUseMedication = StringVar()
    PatientID = StringVar()
    PatientNHSNo = StringVar()
    PatientName = StringVar()
    DateOfBirth = StringVar()
    PatientAddress = StringVar()
    Prescription = StringVar()



    def iExit():
        iExit= messagebox.askyesno("Prescription", "Confirm if you want to exit.")
        if iExit >0:
            root.destroy()
            return

    # def iPrescription():
    #
    #     txtPrescription.insert(END, "Name of Tablets: \t\t\t" + cmbNameTablets.get() +"\n")
    #     txtPrescription.insert(END, "Reference No: \t\t\t" + Ref.get() +"\n")
    #     txtPrescription.insert(END, "Dose: \t\t\t" + Dose.get() +"\n")
    #     txtPrescription.insert(END, "Number of Tablets: \t\t\t" + NumberTablets.get() +"\n")
    #     txtPrescription.insert(END, "Further Information: \t\t\t" + FurtherInformation.get() +"\n")
    #     txtPrescription.insert(END, "Storage Advice: \t\t\t" + StorageAdvice.get() +"\n")

    def iPrescriptionData():

        txtFrameDetail.insert(END, "\t\t\t\t"+ cmbNameTablets.get() + "\t\t"+ Ref.get() +"\t"+ Dose.get() +"\t"+NumberTablets.get()+ "\t\t"+FurtherInformation.get() +"\t\t"+StorageAdvice.get() +"\n")

    def iDelete():
        cmbNameTablets.set("")
        cboNameTablet.current(0)
        Ref.set("")
        Dose.set("")
        NumberTablets.set("")
        FurtherInformation.set("")
        StorageAdvice.set("")
        txtFrameDetail.delete("1.0",END)

    def iReset():
        cmbNameTablets.set("")
        cboNameTablet.current(0)
        Ref.set("")
        Dose.set("")
        NumberTablets.set("")
        FurtherInformation.set("")
        StorageAdvice.set("")

        return

    MainFrame = Frame(root)
    MainFrame.grid()

    TitleFrame = Frame(MainFrame, bd=20, width=1350, padx=20, relief=RIDGE)
    TitleFrame.pack(side=TOP)

    lblTitle = Label(TitleFrame, font=('arial', 40, 'bold'), text="Prescription Data", padx=2)
    lblTitle.grid()

    FrameDetail = Frame(MainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
    FrameDetail.pack(side=BOTTOM)

    ButtonFrame =  Frame(MainFrame, bd=20, width=1350, height=50, padx=20, relief=RIDGE)
    ButtonFrame.pack(side=BOTTOM)

    DataFrame = Frame(MainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE)
    DataFrame.pack(side=BOTTOM)

    DataFrameLEFT = Frame(DataFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE)
    DataFrameLEFT.pack(side=LEFT)

    # DataFrameRight = LabelFrame(DataFrame, bd=10, width=450, height=300, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Prescription:")
    # DataFrameRight.pack(side=RIGHT)

    lblNameTablet = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Name of Tablets:", padx=2, pady=2)
    lblNameTablet.grid(row=0, column=0)

    cboNameTablet = ttk.Combobox(DataFrameLEFT, textvariable=cmbNameTablets, state='readonly',
                                      font=('arial', 12, 'bold'), width=20)

    cboNameTablet['value'] = ('', 'Ibuprofen', 'Co-codamol', 'Paracetamol', 'Amlodipine')
    cboNameTablet.current(0)
    cboNameTablet.grid(row=0, column=1)

    lblFurtherInfo = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Further Information:", padx=2,pady=2)
    lblFurtherInfo.grid(row=0, column=2, sticky=W)
    txtFurtherInfo = Entry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable =FurtherInformation, width=25)
    txtFurtherInfo.grid(row=0, column=3)

    lblRef = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Reference No:", padx=2,pady=2)
    lblRef.grid(row=1, column=0, sticky=W)
    txtRef = Entry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable= Ref, width=25)
    txtRef.grid(row=1, column=1)

    lblStorage = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Storage Advice:", padx=2,pady=2)
    lblStorage.grid(row=1, column=2, sticky=W)
    txtStorage = Entry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable= StorageAdvice, width=25)
    txtStorage.grid(row=1, column=3)

    lblDose = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Dose:", padx=2,pady=2)
    lblDose.grid(row=2, column=0, sticky=W)
    txtRef = Entry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable= Dose, width=25)
    txtRef.grid(row=2, column=1)

    lblNoOfTablets = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="No. of Tablets:", padx=2,pady=2)
    lblNoOfTablets.grid(row=2, column=2, sticky=W)
    txtNoOfTablets = Entry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable= NumberTablets, width=25)
    txtNoOfTablets.grid(row=2, column=3)

    # txtPrescription = Text(DataFrameRight, font=('arial', 12, 'bold'), width=43, height=12, padx=2,pady=6)
    # txtPrescription.grid(row=0, column=0)

    btnPrescription = Button(ButtonFrame, text='Save Prescription', font=('arial',12,'bold'), width=24,bd=4)
    btnPrescription.grid(row=0,column=0)

    btnPrescriptionData = Button(ButtonFrame, text='Add Drug', font=('arial',12,'bold'), width=24,bd=4, command=iPrescriptionData)
    btnPrescriptionData.grid(row=0,column=1)

    btnDelete = Button(ButtonFrame, text='Delete Drug', font=('arial',12,'bold'), width=24, bd=4, command =iDelete)
    btnDelete.grid(row=0,column=2)

    btnReset = Button(ButtonFrame, text='Reset Drug Selection', font=('arial',12,'bold'), width=24, bd=4, command=iReset)
    btnReset.grid(row=0,column=3)

    btnExit = Button(ButtonFrame, text='Exit', font=('arial',12,'bold'), width=24, bd=4, command=iExit)
    btnExit.grid(row=0,column=4)

    lblLabel = Label(FrameDetail, font=('arial', 10, 'bold'), text="Name of Tablets\tReference No.\t Dosage\t No. of Tablets\t Further Information\t Storage Advice", pady=9)
    lblLabel.grid(row=0, column=0)

    txtFrameDetail= Text(FrameDetail, font=('arial',12,'bold'), width=141, height=4, padx=2, pady=4)
    txtFrameDetail.grid(row=1, column=0)



    root.mainloop()

    #todo format it into a table
    #todo add medicine record to table row
    #todo delete medicine record from table row
    #todo scroll bar?
    #todo save into prescription
    #todo Recommended dosage frequency = stringvar()


def treeView():
    root= Tk()
    root.title('Treeview Test')
    root.geometry("700x600")

    myTree = ttk.Treeview(root)

    # Define our columns (treeview has a phantom column at the start)

    myTree['columns'] = ("Medicine ID", "Medicine Type", "Medicine Name")

    # Format our columns
    myTree.column('#0', width=0, stretch=NO)
    myTree.column("Medicine ID", anchor=CENTER, width=100)
    myTree.column("Medicine Type", anchor=W, width=140)
    myTree.column("Medicine Name", anchor=W, width=140)

    # Create headings
    myTree.heading("#0", text="", anchor=W)
    myTree.heading("Medicine ID", text="Medicine ID", anchor=CENTER)
    myTree.heading("Medicine Type", text="Medicine Type", anchor=W)
    myTree.heading("Medicine Name", text= "Medicine Name", anchor=W)

    # Get data from database
    data = [
        [17, 'Analgesics', 'Paracetamol'],
        [18, 'Antiarrhythmics', 'Digoxin'],
        [19, 'Antibiotics', 'Amoxicillin']
    ]

    # Add data
    global count
    count= 0
    for record in data:
        myTree.insert(parent='', index='end', id=count, text="", values=(record[0],record[1],record[2]))
        count += 1



    # Pack to the screen
    myTree.pack(pady=20)

    addFrame = Frame(root)
    addFrame.pack(pady=20)

    il = Label(addFrame, text="Medicine ID")
    il.grid(row=0, column=0)

    tl = Label(addFrame, text="Medicine Type")
    tl.grid(row=0, column=1)

    nl = Label(addFrame, text="Medicine Name")
    nl.grid(row=0, column=2)

    #Entry boxes

    idBox = Entry(addFrame)
    idBox.grid(row=1, column=0)

    typeBox = Entry(addFrame)
    typeBox.grid(row=1, column=1)

    nameBox = Entry(addFrame)
    nameBox.grid(row=1, column=2)

    # Add record
    def addRecord():
        global count

        myTree.insert(parent='', index='end', id=count, text="", values=(idBox.get(), typeBox.get(),nameBox.get()))
        count+= 1

        # Clear the boxes
        idBox.delete(0,END)
        typeBox.delete(0,END)
        nameBox.delete(0,END)

    # Remove all records
    def removeAll():
        for record in myTree.get_children():
            myTree.delete(record)

    # Remove one selected
    def removeSelected():
        x = myTree.selection()
        for record in x:
            myTree.delete(record)


    # Buttons
    addRecord = Button(root, text="Add Medicine", command=addRecord)
    addRecord.pack(pady=20)

    # Remove all
    removeAll = Button(root, text="Remove All Medicine", command=removeAll)
    removeAll.pack(pady=10)

    # Remove one
    removeSelected = Button(root, text="Remove Selected Medicine", command=removeSelected)
    removeSelected.pack(pady=10)


    root.mainloop()

treeView()
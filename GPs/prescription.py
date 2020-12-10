from tkinter import *
from tkinter import messagebox, ttk
import medicinesearchfunctions as ms

def prescription(doctoremail,appointmentID):

    root = Tk()
    root.title('Appointment ID: ' + str(appointmentID))
    root.geometry("1920x950")

    mainFrame = Frame(root)
    mainFrame.grid()

    # titleFrame = Frame(mainFrame, bd=20, width=1350, padx=20, relief=RIDGE)
    # titleFrame.pack(side=TOP)

    # titleLabel = Label(titleFrame, font=('arial', 40, 'bold'), text='Prescription ID: ' + str(prescriptionID), padx=8)
    # titleLabel.grid()

    # Frame for prescriptions treeview (bottom)
    bottomFrame = Frame(mainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
    bottomFrame.pack(side=BOTTOM)

    # Frame for select and print medicine sections (top)
    medicineFrame = Frame(mainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE)
    medicineFrame.pack(side=BOTTOM)

    # Final medicine section
    prescriptionFrame = LabelFrame(bottomFrame, bd=10, width=450, height=300, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Final Prescription:")
    prescriptionFrame.pack(side=BOTTOM)

    # Select medicine section --------------------------------------------
    medSelectFrame = LabelFrame(medicineFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Select Medicine:")
    medSelectFrame.pack(side=LEFT)


    def submitmedsearch():

        trv.delete(*trv.get_children())

        global medsearchstring, drugsearchstring, dtype, mtype, ctype, results
        medsearchstring = mednamesearch.get()
        drugsearchstring = drugnamesearch.get()
        dtype = chosendosetype.get()
        mtype = chosenmedtype.get()
        ctype = chosencategory.get()

        results = ms.search(medsearchstring, drugsearchstring, dtype, mtype, ctype)
        for result in results:
            trv.insert('', 'end', values=result)


    dosage_types = ms.alldosagetypes()
    medicine_types = ms.allmedtypes()
    categories = ms.allcategories()

    chosendosetype = StringVar()
    chosenmedtype = StringVar()
    chosencategory = StringVar()

    mednamelabel = Label(medSelectFrame, text="Type name of Medicine")
    mednamelabel.pack()
    mednamesearch = Entry(medSelectFrame)
    mednamesearch.pack()

    drugnamelabel = Label(medSelectFrame, text="Type name of Drug")
    drugnamelabel.pack()
    drugnamesearch = Entry(medSelectFrame)
    drugnamesearch.pack()

    dtlabel = Label(medSelectFrame, text="Select your dosage type")
    dtlabel.pack()
    dosetypedropmenu = OptionMenu(medSelectFrame, chosendosetype, *dosage_types)
    dosetypedropmenu.pack()

    mtlabel = Label(medSelectFrame, text="Select your medicine type")
    mtlabel.pack()
    medtypedropmenu = OptionMenu(medSelectFrame, chosenmedtype, *medicine_types)
    medtypedropmenu.pack()

    catlabel = Label(medSelectFrame, text="Select your categories")
    catlabel.pack()
    catdropmenu = OptionMenu(medSelectFrame, chosencategory, *categories)
    catdropmenu.pack()

    medsearchsubmit = Button(medSelectFrame, text="Search Medicine", command=submitmedsearch)
    medsearchsubmit.pack()

    # Print search medicine section --------------------------------------------
    medResultsFrame = LabelFrame(medicineFrame, bd=10, width=350, height=250, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Medicine Results:")
    medResultsFrame.pack(side=RIGHT)

    def enterintodisabled(textbox, string):
        textbox.config(state=NORMAL)
        textbox.delete('1.0', END)
        textbox.insert(END, string)
        textbox.config(state=DISABLED)

    def submitchoice():
        if trv.selection():
            for row in trv.selection():
                selected_medicine = trv.item(row, "values")
                # print(selected_medicine)
                break
            enterintodisabled(medid, selected_medicine[0])
            enterintodisabled(medname, selected_medicine[1])
            enterintodisabled(doseType, selected_medicine[3])
            dosages = selected_medicine[7].split(";")
            global chosendose
            chosendose = StringVar()
            chosendose.set(dosages[0])
            global dosagedropdown
            dosagedropdown = OptionMenu(chosenmedframe, chosendose, *dosages)
            dosagedropdown.grid(row=2, column=3)

    # Add record
    def addRecord():
        global count

        myTree.insert(parent='', index='end', id=count, text="", values=(medid.get(1.0,END), medname.get(1.0,END), chosendose.get(), multiplier.get(1.0,END), doseType.get(1.0,END), furtherInformation.get(1.0,END)))
        count+= 1

        # Clear the boxes
        medid.config(state=NORMAL)
        medname.config(state=NORMAL)
        doseType.config(state=NORMAL)
        medid.delete('1.0',END)
        medname.delete('1.0',END)
        multiplier.delete('1.0',END)
        doseType.delete('1.0',END)
        furtherInformation.delete('1.0',END)
        dosagedropdown.destroy()
        medid.config(state=DISABLED)
        medname.config(state=DISABLED)
        doseType.config(state=DISABLED)





    tree_frame = Frame(medResultsFrame)
    tree_frame.pack(pady = 20, padx = 20)

    tree_scroll = Scrollbar(tree_frame,orient = HORIZONTAL)
    tree_scroll.pack(fill=X,side=BOTTOM)

    global trv
    trv = ttk.Treeview(
        tree_frame,
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        show='headings',
        height='5',
        selectmode="browse",
        xscrollcommand=tree_scroll.set
    )
    trv.pack()

    trv.heading(1, text="ID")
    trv.column(1,width=50)
    trv.heading(2, text="Medicine Name")
    trv.heading(3, text="Type")
    trv.column(3, width=80)
    trv.heading(4, text="Dosage method")
    trv.column(4, width=100)
    trv.heading(5, text="Drug route")
    trv.column(5, width=100)
    trv.heading(6, text="Manufacturer")
    trv.column(6, width=100)
    trv.heading(7, text="Drug")
    trv.heading(8, text="Dosages")
    trv.column(8, width=100)
    trv.heading(9, text="Units")
    trv.column(9, width=100)
    trv.heading(10, text="Pharma class")
    trv.heading(11, text="Category")

    tree_scroll.config(command = trv.xview)


    choosemedbutton = Button(medResultsFrame, text="Choose medicine", command=submitchoice)
    choosemedbutton.pack()

    global chosenmedframe
    chosenmedframe = LabelFrame(medResultsFrame,text="Chosen medicine",padx=20,pady=20)
    chosenmedframe.pack()

    medidlabel = Label(chosenmedframe,text="ID")
    medidlabel.grid(row=1,column=1)
    global medid
    medid = Text(chosenmedframe, height=1, width=10,state=DISABLED)
    medid.grid(row=2,column=1)

    mednamelabel = Label(chosenmedframe,text="Medicine")
    mednamelabel.grid(row=1,column=2)
    global medname
    medname = Text(chosenmedframe, height=1, width=30,state=DISABLED)
    medname.grid(row=2,column=2)

    doselabel = Label(chosenmedframe, text="Dose")
    doselabel.grid(row=1, column=3)

    multiplabel = Label(chosenmedframe, text="Dose-Multiplier")
    multiplabel.grid(row=1, column=4)
    multiplier = Text(chosenmedframe, height=1, width=5)
    multiplier.grid(row=2,column=4)

    Typelabel = Label(chosenmedframe, text="Type")
    Typelabel.grid(row=1, column=5)
    global doseType
    doseType = Text(chosenmedframe, height=1, width=30,state=DISABLED)
    doseType.grid(row=2,column=5)

    Freqlabel = Label(chosenmedframe, text="Further Information")
    Freqlabel.grid(row=1, column=6)
    furtherInformation = Text(chosenmedframe, height=1, width=40)
    furtherInformation.grid(row=2,column=6)

    addRecord = Button(medResultsFrame, text="Add Medicine", command=addRecord)
    addRecord.pack(pady=10)

    # place treeview in prescription frame
    myTree = ttk.Treeview(prescriptionFrame)

    # Define our columns (treeview has a phantom column at the start)
    myTree['columns'] = ("Medicine ID", "Medicine Name", "Dosage", "Dosage Multiplier", "Dosage Type", "Further Information")

    # Format our columns
    myTree.column('#0', width=0, stretch=NO)
    myTree.column("Medicine ID", anchor=CENTER, width=100)
    myTree.column("Medicine Name", anchor=W, width=140)
    myTree.column("Dosage", anchor=CENTER, width=140)
    myTree.column("Dosage Multiplier", anchor=CENTER, width=140)
    myTree.column("Dosage Type", anchor=CENTER, width=140)
    myTree.column("Further Information", anchor=W, width=140)


    # Create headings
    myTree.heading("#0", text="", anchor=W)
    myTree.heading("Medicine ID", text="Medicine ID", anchor=CENTER)
    myTree.heading("Medicine Name", text="Medicine Name", anchor=W)
    myTree.heading("Dosage", text="Dosage", anchor=CENTER)
    myTree.heading("Dosage Multiplier", text="Dosage Multiplier", anchor=CENTER)
    myTree.heading("Dosage Type", text="Dosage Type", anchor=CENTER)
    myTree.heading("Further Information", text="Further Information", anchor=W)


    # Get data from database
    data = [

    ]

    # Add data
    global count
    count= 0
    for record in data:
        myTree.insert(parent='', index='end', id=count, text="", values=(record[0],record[1],record[2]))
        count += 1

    # Pack to the screen
    myTree.pack(pady=20)

    # addFrame = Frame(medSelectFrame)
    # addFrame.pack(pady=20)

    # il = Label(addFrame, text="Medicine ID")
    # il.grid(row=0, column=0)
    #
    # tl = Label(addFrame, text="Medicine Type")
    # tl.grid(row=0, column=1)
    #
    # nl = Label(addFrame, text="Medicine Name")
    # nl.grid(row=0, column=2)
    #
    # #Entry boxes
    # idBox = Entry(addFrame)
    # idBox.grid(row=1, column=0)
    #
    # typeBox = Entry(addFrame)
    # typeBox.grid(row=1, column=1)
    #
    # nameBox = Entry(addFrame)
    # nameBox.grid(row=1, column=2)

    # Remove all records
    def removeAll():
        for record in myTree.get_children():
            myTree.delete(record)

    # Remove one selected
    def removeSelected():
        x = myTree.selection()[0]
        myTree.delete(x)

    # Saves prescription data into database
    def savePrescription():
        #todo connect to database and insert new data
        for record in myTree.get_children():
            prescriptionLine = myTree.item(record, "values")
            prescriptionList = list(prescriptionLine)
            prescriptionList.insert(0, appointmentID)
            prescriptionList.pop(2)
            prescriptionList.pop(4)
            ms.addPrescription(prescriptionList)




        exit = messagebox.askyesno("Save Prescription", "Confirm if you want to exit.")
        if exit > 0:
            root.destroy()
            return

    # Buttons
    # addRecord = Button(medSelectFrame, text="Add Medicine", command=addRecord)
    # addRecord.pack(pady=10)

    # Remove all
    removeAll = Button(prescriptionFrame, text="Remove All Medicine", command=removeAll)
    removeAll.pack(pady=5)

    # Remove one
    removeSelected = Button(prescriptionFrame, text="Remove Selected Medicine", command=removeSelected)
    removeSelected.pack(pady=5)

    # Save prescription
    savePrescription = Button(prescriptionFrame, text="Save Prescription", command=savePrescription)
    savePrescription.pack(pady=5)


    root.mainloop()


from tkinter import *
from tkinter import messagebox, ttk
import prescription_med_functions as ms
from GPs.help_page import help_page

def prescription(doctoremail,appointmentID,nhsNumber):
    """Loads up prescription page"""

    # ------------------------- Pulls up data from UCH.db -------------------------
    # Pulls all saved prescription records from the database
    prescriptionData = ms.get_prescription_from_db(appointmentID)

    # Pulls medicine IDs from prescription database
    treeviewMedID = []
    for medicine in prescriptionData:
        treeviewMedID.append(medicine[0])

    # ------------------------- Creates a tkinter window and lays out frame structure -------------------------
    root = Tk()
    root.title('Appointment ID: ' + str(appointmentID) + ', with Dr. ' + doctoremail)
    root.geometry("1920x950")

    # Creates mainframe that encompasses all subframes
    mainFrame = Frame(root)
    mainFrame.grid()

    # Creates top frame
    topFrame = Frame(mainFrame, bd=20, width=1350, height=400, padx=10, relief=RIDGE)
    topFrame.pack(side=TOP)

    # Creates bottom frame
    bottomFrame = Frame(mainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
    bottomFrame.pack(side=BOTTOM)

    # Creates search medicine frame
    medSearchFrame = LabelFrame(topFrame, bd=10, width=800, height=300, padx=10, relief=RIDGE, font=('arial', 12, 'bold'), text="Step 1. Search Medicine:")
    medSearchFrame.pack(side=LEFT)

    # Creates medicine results frame
    medResultsFrame = LabelFrame(topFrame, bd=10, width=800, height=300, padx=5, relief=RIDGE, font=('arial', 12, 'bold'), text="Step 2. Choose Medicine Search Results:")
    medResultsFrame.pack(side=RIGHT)

    # Creates frame for confirm final prescription section
    prescriptionFrame = LabelFrame(bottomFrame, bd=10, width=450, height=300, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Step 3. Confirm Final Prescription:")
    prescriptionFrame.pack(side=TOP)

    # Creates frame for i instructions section
    instructionFrame = LabelFrame(bottomFrame, bd=10, width=225, height=50, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Need help? Here is a guide:")
    instructionFrame.pack(side=BOTTOM)


    # ------------------------- Seach medicine functionality -------------------------
    def submit_medicine_search():
        """Pulls all medicine from database based on GP search preferences and displays it on a treeview"""

        trv.delete(*trv.get_children())

        global medsearchstring, drugsearchstring, dtype, mtype, ctype, results
        medsearchstring = mednamesearch.get()
        drugsearchstring = drugnamesearch.get()
        dtype = chosendosetype.get()
        mtype = chosenmedtype.get()
        ctype = chosencategory.get()

        results = ms.medicine_search(medsearchstring, drugsearchstring, dtype, mtype, ctype)
        for result in results:
            trv.insert('', 'end', values=result)

    # Displays input categories for searching medicine
    dosage_types = ms.get_all_dosage_types()
    dosage_types.insert(0,"-")
    medicine_types = ms.get_all_med_types()
    medicine_types.insert(0,"-")
    categories = ms.get_all_med_categories()
    categories.insert(0,"-")

    chosendosetype = StringVar(value="-")
    chosenmedtype = StringVar(value="-")
    chosencategory = StringVar(value="-")

    mednamelabel = Label(medSearchFrame, text="Medicine name/Brand name")
    mednamelabel.pack()
    mednamesearch = Entry(medSearchFrame)
    mednamesearch.config(width = 25)
    mednamesearch.pack()

    drugnamelabel = Label(medSearchFrame, text="Drug name/Active Ingredient")
    drugnamelabel.pack()
    drugnamesearch = Entry(medSearchFrame)
    drugnamesearch.config(width = 25)
    drugnamesearch.pack()

    dtlabel = Label(medSearchFrame, text="Dosage type")
    dtlabel.pack()
    dosetypedropmenu = OptionMenu(medSearchFrame, chosendosetype, *dosage_types)
    dosetypedropmenu.config(width = 20)
    dosetypedropmenu.pack()

    mtlabel = Label(medSearchFrame, text="Medicine type")
    mtlabel.pack()
    medtypedropmenu = OptionMenu(medSearchFrame, chosenmedtype, *medicine_types)
    medtypedropmenu.config(width = 20)
    medtypedropmenu.pack()

    catlabel = Label(medSearchFrame, text="Categories")
    catlabel.pack()
    catdropmenu = OptionMenu(medSearchFrame, chosencategory, *categories)
    catdropmenu.config(width = 20)
    catdropmenu.pack()

    medsearchsubmit = Button(medSearchFrame, text="Search Medicine", command=submit_medicine_search)
    medsearchsubmit.pack(pady=10)

    # ------------------------- Medicine results functionality -------------------------
    def enter_into_disabled_box(textbox, string):
        """Displays selected medicine data into unalterable boxes for the user"""

        textbox.config(state=NORMAL)
        textbox.delete(0, END)
        textbox.insert(0, string)
        textbox.config(state=DISABLED)

    def submit_choice():
        """Displays data of the selected medicine within entry boxes of the chosen medicine section"""

        if trv.selection():
            for row in trv.selection():
                selected_medicine = trv.item(row, "values")
                break
            enter_into_disabled_box(medid, selected_medicine[0])
            enter_into_disabled_box(medname, selected_medicine[1])
            enter_into_disabled_box(doseType, selected_medicine[3])
            dosages = selected_medicine[7].split(";")
            global chosendose
            chosendose = StringVar()
            chosendose.set(dosages[0])
            global dosagedropdown
            dosagedropdown = OptionMenu(chosenmedframe, chosendose, *dosages)
            dosagedropdown.config(width = 10)
            dosagedropdown.grid(row=2, column=3)


    def add_record():
        """Adds record into confirm final prescription treeview"""

        if medid.get() and int(medid.get()) not in treeviewMedID:
            treeviewMedID.append(int(medid.get()))
            doseUnit = ms.get_medicine_units(medid.get())

            global count
            addvalues = (
                            medid.get(),
                            medname.get(),
                            str(chosendose.get()) + " " + doseUnit[0],
                            str(multiplier.get()) + 'x',
                            doseType.get(),
                            furtherInformation.get()
            )
            myTree.insert(parent='', index='end', id=count, text="", values=addvalues)
            count+= 1

            # Clear the boxes
            medid.config(state=NORMAL)
            medname.config(state=NORMAL)
            doseType.config(state=NORMAL)
            multiplier.config(state=NORMAL)
            medid.delete(0,END)
            medname.delete(0,END)
            multiplier.delete(0, END)
            multiplier.insert(0,1)
            doseType.delete(0,END)
            furtherInformation.delete(0,END)
            dosagedropdown.destroy()
            medid.config(state=DISABLED)
            medname.config(state=DISABLED)
            doseType.config(state=DISABLED)
            multiplier.config(state='readonly')
            potential_allergy = ms.allergy_message_handler(nhsNumber, addvalues[1])
            if potential_allergy:
                messagebox.showerror("Warning!", potential_allergy)

        elif not medid.get():
            messagebox.showerror("Error", "Please choose a medicine before you click 'Add Medicine'")
        elif int(medid.get()) in treeviewMedID:
            messagebox.showerror("Error", "You have added a medicine that already exists in your final prescriptions.")


    # Places medicine results treeview in medicine results frame
    global trv
    trv = ttk.Treeview(
        medResultsFrame,
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        show='headings',
        height='5',
        selectmode="browse"
    )

    # Packs to the screen
    trv.pack(pady=5)

    # Formats columns and headings
    trv.heading(1, text="ID")
    trv.column(1,width=45)
    trv.heading(2, text="Medicine Name")
    trv.column(2, width=120)
    trv.heading(3, text="Type")
    trv.column(3, width=90)
    trv.heading(4, text="Dosage Method")
    trv.column(4, width=100)
    trv.heading(5, text="Drug Route")
    trv.column(5, width=100)
    trv.heading(6, text="Manufacturer")
    trv.column(6, width=100)
    trv.heading(7, text="Drug")
    trv.column(7, width=100)
    trv.heading(8, text="Dosage")
    trv.column(8, width=75)
    trv.heading(9, text="Units")
    trv.column(9, width=100)
    trv.heading(10, text="Pharma class")
    trv.column(10, width=100)
    trv.heading(11, text="Category")
    trv.column(11, width=100)

    # Creates choose medicine button
    choosemedbutton = Button(medResultsFrame, text="Choose medicine", command=submit_choice)
    choosemedbutton.pack(pady=10)

    # Creates chosen medicine frame
    global chosenmedframe
    chosenmedframe = LabelFrame(medResultsFrame,text="Chosen medicine",padx=20,pady=20)
    chosenmedframe.pack(pady=10,padx=10)

    # Creates chosen medicine data boxes and displays respective data within these boxes
    medidlabel = Label(chosenmedframe,text="Medicine ID")
    medidlabel.grid(row=1,column=1)
    global medid
    medid = Entry(chosenmedframe, width=5,state=DISABLED,disabledbackground="white",disabledforeground="black")
    medid.grid(row=2,column=1)

    mednamelabel = Label(chosenmedframe,text="Medicine Name")
    mednamelabel.grid(row=1,column=2)
    global medname
    medname = Entry(chosenmedframe, width=30,state=DISABLED,disabledbackground="white",disabledforeground="black")
    medname.grid(row=2,column=2)

    doselabel = Label(chosenmedframe, text="Dosage")
    doselabel.grid(row=1, column=3)

    multiplabel = Label(chosenmedframe, text="Dose-Multiplier")
    multiplabel.grid(row=1, column=4)
    multiplier = Spinbox(chosenmedframe,from_ = 1, to = 100 ,width=5,state='readonly',readonlybackground='white')
    multiplier.grid(row=2,column=4)

    Typelabel = Label(chosenmedframe, text="Dosage Method")
    Typelabel.grid(row=1, column=5)
    global doseType
    doseType = Entry(chosenmedframe, width=10,state=DISABLED,disabledbackground="white",disabledforeground="black")
    doseType.grid(row=2,column=5)

    Freqlabel = Label(chosenmedframe, text="Further Information")
    Freqlabel.grid(row=1, column=6)
    furtherInformation = Entry(chosenmedframe, width=40)
    furtherInformation.grid(row=2,column=6)

    # Creates add record button
    addRecord = Button(medResultsFrame, text="Add Medicine", command=add_record)
    addRecord.pack(pady=10)


    # ------------------------- Confirm final prescriptions functionality -------------------------
    # Places treeview in prescription frame
    myTree = ttk.Treeview(prescriptionFrame, height='5')

    # Defines treeview columns
    myTree['columns'] = ("Medicine ID", "Medicine Name", "Dosage", "Dosage Multiplier", "Dosage Method", "Further Information")

    # Formats treeview columns
    myTree.column('#0', width=0, stretch=NO)
    myTree.column("Medicine ID", anchor=CENTER, width=100)
    myTree.column("Medicine Name", anchor=W, width=140)
    myTree.column("Dosage", anchor=CENTER, width=140)
    myTree.column("Dosage Multiplier", anchor=CENTER, width=140)
    myTree.column("Dosage Method", anchor=CENTER, width=140)
    myTree.column("Further Information", anchor=W, width=140)

    # Creates headings
    myTree.heading("#0", text="", anchor=W)
    myTree.heading("Medicine ID", text="Medicine ID", anchor=CENTER)
    myTree.heading("Medicine Name", text="Medicine Name", anchor=W)
    myTree.heading("Dosage", text="Dosage", anchor=CENTER)
    myTree.heading("Dosage Multiplier", text="Dosage Multiplier", anchor=CENTER)
    myTree.heading("Dosage Method", text="Dosage Method", anchor=CENTER)
    myTree.heading("Further Information", text="Further Information", anchor=W)

    # Adds any record from prescriptionData and adds it into final prescription treeview
    global count
    count= 0
    for record in prescriptionData:
        myTree.insert(parent='', index='end', id=count, text="", values=(record[0],record[1],record[2],record[3],record[4],record[5]))
        count += 1

    # Packs to the screen
    myTree.pack(pady=20)

    def remove_all():
        """Removes all records"""
        treeviewMedID.clear()
        for record in myTree.get_children():
            myTree.delete(record)

    def remove_selected():
        """Remove selected record(s)"""
        for selection in myTree.selection():
            selectionID = int(myTree.item(selection, "values")[0])
            treeviewMedID.remove(selectionID)
            myTree.delete(selection)

    def save_prescription():
        """Saves prescription data into UCH.db"""
        ms.delete_med_record(appointmentID)
        for record in myTree.get_children():
            prescriptionLine = myTree.item(record, "values")
            prescriptionList = list(prescriptionLine)
            prescriptionList.insert(0, appointmentID)
            prescriptionList.pop(2)
            prescriptionList.pop(4)

            ms.add_prescription_to_db(prescriptionList)

        exit = messagebox.askyesno("Save Prescription", "Confirm if you want to exit.")
        if exit > 0:
            root.after(1, root.destroy())
            return

    # Creates remove all button
    removeAll = Button(prescriptionFrame, text="Remove All Medicine", command=remove_all)
    removeAll.pack(pady=5)

    # Creates remove selected button
    removeSelected = Button(prescriptionFrame, text="Remove Selected Medicine", command=remove_selected)
    removeSelected.pack(pady=5)

    # Creates save prescription button
    savePrescription = Button(prescriptionFrame, text="Save Prescription", command=save_prescription)
    savePrescription.pack(pady=5)

    # Creates user guide button
    instructionButton = Button(instructionFrame, text='User Guide', command=help_page,
                               background='SlateGray1')
    instructionButton.pack(pady=5)

    # ------------------------- Runs tkinter -------------------------
    root.after(1000, root.focus_force)
    root.mainloop()

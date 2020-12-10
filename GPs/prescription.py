from tkinter import *
from tkinter import messagebox, ttk

def prescription(prescriptionID):

    root = Tk()
    root.title('Prescription ID: ' + str(prescriptionID))
    root.geometry("1100x850")

    mainFrame = Frame(root)
    mainFrame.grid()

    titleFrame = Frame(mainFrame, bd=20, width=1350, padx=20, relief=RIDGE)
    titleFrame.pack(side=TOP)

    titleLabel = Label(titleFrame, font=('arial', 40, 'bold'), text='Prescription ID: ' + str(prescriptionID), padx=8)
    titleLabel.grid()

    # Frame for prescriptions treeview (bottom)
    bottomFrame = Frame(mainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
    bottomFrame.pack(side=BOTTOM)

    # Frame for select and print medicine sections (top)
    medicineFrame = Frame(mainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE)
    medicineFrame.pack(side=BOTTOM)

    # Final medicine section
    prescriptionFrame = LabelFrame(bottomFrame, bd=10, width=450, height=300, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Final Prescription:")
    prescriptionFrame.pack(side=BOTTOM)

    # Select medicine section
    medSelectFrame = LabelFrame(medicineFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Select Medicine:")
    medSelectFrame.pack(side=LEFT)

    # Print search medicine section
    medResultsFrame = LabelFrame(medicineFrame, bd=10, width=350, height=250, padx=20, relief=RIDGE, font=('arial', 12, 'bold'), text="Medicine Results:")
    medResultsFrame.pack(side=RIGHT)

    # place treeview in prescription frame
    myTree = ttk.Treeview(prescriptionFrame)

    # Define our columns (treeview has a phantom column at the start)
    myTree['columns'] = ("Medicine ID", "Medicine Name", "Dosage", "Dosage Multiplier", "Frequency")

    # Format our columns
    myTree.column('#0', width=0, stretch=NO)
    myTree.column("Medicine ID", anchor=CENTER, width=100)
    myTree.column("Medicine Name", anchor=W, width=140)
    myTree.column("Dosage", anchor=W, width=140)
    myTree.column("Dosage Multiplier", anchor=CENTER, width=140)
    myTree.column("Frequency", anchor=W, width=140)


    # Create headings
    myTree.heading("#0", text="", anchor=W)
    myTree.heading("Medicine ID", text="Medicine ID", anchor=CENTER)
    myTree.heading("Medicine Name", text="Medicine Name", anchor=W)
    myTree.heading("Dosage", text="Dosage", anchor=W)
    myTree.heading("Dosage Multiplier", text="Dosage Multiplier", anchor=CENTER)
    myTree.heading("Frequency", text="Frequency", anchor=W)


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

    addFrame = Frame(medSelectFrame)
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
        x = myTree.selection()[0]
        myTree.delete(x)

    # Saves prescription data into database
    def savePrescription():
        #todo connect to database and insert new data
        exit = messagebox.askyesno("Save Prescription", "Confirm if you want to exit.")
        if exit > 0:
            root.destroy()
            return

    # Buttons
    addRecord = Button(medSelectFrame, text="Add Medicine", command=addRecord)
    addRecord.pack(pady=10)

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


prescription(4)
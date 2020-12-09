from tkinter import *
from tkinter import messagebox, ttk

def prescription(doctoremail,appointmentid):

    root = Tk()
    root.title('Prescription')
    root.geometry("700x750")

    mainFrame = Frame(root)
    mainFrame.grid()

    titleFrame = Frame(mainFrame, bd=20, width=1350, padx=20, relief=RIDGE)
    titleFrame.pack(side=TOP)

    titleLabel = Label(titleFrame, font=('arial', 40, 'bold'), text="Prescription", padx=2)
    titleLabel.grid()

    prescriptionFrame = Frame(mainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
    prescriptionFrame.pack(side=BOTTOM)

    selectionFrame = Frame(mainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
    selectionFrame.pack(side=BOTTOM)

    myTree = ttk.Treeview(prescriptionFrame)

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
    myTree.heading("Medicine Name", text="Medicine Name", anchor=W)

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

    addFrame = Frame(selectionFrame)
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
    addRecord = Button(selectionFrame, text="Add Medicine", command=addRecord)
    addRecord.pack(pady=10)

    # Remove all
    removeAll = Button(selectionFrame, text="Remove All Medicine", command=removeAll)
    removeAll.pack(pady=10)

    # Remove one
    removeSelected = Button(selectionFrame, text="Remove Selected Medicine", command=removeSelected)
    removeSelected.pack(pady=10)

    # Save prescription
    savePrescription = Button(prescriptionFrame, text="Save Prescription", command=savePrescription)
    savePrescription.pack(pady=10)


    root.mainloop()


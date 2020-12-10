from tkinter import *
from tkinter.ttk import Treeview
import medicinesearchfunctions as ms

def enterintodisabled(textbox,string):
    textbox.config(state=NORMAL)
    textbox.delete('1.0', END)
    textbox.insert(END,string)
    textbox.config(state=DISABLED)

def submitchoice():
    if trv.selection():
        for row in trv.selection():
            selected_medicine = trv.item(row,"values")
            #print(selected_medicine)
            break
        enterintodisabled(medid,selected_medicine[0])
        enterintodisabled(medname,selected_medicine[1])
        enterintodisabled(doseType,selected_medicine[3])
        dosages = selected_medicine[7].split(";")
        chosendose = StringVar()
        chosendose.set(dosages[0])
        dosagedropdown = OptionMenu(chosenmedframe,chosendose,*dosages)
        dosagedropdown.grid(row=2,column=3)

def medsearchresultspage(medsearchstring, drugsearchstring, dtype, mtype, ctype):
    results = ms.search(medsearchstring, drugsearchstring, dtype, mtype, ctype)

    global search_results
    search_results = Toplevel()
    search_results.title("Here are your results")
    search_results.geometry("1200x400")

    tree_frame = Frame(search_results)
    tree_frame.pack(pady = 20, padx = 20)

    tree_scroll = Scrollbar(tree_frame,orient = HORIZONTAL)
    tree_scroll.pack(fill=X,side=BOTTOM)

    global trv
    trv = Treeview(
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

    for result in results:
        trv.insert('','end',values = result)

    choosemedbutton = Button(search_results, text="Choose medicine", padx=20, pady=20,command=submitchoice)
    choosemedbutton.pack()

    global chosenmedframe
    chosenmedframe = LabelFrame(search_results,text="Chosen medicine",padx=20,pady=20)
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

    Freqlabel = Label(chosenmedframe, text="Frequency")
    Freqlabel.grid(row=1, column=6)
    Frequency = Text(chosenmedframe, height=1, width=40)
    Frequency.grid(row=2,column=6)

    search_results.mainloop()
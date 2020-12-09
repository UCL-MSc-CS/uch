from tkinter import *
from tkinter.ttk import Treeview
import medicinesearchfunctions as ms

def submitchoice():
    for row in trv.selection():
        global selected_medicine
        selected_medicine = trv.item(row,"values")
        print(selected_medicine)
        break
    search_results.destroy()

def medsearchresultspage(medsearchstring, drugsearchstring, dtype, mtype, ctype):
    results = ms.search(medsearchstring, drugsearchstring, dtype, mtype, ctype)

    global search_results
    search_results = Toplevel()
    search_results.title("Here are your results")
    search_results.geometry("1000x750")

    tree_frame = Frame(search_results)
    tree_frame.pack(pady = 20, padx = 20)

    tree_scroll = Scrollbar(tree_frame,orient = HORIZONTAL)
    tree_scroll.pack(fill=X,side=BOTTOM)

    global trv
    trv = Treeview(
        tree_frame,
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        show='headings',
        height='30',
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

    submitbutton = Button(search_results, text="Submit choice", padx=20, pady=20,command=submitchoice)
    submitbutton.pack()

    search_results.mainloop()
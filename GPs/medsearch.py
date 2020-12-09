from tkinter import *
import medicinesearchfunctions as ms
from GPs.medsearchresults import medsearchresultspage

def submitmedsearch():
    medsearchstring = mednamesearch.get(1.0,END)
    drugsearchstring = drugnamesearch.get(1.0,END)
    dtype = chosendosetype.get()
    mtype = chosenmedtype.get()
    ctype = chosencategory.get()
    medsearchresultspage(medsearchstring, drugsearchstring, dtype, mtype, ctype)


dosage_types = ms.alldosagetypes()
medicine_types = ms.allmedtypes()
categories = ms.allcategories()

searchpage = Tk()
searchpage.title("Search for your medicines")
searchpage.geometry("400x300")

chosendosetype = StringVar()
chosenmedtype = StringVar()
chosencategory = StringVar()

mednamelabel = Label(searchpage,text="Type name of Medicine")
mednamelabel.pack()
mednamesearch = Text(searchpage,height =1,width = 40)
mednamesearch.pack()

drugnamelabel = Label(searchpage,text="Type name of Drug")
drugnamelabel.pack()
drugnamesearch = Text(searchpage,height =1,width = 40)
drugnamesearch.pack()

dtlabel = Label(searchpage,text="Select your dosage type")
dtlabel.pack()
dosetypedropmenu = OptionMenu(searchpage,chosendosetype,*dosage_types)
dosetypedropmenu.pack()

mtlabel = Label(searchpage,text="Select your medicine type")
mtlabel.pack()
medtypedropmenu = OptionMenu(searchpage,chosenmedtype,*medicine_types)
medtypedropmenu.pack()

catlabel = Label(searchpage,text="Select your categories")
catlabel.pack()
catdropmenu = OptionMenu(searchpage,chosencategory,*categories)
catdropmenu.pack()

medsearchsubmit = Button(searchpage,text = "Submit",command = submitmedsearch,padx=10,pady=10)
medsearchsubmit.pack()

searchpage.mainloop()



from PIL import Image, ImageTk
from tkinter import *


# Load up instructions function

# global guideImage
root = Tk()
# root.title('User Guide')
# guideImage = ImageTk.PhotoImage(Image.open("images/"))
# guideLabel = Label(root, image=guideImage).pack()
# # guideImage = PhotoImage(file="Step 1.PNG")

load = ImageTk.Image.open("Step 1.PNG")
load = load.resize((4, 3))
render = ImageTk.PhotoImage(load)
img = Label(image=render)
img.image = render
img.place(x=0, y=0)

load = ImageTk.Image.open("Step 2.PNG")
render = ImageTk.PhotoImage(load)
img = Label(image=render)
img.image = render
img.place(x=0, y=1)

root.mainloop()


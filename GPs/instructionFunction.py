from PIL import ImageTk
from tkinter import *
from tkinter import ttk

    # Load up instructions function
def instructionFunction():
    # global guideImage
    top = Toplevel()
    top.title('Prescription process')
    top.geometry("1920x950")

    # create Main frame

    main_frame = Frame(top)
    main_frame.pack(fill= BOTH, expand = 1)

    # Create a Canvas in the Main frame

    canvas = Canvas(main_frame)
    canvas.pack(side = LEFT, fill= BOTH, expand = 1)

    # Create style for scrollbar

    scrollstyle = ttk.Style()
    scrollstyle.theme_use('clam')
    #print(scrollstyle.element_options("scrollstyle.Vertical.TScrollbar.trough"))
    scrollstyle.configure("scrollstyle.Vertical.TScrollbar",arrowsize=30)

    # Add a scrollbar

    scrollbar = ttk.Scrollbar(main_frame,orient = VERTICAL,command = canvas.yview, style="scrollstyle.Vertical.TScrollbar")
    scrollbar.pack(side = RIGHT, fill = Y)

    # Configure the Canvas

    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    # create another frame inside the canvas

    second_frame = Frame(canvas)

    #add second frame to a window in the cavas

    canvas.create_window((0,0),window = second_frame, anchor = "nw")

    #-------------------------------------Step 1----------------------------------------------------#

    image1 = ImageTk.Image.open("GPs/Step 1.PNG")
    image1 = image1.resize((250,300))
    render = ImageTk.PhotoImage(image1)
    img = Label(second_frame,image=render)
    img.image = render
    img.grid(row=1,column=1)
    step1 = Label(second_frame,text="Step 1: Add your search terms and filters and then click the 'Search Medicine' button.")
    step1.grid(row=1,column=2)

    #-------------------------------------Step 2----------------------------------------------------#

    image2 = ImageTk.Image.open("GPs/Step 2.PNG")
    image2 = image2.resize((800,300))
    render = ImageTk.PhotoImage(image2)
    img = Label(second_frame,image=render)
    img.image = render
    img.grid(row=2,column=1)
    labeltext = """
    Step 2: Select a search result and then press the 'Choose Medicine' button.
    If no search results are generated you might have to return to step 1 and adjust search terms.
    """
    step2 = Label(second_frame,text=labeltext)
    step2.grid(row=2,column=2)

    #-------------------------------------Step 3----------------------------------------------------#
    image3 = ImageTk.Image.open("GPs/Step 3.PNG")
    image3 = image3.resize((800,300))
    render = ImageTk.PhotoImage(image3)
    img = Label(second_frame,image=render)
    img.image = render
    img.grid(row=3,column=1)
    labeltext = """
    "Step 3: In the 'Chosen Medicine box' set your dosage, its multiplier and any further information."
    Press the 'Add Medicine' button to add the medicine into the final prescription section below.
    """
    step2 = Label(second_frame,text=labeltext)
    step2.grid(row=3,column=2)

    #-------------------------------------Step 4----------------------------------------------------#

    image4 = ImageTk.Image.open("GPs/Step 4.PNG")
    image4 = image4.resize((800,300))
    render = ImageTk.PhotoImage(image4)
    img = Label(second_frame,image=render)
    img.image = render
    img.grid(row=4,column=1)
    labeltext = """
    "Step 4: Build your prescription by continuously adding medicines."
    You can remove all medicines/a selected medicines given the buttons below.
    """
    step2 = Label(second_frame,text=labeltext)
    step2.grid(row=4,column=2)

    #-------------------------------------Step 5----------------------------------------------------#

    image5 = ImageTk.Image.open("GPs/Step 5.PNG")
    image5 = image5.resize((850,300))
    render = ImageTk.PhotoImage(image5)
    img = Label(second_frame,image=render)
    img.image = render
    img.grid(row=5,column=1)
    labeltext = """
    "Step 5: When you are ready press the 'Save Prescription' button.
    When the dialog box pops up asking you to confirm your exit, please press 'OK'.
    """
    step2 = Label(second_frame,text=labeltext)
    step2.grid(row=5,column=2)




## UCH

<!-- ![](images/UCH.gif) -->

**Step-by-Step on how to run the application**
This is a CLI (command line interface) application, and it can be run by cloning the source code to your local computer. Some aspects of this application have a graphical user interface.

The following libraries were used in this project and will have to be installed in order to run the code.
1.Pandas
2.Pillow
If an error is thrown, asking for installation of these libraries, run the following command in terminal - "pip install <name of library here>" 
To run the program, type 'python .\root.py'
The sqlite3 database file, UCH.db, should be created automatically the first time the program is run. If it isn't, run database.py in the terminal.
The GUI windows in this program are designed for 1080p resolution and 100% text scaling. Please check your display settings in case the windows are not displaying fully. 

**Login details**
Admins:
    email - jacob.lapkin@ucl.ac.uk
    p/w   - 1234

GPs:
    email - andrew.oconnell@ucl.ac.uk
    p/w   - 1234
    email - caroline.crandell@ucl.ac.uk
    p/w   - 1234
    email - chenuka.ratwatte@ucl.ac.uk
    p/w   - 1234

Patients:
    email - m.shorvon@gmail.com
    p/w   - 1234
    email - a.bourke@gmail.com
    p/w   - 1234

**What does this application do and why?**

* This e-Health patient management system makes appointment bookings easy for patients and GPs of University College Hospital (UCH).
* Admins can add new GPs, deactivate/delete their profiles, confirm patients' registration, and manage patient records.
* GPs can login, add availability, confirm patient appointments, and input prescriptions.
* Patients can register their details, login, and book/cancel appointments.

**How the application is organized**

UCH is organized into the following files: 

<!-- ![root folder](images/rootFolder.png) -->

* *README* - this file contains all information about this e-Health patient management system.

* *images folder* - stores all of the images for this README file.

**Technologies Used** 

* Python

**Libraries Used**

* TKinter: Lundh, F., 1999. An introduction to tkinter. URL: www.pythonware.com/library/tkinter/introduction/index.htm.
* Sqlite3: Hipp, R.D., 2020. SQLite, Available at: https://www.sqlite.org/index.html.
* Pillow: Clark, A., 2015. Pillow (PIL Fork) Documentation, readthedocs. Available at: https://buildmedia.readthedocs.org/media/pdf/pillow/latest/pillow.pdf.
* Pandas: McKinney, W. & others, 2010. Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference. pp. 51–56.


**Developers**

Arianna Bourke - AriannaBourke

Caroline Crandell - cecrandell - patient_main.py, patient.py

Jacob Lapkin - Post-Shalom

Andrew O'Connell - chengoconnell

Wei Quan - erinuclkwon

Chenuka Ratwatte - ucabcnd

Matthew Shorvon - mattShorvon

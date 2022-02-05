# UCH
An e-Health patient management system that simplifies appointment bookings for patients and GPs of University College Hospital (UCH).

## Getting Started
This is a CLI (command line interface) application, and it can be run by cloning the source code to your local computer. Some aspects of this application have a graphical user interface.

The following libraries were used in this project and will have to be installed in order to run the code.
1.Pandas
2.Pillow
If an error is thrown, asking for installation of these libraries, run the following command in terminal - "pip install <name of library here>" 
To run the program, type 'python .\root.py'. You can then login with any of the accounts already created (details given below). 
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

## Application features
* Admins can add new GPs, deactivate/reactivate/delete their profiles, confirm/unconfirm patients' registrations, manage patient records and check in/check out patients to and from their appointments. 
* GPs can login, add unavailability in the form of holiday and non-patient time, confirm patients' appointments, view their timetable, cancel appointments, and during the appointment can input appointment notes, prescriptions and download the patient summary.
* Patients can register their details, login, book/cancel appointments, view their appointments, input their vaccination, cancer and pre-existing conditions histories for themselves or their children/family, input any medecine allergies for themselves or their children, view and change their personal details and take a lifestyle risk questionanaire to provide information about aspects of their lifestyle that affect their health such as their exercise routines and diet.

## Built With
* Python

**Libraries Used**

* TKinter: Lundh, F., 1999. An introduction to tkinter. URL: www.pythonware.com/library/tkinter/introduction/index.htm.
* Sqlite3: Hipp, R.D., 2020. SQLite, Available at: https://www.sqlite.org/index.html.
* Pillow: Clark, A., 2015. Pillow (PIL Fork) Documentation, readthedocs. Available at: https://buildmedia.readthedocs.org/media/pdf/pillow/latest/pillow.pdf.
* Pandas: McKinney, W. & others, 2010. Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference. pp. 51–56.


**Developers**

Arianna Bourke - AriannaBourke

Caroline Crandell - cecrandell 

Jacob Lapkin - Post-Shalom

Andrew O'Connell - chengoconnell

Wei Quan - erinuclkwon

Chenuka Ratwatte - ucabcnd

Matthew Shorvon - mattShorvon

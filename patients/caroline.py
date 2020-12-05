# First draft

class Patient:

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.appointments = {}
        self.prescriptions = {}

    def patientSummary(self):
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Email: " + self.email)
        print("Password: " + self.password)
        print("Appointments: " + str(self.appointments))
        print("Prescriptions: " + str(self.prescriptions))

    def bookAppointment(self, date, time, GP):
        self.appointments[GP] = date + " at " + time

    def cancelAppointment(self, date):
        if date in self.appointments:
            print(self.appointments[date])
    
    def viewAppointments(self):
        print(self.appointments)
    
    def requestPrescription(self, medication):
        self.appointments.push([medication])

    def deletePrescription(self, medication):
        if medication in self.prescriptions:
            print(self.prescriptions[medication])

    def viewPrescriptions(self):
        print(self.prescriptions)
    
caroline = Patient("Caroline", "Crandell", "caro@line.com", "password")
caroline.patientSummary()
caroline.bookAppointment("11/20", "13:00", "Dr Shepherd")
caroline.patientSummary()
caroline.bookAppointment("11/21", "11:00", "Dr Grey")
caroline.patientSummary()
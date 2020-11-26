from getpass import getpass

class Patient:

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.loggedIn = 0
        self.update()

    def update(self):
        # c.execute("INSERT INTO patient VALUES (null,?,?,?,?,?)", (self.firstName, self.lastName, self.email, self.password, self.loggedIn))
        pass
    
    def login(self):
        email = input("Please enter your email. ")
        password = getpass("Please enter your password. ")
        self.loginCheck(email, password)

    def registrationSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        print("Welcome, " + self.firstName +
              "! Thank you for registering with UCH.")
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Email: " + self.email)
        print("Password: " + hash)

    def loginCheck(self, email, password):
        if self.email == email and self.password == password:
            self.loggedIn = True
            print("Hello, " + self.firstName + ", welcome back!")
            self.options()
        else:
            print("I'm sorry, those details are not correct, please try again. ")
            self.login()

    def options(self):
        if self.loggedIn == True:
            action = input(
                "What would you like to do next? Enter 1 for book an appointment, 2 for cancel an appointment, or 3 for check your prescriptions.")
        else:
            print("Please login.")
            self.login()

    def patientSummary(self):
        hash = ""
        for i in self.password:
            hash += "*"
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Email: " + self.email)
        print("Password: " + hash)
        print("Questionnaire: " + str(self.questionnaire))
        print("Appointments: " + str(self.appointments))
        print("Prescriptions: " + str(self.prescriptions))

def task():
    action = input("Would you like to register for a new account or login? ")
    action = action.lower()
    if action == "register":
        firstName = input("Please enter your first name. ")
        lastName = input("Please enter your last name. ")
        email = input("Please enter your email. ")
        password = getpass("Please enter your password. ")
        x = Patient(firstName, lastName, email, password)
        x.registrationSummary()
    elif action == "login":
        email = input("Please enter your email. ")
        password = getpass("Please enter your password. ")
    else:
        print("I'm sorry, that is an invalid option. Please type 'Register' or 'Login'. ")
        task()

task()

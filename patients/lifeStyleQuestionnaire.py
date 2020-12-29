import sqlite3 as sql
import webbrowser
import patients.patient_medical_functions as pf


"""Patient can enter data about their lifestyles. Relevant NHS advise and support information are provided to them"""
class RiskProfile:
    def __init__(self, nhsNumber):
        self.connection = sql.connect('UCH.db')
        self.a = self.connection.cursor()
        self.questionnaire = [
            "c_exercise",
            "c_type",
            "c_frequency",
            "c_time",
            "d_goals"
        ]
        self.BMIRelatedData = []
        self.answers = []

    def questions(self, nhs_number):
        print('*'*20, '\nEXERCISE\n\nPlease enter 0 to exit exercises related questions.'
                      '\nENTERING 0 IN ANY OF THE QUESTIONS WILL RESULT IN NONE OF THE ANSWERS PROVIDED BEING SAVED IN THE END!')
        while True:
            try:
                c_exercise = input("Are you currently involved in regular endurance (cardiovascular) exercise? "
                                   "Y for yes, N for no: ").lower()
                if c_exercise == "0":
                    return 0
                if not c_exercise:
                    raise pf.EmptyFieldError()
                if c_exercise != "n" and c_exercise != "y":
                    raise pf.InvalidAnswerError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            except pf.InvalidAnswerError:
                print("\n    < Please enter Y for yes and N for no >\n")
            else:
                break
        if c_exercise == "y":
            c_exercise = 1
        else:
            c_exercise = 0
        self.questionnaire[0] = str(c_exercise)
        if c_exercise == 1:
            while True:
                try:
                    c_type = input("Please name one example of the regular endurance (cardiovascular) "
                                   "exercise you participate in: ")
                    if c_type == "0":
                        return 1
                    if c_type == '':
                        raise pf.EmptyFieldError()
                except pf.EmptyFieldError:
                    error = pf.EmptyFieldError()
                    print(error)
                else:
                    break
            c_type = c_type.title()
            self.questionnaire[1] = c_type
            while True:
                try:
                    c_frequency = int(input("How many times do you engage in " + c_type + " per week" + ": "))
                    if c_frequency == 0:
                        return 1
                    if c_frequency == '':
                        raise pf.EmptyFieldError()
                except pf.EmptyFieldError:
                    error = pf.EmptyFieldError()
                    print(error)
                except ValueError:
                    print("\n    < You have entered a non-numeric value >\n")
                else:
                    break
            self.questionnaire[2] = str(c_frequency)
            while True:
                try:
                    c_time = int(input("In minutes, how much time per week do you commit to " + c_type + ": "))
                    if c_time == 0:
                        return 1
                    if not c_time:
                        raise pf.EmptyFieldError()
                    if c_time >= 10080:
                        raise pf.InvalidAnswerError()
                except pf.EmptyFieldError:
                    error = pf.EmptyFieldError()
                    print(error)
                except pf.InvalidAnswerError:
                    print("\n    < Please enter a realistic answer for this questions >\n")
                except ValueError:
                    print("\n    < You have entered a non-numeric value >\n")
                else:
                    break
            self.questionnaire[3] = str(c_time)
            if c_time < 150:
                print("The nhs recommends at least 150 minutes of moderate intensity activity a week.")
        else:
            print("Regular exercises are the key to stay healthy.")
        print('*'*20, '\nGOALS\nPlease enter 0 to exit goal related questions.')
        while True:
            try:
                d_goals = input("What are your main health goals: ")
                if d_goals == "0":
                    return 1
                if d_goals == '':
                    raise pf.EmptyFieldError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            else:
                break
        d_goals = d_goals.title()
        self.questionnaire[4] = d_goals

    def BMI_calculator(self, nhs_number):
        print('*'*20, '\nBMI CALCULATOR\nPlease enter 0 to exit BMI related questions.')
        while True:
            try:
                height = float(input("What is your height in metres: "))
                if height == 0:
                    return 1
                weight = float(input("What is your weight in kg: "))
                if weight == 0:
                    return 1
                if not height or not weight:
                    raise pf.EmptyFieldError()
                if height >= 3 or weight >= 400:
                    raise pf.InvalidAnswerError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            except pf.InvalidAnswerError:
                print("\n    < Error! The entered height and weight seem to be unrealistic >\n")
            except ValueError:
                print('\n    < Error! Please enter numeric values for height and weight >\n')
            else:
                break
        bmi_calculation = round(weight/(height ** 2), 2)
        bmi = bmi_calculation
        self.BMIRelatedData.append(height)
        self.BMIRelatedData.append(weight)
        self.BMIRelatedData.append(bmi)
        self.answers.extend(self.questionnaire)
        self.answers.extend(self.BMIRelatedData)
        if bmi < 18.4:
            print("*" * 20)
            print("Your BMI of {} suggests you are underweight.".format(bmi))
            print("Being underweight could be a sign you're not eating enough or you may be ill."
                  "\nPlease talk to your doctor. You can also find advice on the following NHS webpage: ")
            if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/advice-for-underweight-adults/", new=2)

        if 18.5 < bmi < 24.9:
            print("*" * 20)
            print("Your BMI of {} is within a healthy range.".format(bmi))

        if 25 < bmi < 30:
            print("*" * 20)
            print("Your BMI of {} suggests you are overweight.".format(bmi))
            print("Losing and keeping off 5% of your weight can have health benefits, "
                  "\nsuch as lowering your blood pressure and reducing your risk of developing type 2 diabetes."
                  "\nYou should work towards achieving a healthier weight over time. "
                  "\nWe suggest you visit your GP to discuss. You can also find advice on the following NHS webpage: ")
            if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/start-the-nhs-weight-loss-plan"
                                "/?tabname=weight-loss-support", new=2)

        if bmi > 30:
            print("*" * 20)
            print("Your BMI of {} suggests you are obese.".format(bmi))
            print("Losing and keeping off 5% of your weight can have health benefits, "
                  "\nsuch as lowering your blood pressure and reducing your risk of developing type 2 diabetes."
                  "\nYou should work towards achieving a healthier weight over time. "
                  "\nWe suggest you visit your GP to discuss. You can also find advice on the following NHS webpage: ")
            if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/start-the-nhs-weight-loss-plan"
                                "/?tabname=weight-loss-support", new=2)

    def smoking(self, nhs_number):
        print('*'*20, '\nSMOKING\nPlease enter 0 to exit smoking related questions.')
        while True:
            try:
                smoking = input("Y for yes, N for no. Do you smoke cigarettes regularly: ").lower()
                if smoking == "0":
                    return 1
                if not smoking:
                    raise pf.EmptyFieldError()
                if smoking != "n" and smoking != "y":
                    raise pf.InvalidAnswerError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            except pf.InvalidAnswerError:
                print("\n    < Error! Please re-answer the questions with Y for yes and N for no >\n")
            else:
                break
        if smoking == "y":
            smoking = 1
        else:
            smoking = 0
        self.answers.append(smoking)
        if smoking == 1:
            print("*" * 20)
            print("Stopping smoking is one of the best things you'll ever do for your health."
                  "\nWhen you stop, you give your lungs the chance to repair and you'll"
                  "\nbe able to breathe easier. There are lots of other benefits too and "
                  "\nthey start almost immediately!")
            print("If you would like more advice and support, "
                  "\nplease consult your doctor and look at the following NHS webpage: ")
            if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/better-health/quit-smoking/", new=2)

    def drugs(self, nhs_number):
        print('*'*20, '\nDRUGS\nPlease enter 0 to exit drug related questions.')
        while True:
            try:
                drugs = input("Y for yes, N for no. Do you consume recreational drugs: ").lower()
                if drugs == "0":
                    return 1
                if not drugs:
                    raise pf.EmptyFieldError()
                if drugs != "n" and drugs != "y":
                    raise pf.InvalidAnswerError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            except pf.InvalidAnswerError:
                print("\n    < Error! Please enter Y for yes and N for no >\n")
            else:
                break
        if drugs == "y":
            drugs = 1
        else:
            drugs = 0
        if drugs == 1:
            while True:
                try:
                    drugs_type = input("Please name one type of drugs you regularly "
                                       "consume or enter N/A if prefer not to disclose: ").lower()
                    if drugs_type == "":
                        raise pf.EmptyFieldError()
                except pf.EmptyFieldError:
                    error = pf.EmptyFieldError()
                    print(error)
                else:
                    break
            self.answers.append(drugs)
            self.answers.append(drugs_type)
        else:
            drugs_type = 0
            self.answers.append(drugs)
            self.answers.append(drugs_type)

    def alcohol(self, nhs_number):
        print('*'*20, '\nALCOHOL\nPlease enter 0 to exit alcohol related questions.')
        print("1 unit of alcohol is around 76ml(~1/2 a glass) of wine or 250ml of beer (~1/2 a pint).")
        while True:
            try:
                alcohol = input("Y for yes, N for no. Do you drink alcohol in general: ").lower()
                if alcohol == "0":
                    return 1
                if not alcohol:
                    raise pf.EmptyFieldError()
                if alcohol != "n" and alcohol != "y":
                    raise pf.InvalidAnswerError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            except pf.InvalidAnswerError:
                print("\n    < Error! Please enter Y for yes and N for no >\n")
            else:
                break
        if alcohol == "y":
            alcohol = 1
        else:
            alcohol = 0
        if alcohol == 1:
            print("On average, how many units of alcohol do you drink a week?")
            print("Choose [1]: 1-2"
                    "\nChoose [2]: 3-4"
                    "\nChoose [3]: 5-6"
                    "\nChoose [4]: 7-8"
                    "\nChoose [5]: 9-10"
                    "\nChoose [6]: 11-12"
                    "\nChoose [7]: 13-14"
                    "\nChoose [8]: 14+")
            unit = [1, 2, 3, 4, 5, 6, 7, 8]
            while True:
                try:
                    alcohol_unit = int(input("Please choose a number from the options above: "))
                    if alcohol_unit == "0":
                        return 1
                    if alcohol_unit == '':
                        raise pf.EmptyFieldError()
                    if alcohol_unit not in unit:
                        raise pf.InvalidAnswerError()
                except pf.EmptyFieldError:
                    error = pf.EmptyFieldError()
                    print(error)
                except pf.InvalidAnswerError:
                    print("\n    < Invalid answer. Please enter your answer based on the menu provided >\n")
                except ValueError:
                    print('\n    < Error! Please enter a numeric value from the menu above >\n')
                else:
                    break
            self.answers.append(alcohol)
            self.answers.append(str(alcohol_unit))
            if alcohol_unit == 8:
                print("*" * 20)
                print("Men and women are advised not to drink more than 14 units"
                      "\na week on a regular basis. Spread your drinking over 3 "
                      "\nor more days if you regularly drink as much as 14 units a week."
                      "\nIf you want to cut down, try to have several drink-free days each week")
                print("If you would like more advice and support, "
                      "\nplease consult your doctor and look at the following NHS webpage: ")
                if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
                    webbrowser.open("https://www.nhs.uk/live-well/alcohol-support/tips-on-cutting-down-alcohol/", new=2)
        else:
            alcohol_unit = 0
            self.answers.append(alcohol)
            self.answers.append(alcohol_unit)

    def diet(self, nhs_number):
        print('*'*20, '\nDIET\nPlease enter 0 to exit diet related questions.')
        while True:
            try:
                meat = int(input("How many meals a week do you consume red meat: "))
                if meat == '':
                    raise pf.EmptyFieldError()
                diet = int(input("How many portions of fruit or vegetables do you consume a day: "))
                # if diet == "0":
                #     return 1
                if diet == '':
                    raise pf.EmptyFieldError()
            except pf.EmptyFieldError:
                error = pf.EmptyFieldError()
                print(error)
            except ValueError:
                print('\n    < Error! Please enter a numeric value >\n')
            else:
                break
        if diet < 5:
            print("The NHS suggests that men and women should consume at least 5 "
                  "portions of fruit or vegetables a day as part of a healthy diet.")
        print("If you would like more advice and support, "
              "\nplease consult your doctor and look at the following NHS webpage: ")
        if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
            webbrowser.open("https://www.nhs.uk/live-well/eat-well/meat-nutrition/", new=2)
        while True:
            try:
                caffeine = int(input("How many cups of coffee or caffeinated drinks do you consume per day: "))
                # if caffeine == "0":
                #     return 1
            except ValueError:
                print('\n    < Error! Please enter a numeric value >\n')
            else:
                break
        if caffeine > 4:
            print("According to the NHS guidelines, drinking up to four cups of coffee a day carries no health risk.",
                  "\nYou might want to cut down your daily caffeine intake.")
            print("If you would like more advice and support, "
                  "\nplease consult your doctor and look at the following NHS webpage: ")
            if input("Type Y for yes to open in browser (type anything else means no): ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/news/genetics-and-stem-cells/four-cups-of-coffee-not-bad-for-health-suggests-review", new=2)
        self.answers.append(str(meat))
        self.answers.append(str(diet))
        self.answers.append(str(caffeine))

    def insert_to_table(self, nhs_number):
        self.answers.insert(0, nhs_number)
        try:
            question_query = """INSERT INTO questionnaireTable (nhsNumber, exercise, exerciseType, exerciseFrequency,
            exerciseDuration, goal, height, weight, bmi, smoking, drugs, drugType, alcohol, 
            alcoholUnit, meat, diet, caffeine)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            self.a.execute(question_query, self.answers)
        except Exception:
            print('No answers saved. Please remember to come back to finish the questions next time')
            return 1
        else:
            self.connection.commit()
            self.connection.close()
        # self.a.execute("SELECT * FROM questionnaireTable")
        # result = self.a.fetchall()
        # print(result)

# Erin = RiskProfile()
# Erin.questions("0123456789")
# Erin.BMI_calculator("0123456789")
# Erin.alcohol("0123456789")
# Erin.drugs("0123456789")
# Erin.diet("0123456789")
# Erin.smoking("0123456789")
# Erin.save_your_answers()
# correct order: smoking, drugs, alcohol, diet
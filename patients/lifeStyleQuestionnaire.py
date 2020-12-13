import sqlite3 as sql
import webbrowser


class InvalidMenuSelectionError(Exception):
    pass
class InvalidAnswerError(Exception):
    pass
class RiskProfile:
    def __init__(self):
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

    def questions(self):
        print("EXERCISE")
        try:
            c_exercise = input("Are you currently involved in regular endurance (cardiovascular) exercise? "
                               "Y for yes, N for no\n")
            if c_exercise != "N" and c_exercise != "Y" and c_exercise != "n" and c_exercise != "y":
                raise InvalidAnswerError()
        except InvalidAnswerError:
            print("Please enter Y for yes and N for no.")
            c_exercise = input("Are you currently involved in regular endurance (cardiovascular) exercise? "
                               "Y for yes, N for no\n")
        c_exercise = c_exercise.lower()
        self.questionnaire[0] = c_exercise
        if "y" in c_exercise:
            c_type = input("Please name one example of the regular endurance (cardiovascular) "
                           "exercise you participate in?\n")
            c_type = c_type.lower()
            self.questionnaire[1] = c_type
            try:
                c_frequency = int(input("How many times do you engage in " + c_type + " per week" + "?\n"))
            except ValueError:
                print("You have entered a non-numeric value.")
                c_frequency = int(input("How many times do you engage in " + c_type + " per week" + "?\n"))
            self.questionnaire[2] = str(c_frequency)
            try:
                c_time = int(input("In minutes, how much time per week do you commit to " + c_type + "?\n"))
                if c_time >= 10080:
                    raise InvalidAnswerError()
            except ValueError:
                print("You have entered a non-numeric value.")
                c_time = int(input("In minutes, how much time per week do you commit to " + c_type + "?\n"))
            except InvalidAnswerError:
                print("Please enter a realistic answer for this questions.")
                c_time = int(input("In minutes, how much time per week do you commit to " + c_type + "?\n"))
            self.questionnaire[3] = str(c_time)
            if c_time < 150:
                print("The nhs recommends at least 150 minutes of moderate intensity activity a week")
        else:
            print("Regular exercises are the key to stay healthy.")
        print("GOALS\n", "*"*20)
        d_goals = input("What are your main health goals?\n")
        d_goals = d_goals.lower()
        self.questionnaire[4] = d_goals

    def BMI_calculator(self):
        try:
            height = float(input("What is your height in metres? "))
            weight = float(input("What is your weight in kg? "))
            if height >= 3 or weight >= 400:
                raise InvalidAnswerError()
        except InvalidAnswerError:
            print("Error! The entered height and weight seem to be too large.")
            height = float(input("What is your height in metres? "))
            weight = float(input("What is your weight in kg? "))
        bmi_calculation = round(weight/(height ** 2), 2)
        bmi = bmi_calculation
        self.BMIRelatedData.append(height)
        self.BMIRelatedData.append(weight)
        self.BMIRelatedData.append(bmi)
        self.answers.extend(self.questionnaire)
        self.answers.extend(self.BMIRelatedData)
        if bmi < 18.4:
            print("*" * 20)
            print("Your BMI of {} suggests you are underweight".format(bmi))
            print("Being underweight could be a sign you're not eating enough or you may be ill."
                  "\nPlease talk to your doctor. You can also find advice on the following NHS webpage: ")
            if input("Type Y for yes to open in browser: ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/advice-for-underweight-adults/", new=2)

        if 18.5 < bmi < 24.9:
            print("*" * 20)
            print("Your BMI of {} is within a healthy range".format(bmi))

        if 25 < bmi < 30:
            print("*" * 20)
            print("Your BMI of {} suggests you are overweight".format(bmi))
            print("Losing and keeping off 5% of your weight can have health benefits, "
                  "\nsuch as lowering your blood pressure and reducing your risk of developing type 2 diabetes."
                  "\nYou should work towards achieving a healthier weight over time. "
                  "\nWe suggest you visit your GP to discuss. You can also find advice on the following NHS webpage: ")
            if input("Type Y for yes to open in browser: ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/start-the-nhs-weight-loss-plan"
                                "/?tabname=weight-loss-support", new=2)

        if bmi > 30:
            print("*" * 20)
            print("Your BMI of {} suggests you are obese".format(bmi))
            print("Losing and keeping off 5% of your weight can have health benefits, "
                  "\nsuch as lowering your blood pressure and reducing your risk of developing type 2 diabetes."
                  "\nYou should work towards achieving a healthier weight over time. "
                  "\nWe suggest you visit your GP to discuss. You can also find advice on the following NHS webpage: ")
            if input("Type Y for yes to open in browser: ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/start-the-nhs-weight-loss-plan"
                                "/?tabname=weight-loss-support", new=2)

    def smoking(self):
        print("*" * 20)
        print("This section of the survey will assess smoking: ")
        try:
            smoking = input("Y for yes, N for no. Do you smoke cigarettes regularly?: ").lower()
            if smoking != "N" and smoking != "Y" and smoking != "n" and smoking != "y":
                raise InvalidAnswerError()
        except InvalidAnswerError:
            print("Error! Please re-answer the questions with Y for yes and N for no")
            smoking = input("Y for yes, N for no. Do you smoke cigarettes regularly?: ").lower()
        self.answers.append(smoking)
        if smoking == "y":
            print("*" * 20)
            print("Stopping smoking is one of the best things you'll ever do for your health."
                  "\nWhen you stop, you give your lungs the chance to repair and you'll"
                  "\nbe able to breathe easier. There are lots of other benefits too and "
                  "\nthey start almost immediately!")
            print("If you would like more advice and support, "
                  "\nplease consult your doctor and look at the following NHS webpage: ")
            if input("Type Y for yes to open in browser: ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/better-health/quit-smoking/", new=2)

    def drugs(self):
        print("*" * 20)
        try:
            drugs = input("Y for yes, N for no. Do you consume recreational drugs? yes or no: ").lower()
            if drugs != "N" and drugs != "Y" and drugs != "n" and drugs != "y":
                raise InvalidAnswerError()
        except InvalidAnswerError:
            print("Error! Please enter Y for yes and N for no.")
            drugs = input("Y for yes, N for no. Do you consume recreational drugs? yes or no: ").lower()
        if drugs == "y":
            drugs_type = input("Please name one type of drugs you regularly consume. ")
            self.answers.append(drugs)
            self.answers.append(drugs_type)
        else:
            drugs_type = ""
            self.answers.append(drugs)
            self.answers.append(drugs_type)

    def alcohol(self):
        print("*" * 20)
        print("The following part of the survey will assess your consumption of alcohol: ")
        print("1 unit of alcohol is around 76ml(~1/2 a glass) of wine or 250ml of beer (~1/2 a pint)")
        try:
            alcohol = (input("Y for yes, N for no. Do you drink alcohol in general? ")).lower()
            if alcohol != "N" and alcohol != "Y" and alcohol != "n" and alcohol != "y":
                raise InvalidAnswerError()
        except InvalidAnswerError:
            print("Error! Please enter Y for yes and N for no.")
            alcohol = (input("Y for yes, N for no. Do you drink alcohol in general? ")).lower()
        if alcohol == "y":
            print("On average, how many units of alcohol do you drink a week?")
            print("1. 1-2"
                    "\n2. 3-4"
                    "\n3. 5-6"
                    "\n4. 7-8"
                    "\n5. 9-10"
                    "\n6. 11-12"
                    "\n7. 13-14"
                    "\n8. 14+")
            unit = [1, 2, 3, 4, 5, 6, 7, 8]
            try:
                alcohol_unit = int(input("Please choose a number from the options above: "))
                if alcohol_unit not in unit:
                    raise InvalidAnswerError()
            except InvalidAnswerError:
                print("Please enter your answer based on the menu provided.")
                alcohol_unit = int(input("Please choose a number from the options above: "))
            self.answers.append(alcohol)
            self.answers.append(alcohol_unit)
            if alcohol_unit == 8:
                print("*" * 20)
                print("Men and women are advised not to drink more than 14 units"
                      "\na week on a regular basis. Spread your drinking over 3 "
                      "\nor more days if you regularly drink as much as 14 units a week."
                      "\nIf you want to cut down, try to have several drink-free days each week")
                print("If you would like more advice and support, "
                      "\nplease consult your doctor and look at the following NHS webpage: ")
                if input("Type Y for yes to open in browser: ").lower() == "y":
                    webbrowser.open("https://www.nhs.uk/live-well/alcohol-support/tips-on-cutting-down-alcohol/", new=2)
        else:
            alcohol_unit = ""
            self.answers.append(alcohol)
            self.answers.append(alcohol_unit)

    def diet(self):
        print("*" * 20)
        print("The following part of the survey will assess your diet: ")
        meat = input("How many meals a week do you consume red meat? ")
        diet = input("How many portions of fruit or vegetables do you consume a day? ")
        if int(diet) < 5:
            print("The NHS suggests that men and women should consume at least 5 "
                  "portions of fruit or vegetables a day as part of a healthy diet.")
        print("If you would like more advice and support, "
              "\nplease consult your doctor and look at the following NHS webpage: ")
        if input("Type Y for yes to open in browser: ").lower() == "y":
            webbrowser.open("https://www.nhs.uk/live-well/eat-well/meat-nutrition/", new=2)
        caffeine = input("How many cups of coffee or caffeinated drinks do you consume per day? ")
        if int(caffeine) > 4:
            print("According to the NHS guidelines, drinking up to four cups of coffee a day carries no health risk",
                  "\nYou might want to cut down your daily caffeine intake a bit.")
            print("If you would like more advice and support, "
                  "\nplease consult your doctor and look at the following NHS webpage: ")
            if input("Type Y for yes to open in browser: ").lower() == "y":
                webbrowser.open("https://www.nhs.uk/news/genetics-and-stem-cells/four-cups-of-coffee-not-bad-for-health-suggests-review", new=2)
        self.answers.append(meat)
        self.answers.append(diet)
        self.answers.append(caffeine)

    def insert_to_table(self, patient_email):
        self.answers.insert(0, patient_email)
        question_query = """INSERT INTO questionnaireTable (patientEmail, exercise, exerciseType, exerciseFrequency,
        exerciseDuration, goal, height, weight, bmi, smoking, drugs, drugType, alcohol, 
        alcoholUnit, meat, diet, caffeine)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.a.execute(question_query, self.answers)
        self.connection.commit()
        self.connection.close()
        # self.a.execute("SELECT * FROM questionnaireTable")
        # result = self.a.fetchall()
        # print(result)

Erin = RiskProfile()
# Erin.BMI_calculator()
Erin.alcohol()
Erin.drugs()
Erin.diet()
Erin.smoking()
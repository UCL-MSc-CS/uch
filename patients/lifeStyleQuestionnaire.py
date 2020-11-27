import sqlite3 as sql
import webbrowser


class RiskProfile:
    def __init__(self, answers):
        self.connection = sql.connect('questionnaireTable.db')
        self.a = self.connection.cursor()
        self.questionnaire = [
            "c_exercise",
            "c_type",
            "c_frequency",
            "c_time",
            "d_goals"
        ]
        self.answers = []

    def questions(self, answers):
        print("EXERCISE")
        c_exercise = input("Are you currently involved in regular endurance (cardiovascular) exercise? "
                           "Y for yes, N for no\n")
        c_exercise = c_exercise.lower()
        self.answers.append(c_exercise)
        if "y" in c_exercise:
            c_type = input("What type of regular endurance (cardiovascular) exercise do you participate in?\n")
            c_type = c_type.lower()
            self.answers.append(c_type)
            c_frequency = input("How frequently do you engage in " + c_type + "per week" + "?\n")
            c_frequency = c_frequency.lower()
            self.answers.append(c_frequency)
            c_time = input("In minutes, how much time per week do you commit to " + c_type + "?\n")
            c_time = c_time.lower()
            self.answers.append(c_time)
            if c_time < str(150):
                print("The nhs recommends at least 150 minutes of moderate intensity activity a week")
        else:
            print("Regular exercises are the key to stay healthy")
        print("GOALS")
        d_goals = input("What are your main health goals?\n")
        d_goals = d_goals.lower()
        self.answers.append(d_goals)

    def BMI_calculator(self):
        height = float(input("What is your height in metres? "))
        weight = float(input("What is your weight in kg? "))
        BMI = round(weight/(height ** 2), 2)
        self.answers.append(height)
        self.answers.append(weight)
        question_query = """INSERT INTO questionnaireTable (exercise, exerciseType, exerciseFrequency, 
        exerciseDuration, goal, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self.a.execute(question_query, self.answers)
        self.a.execute("SELECT * FROM questionnaireTable")
        result = self.a.fetchall()
        print(result)
        if BMI < 18.4:
            print("*" * 20)
            print("Your BMI of {} suggests you are underweight".format(BMI))
            print("Being underweight could be a sign you're not eating enough or you may be ill."
                  "\nPlease talk to your doctor. You can also find advice on the following NHS webpage: ")
            if input("Type yes to open in browser: ").lower() == "yes":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/advice-for-underweight-adults/", new=2)
                print("*" * 20)
        if 18.5 < BMI < 24.9:
            print("*" * 20)
            print("Your BMI of {} is within a healthy range".format(BMI))
            print("*" * 20)
        if 25 < BMI < 30:
            print("*" * 20)
            print("Your BMI of {} suggests you are overweight".format(BMI))
            print("Losing and keeping off 5% of your weight can have health benefits, "
                  "\nsuch as lowering your blood pressure and reducing your risk of developing type 2 diabetes."
                  "\nYou should work towards achieving a healthier weight over time. "
                  "\nWe suggest you visit your GP to discuss. You can also find advice on the following NHS webpage: ")
            if input("Type yes to open in browser: ").lower() == "yes":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/start-the-nhs-weight-loss-plan"
                                "/?tabname=weight-loss-support", new=2)
                print("*" * 20)
        if BMI > 30:
            print("*" * 20)
            print("Your BMI of {} suggests you are obese".format(BMI))
            print("Losing and keeping off 5% of your weight can have health benefits, "
                  "\nsuch as lowering your blood pressure and reducing your risk of developing type 2 diabetes."
                  "\nYou should work towards achieving a healthier weight over time. "
                  "\nWe suggest you visit your GP to discuss. You can also find advice on the following NHS webpage: ")
            if input("Type yes to open in browser: ").lower() == "yes":
                webbrowser.open("https://www.nhs.uk/live-well/healthy-weight/start-the-nhs-weight-loss-plan"
                                "/?tabname=weight-loss-support", new=2)
                print("*" * 20)

    def smoking(self):
        print("*" * 20)
        print("This section of the survey will assess smoking: ")
        smoking = input("Do you smoke cigarettes regularly?: ").lower()
        if smoking == "yes":
            print("*" * 20)
            print("Stopping smoking is one of the best things you'll ever do for your health."
                  "\nWhen you stop, you give your lungs the chance to repair and you'll"
                  "\nbe able to breathe easier. There are lots of other benefits too and "
                  "\nthey start almost immediately!")
            print("If you would like more advice and support, "
                  "\nplease consult your doctor and look at the following NHS webpage: ")
            if input("Type yes to open in browser: ").lower() == "yes":
                webbrowser.open("https://www.nhs.uk/better-health/quit-smoking/", new=2)

    def drugs(self):
        print("*" * 20)
        drugs = input("Do you consume recreational drugs? yes or no: ").lower()
        drugs_type = input("What type of drugs? ")

    def alcohol(self):
        print("*" * 20)
        print("The following part of the survey will assess your consumption of alcohol: ")
        print("1 unit of alcohol is around 76ml(~1/2 a glass) of wine or 250ml of beer (~1/2 a pint)")
        print("On average, how many units of alcohol do you drink a week?")
        print("1. 0"
                "\n2. 1-2 "
                "\n3. 3-5"
                "\n4. 5-10"
                "\n5. 14+")
        alcohol = int(input("Please choose a number from the options above: "))
        if alcohol == 5:
            print("*" * 20)
            print("Men and women are advised not to drink more than 14 units"
                  "\na week on a regular basis. Spread your drinking over 3 "
                  "\nor more days if you regularly drink as much as 14 units a week."
                  "\nIf you want to cut down, try to have several drink-free days each week")
            print("If you would like more advice and support, "
                  "\nplease consult your doctor and look at the following NHS webpage: ")
            if input("Type yes to open in browser: ").lower() == "yes":
                webbrowser.open("https://www.nhs.uk/live-well/alcohol-support/tips-on-cutting-down-alcohol/", new=2)

    def diet(self):
        # print("*" * 20)
        # print("The following part of the survey will assess your diet: ")
        # meat = input("How many meals a week do you consume red meat? ")
        # diet = input("How many portions of fruit or vegetables do you consume a day? ")
        # caffeine = input("How much caffeine do you consume per day? ")
        pass


print("Please fill out the following risk profile")
arianna = RiskProfile()
arianna.questions()
arianna.BMI_calculator()
# arianna.diet()
# arianna.smoking()
# arianna.drugs()
# arianna.alcohol()

# Bob = RiskProfile()
# Bob.BMI_calculator()

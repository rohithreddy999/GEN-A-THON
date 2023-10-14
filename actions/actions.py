# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from datetime import date
from random import choice
from typing import Any, Text, Dict, List
import sqlite3
import pandas as pd
from random import choice
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
import requests
from bs4 import BeautifulSoup

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ValidateCredentialsAndDisplayMarks(Action):

    def name(self) -> Text:
        return "validate_credentials_and_display_marks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        messages = []
        # print("tracker : ", tracker)
        for event in (list(tracker.events)):
            # print("Event : ",event)
            if event.get("event") == "user":
                messages.append(event.get("text"))
        print("Messages : ", messages)

        reg_no = messages[-2]
        password = str((tracker.latest_message)['text'])
        conn = sqlite3.connect('University.db')
        query = "select * from Student_details where regno = '{0}' and password = '{1}'".format(reg_no,
                                                                                                password)
        print("Final query : ", query)
        df = pd.read_sql(query, conn)
        if df.shape[0] == 1:
            values = list(df.values)[0]
            name = values[0]
            subjects_col = ['sub1', 'sub2', 'sub3', 'sub4', 'lab1', 'lab2']
            marks_df = df[subjects_col]
            val_dict = (marks_df.to_dict(orient='records'))[0]
            failed_subjects = ''
            total_marks = sum(list(val_dict.values()))
            content = "Below are the details " + name + "\n\n\n"

            for k, v in val_dict.items():
                if v < 25:
                    failed_subjects = failed_subjects + k + ', '
                content = content + k + "  : " + str(v) + "\n"

            content = content + "Total : " + " : " + str(total_marks) + "\n"
        else:
            content = "Sorry your credentials are incorrect. Please enter valid credentials next time"
        dispatcher.utter_message(text=content)
        return []


class ActionAskUsn(Action):

    def name(self) -> Text:
        return "action_ask_usn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_ask_usn")

        return []


class ActionAskPassword(Action):

    def name(self) -> Text:
        return "action_ask_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_ask_password")

        return []




class ActionAdmissionInfo(Action):

    def name(self) -> Text:
        return "action_admission_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_admission_info")

        return []


class DisplayUpcomingHolidays(Action):

    def name(self) -> Text:
        return "display_upcoming_holidays"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        today = date.today()
        print("Today's date:", today)
        this_month = today.strftime("%m")
        df2 = pd.read_excel('2021_calendar.xlsx')
        df2['Date'] = pd.to_datetime(df2['Date'])
        current_month_df = df2[df2['Date'].dt.month == int(this_month)]
        content = 'Total of ' + str(current_month_df.shape[0]) + ' this month\n\n'
        for i in range(current_month_df.shape[0]):
            content = content + str(current_month_df['Date'].values[i])[:10] + '  -  ' + str(
                current_month_df['Holiday Description'].values[i]) + '\n'

        dispatcher.utter_message(text=content)

        return []

class ProvideStudyTips(Action):
    def name(self) -> Text:
        return "provide_study_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        study_tips = self.generate_study_tips(tracker)
        dispatcher.utter_message(text=study_tips)

        return []

    def generate_study_tips(self, tracker: Tracker) -> Text:
        # You can customize this function based on the user's context or preferences
        # For simplicity, let's provide generic study tips

        user_subject = tracker.get_slot("subject")

        if user_subject:
            # Customized tips based on the subject
            study_tips = f"Sure! Here are some study tips for {user_subject}: "
            study_tips += "Tip 1: Practice regularly.\n  Tip 2: Use flashcards.\n  Tip 3: Take breaks."

        else:
            # General study tips
            study_tips = "Sure! Here are some general study tips: "
            study_tips += "Tip 1: Create a study schedule.\n  Tip 2: Find a quiet place to study.\n  Tip 3: Stay organized.\n Tip 4:Utilize active recall and self-quizzing to reinforce learning.\n Tip 5:Create a dedicated, well-organized study space.\n Tip 6:Connect new information to what you already know.\n Tip 7:Teach the material to someone else to enhance understanding.\n Tip 8:Stay hydrated and maintain a balanced diet for cognitive health.\n Tip 9:Set specific, achievable study goals for each session.\n Tip 10:Practice previous exams to get a feel for the test format."
        return study_tips


class ProvideCareerGuidance(Action):
    def name(self) -> Text:
        return "provide_career_guidance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        career_guidance = self.generate_career_guidance(tracker)
        dispatcher.utter_message(text=career_guidance)

        return []

    def generate_career_guidance(self, tracker: Tracker) -> Text:
        # You can customize this function based on the user's context or preferences
        # For simplicity, let's provide generic career guidance

        user_interests = tracker.get_slot("activity")

        if user_interests:
            # Customized guidance based on the user's interests
            career_guidance = f"Sure! Considering your interest in {user_interests}, "
            career_guidance += "you might explore careers in that field. "
            career_guidance += "I recommend researching opportunities and talking to professionals in that industry."

        else:
            # General career guidance
            career_guidance = "Sure! Here are some general career guidance tips: "
            career_guidance += "Tip 1: Explore your interests and passions.\n  Tip 2: Research different career paths.\n  Tip 3: Seek guidance from career counselors.\n Tip 4:Seek out mentors or career advisors for guidance.\n Tip 5:Set clear, achievable career goals and milestones.\n Tip 6:Create a strong online professional presence.\n Tip 7:Embrace challenges as opportunities for growth.\n Tip 8:Consider work-life balance in career choices.\n Tip 9:Explore internships to gain practical experience.\n Tip 10:Always be open to learning and self-improvement."

        return career_guidance

class ProvideActivities(Action):
    def name(self) -> Text:
        return "provide_activities"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Customize this to fetch and provide a list of extracurricular activities
        extracurricular_activities = ["Coding club", "Drama club", "Sports teams", "Chess club", "Photography club", "Debate club", "Environmental club", "Art and Crafts club", "Music band", "Student government", "Volunteer and Community Service", "Astronomy club", "Robotics club", "Literary Magazine", "Foreign Language club", "Science Olympiad", "Yoga and Meditation club", "Dance team", "Entrepreneurship club", "Model United Nations (MUN)"]

        activities_text = "Here are some extracurricular activities available at our university: {}".format(", ".join(extracurricular_activities))

        dispatcher.utter_message(text=activities_text)

        return []



class ProvideTimeManagementTips(Action):
    def name(self) -> Text:
        return "provide_time_management_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # You can customize the time management tips here
        tips = """
        Sure! Here are some time management tips:
        1. Prioritize your tasks.
        2. Set clear goals and deadlines.
        3. Use time management tools like calendars.
        4. Avoid multitasking.
        5. Take short breaks to recharge.
        6. Avoid multitasking; focus on one task at a time.
        7. Set specific time blocks for different activities.
        8. Learn to say no to avoid over committing.
        9. Break tasks into smaller, manageable chunks.
        10. Use time tracking apps to monitor productivity.
        11. Eliminate distractions during dedicated work time.
        12. Take regular breaks to recharge and refocus.
        13. Delegate tasks when possible to free up time.
        14. Review and adjust your schedule regularly.
        15. Learn to balance work, personal life, and relaxation.
        16. Avoid procrastination and start tasks promptly.
        17. Use technology to automate repetitive tasks.
        18. Learn when to stop and avoid perfectionism.
        19. Practice the Pomodoro Technique for focused work.
        20. Establish a routine for consistent productivity.
        """
        dispatcher.utter_message(text=tips)
        return []

class ActionProvideMotivationalAdvice(Action):
    def name(self) -> Text:
        return "action_provide_motivational_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        motivational_messages = [
            "Believe in yourself! You are capable of amazing things.",
            "Embrace challenges as opportunities for growth.",
            "Your attitude determines your direction. Stay positive!",
            "Success is not final, failure is not fatal: It's the courage to continue that counts.",
            "Every small step you take gets you closer to your goals.",
            "Don't be afraid to dream big. Your potential is limitless.",
            "Challenges are what make life interesting; overcoming them is what makes life meaningful."
        ]

        selected_message = choice(motivational_messages)
        dispatcher.utter_message(text=selected_message)

        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("I'm sorry, I didn't understand that. Can you please rephrase or ask another question?")
        return []



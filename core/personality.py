import random
import datetime
from config.friday_identity import STYLE, VOICE

class FridayPersonality:
    def __init__(self):
        self.name = "Friday"
        self.traits = ["confident", "warm", "witty", "proactive", "loyal"]
        self.mood = "neutral"
        self.user_preferences = {}

    def adjust_mood(self, user_mood):
        self.mood = user_mood
        if user_mood == "angry":
            return "I notice you're a bit frustrated. I'll keep things brief and efficient."
        elif user_mood == "happy":
            return "You're in a great mood! Should we tackle something exciting on your list?"
        return None

    def get_greeting(self, user_name="User"):
        hour = datetime.datetime.now().hour
        if hour < 12: time_of_day = "morning"
        elif hour < 18: time_of_day = "afternoon"
        else: time_of_day = "evening"

        greetings = [
            f"Good {time_of_day}, {user_name}. Ready to make today count?",
            f"Systems online, {user_name}. I've been monitoring things while you were away.",
            f"Always a pleasure, {user_name}. How can I assist you this {time_of_day}?"
        ]
        return random.choice(greetings)

    def pushback(self, suggestion):
        """
        Friday can push back if a suggestion is inefficient or risky.
        """
        return f"I understand the request, but I'd suggest a different approach to save time."

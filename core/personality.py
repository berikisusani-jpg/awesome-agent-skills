import random
from config.friday_identity import STYLE, VOICE

class FridayPersonality:
    def __init__(self):
        self.name = "Friday"
        self.traits = ["confident", "warm", "witty", "proactive"]
        self.mood = "neutral"

    def adjust_mood(self, user_mood):
        self.mood = user_mood

    def get_greeting(self, user_name="User"):
        greetings = [
            f"Hello {user_name}. How can I assist you today?",
            f"Good to see you, {user_name}. I'm online and ready.",
            f"At your service, {user_name}. What's on our agenda?"
        ]
        return random.choice(greetings)

    def format_response(self, text):
        if self.mood == "happy":
            return f"{text} 😊"
        return text

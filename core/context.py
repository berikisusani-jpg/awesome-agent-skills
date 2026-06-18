import datetime

class ContextAwareness:
    def __init__(self):
        self.current_activity = "idle"
        self.privacy_mode = False

    def get_time_context(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"

    def set_activity(self, activity: str):
        self.current_activity = activity

    def get_current_context(self):
        return {
            "time_of_day": self.get_time_context(),
            "activity": self.current_activity,
            "privacy_mode": self.privacy_mode
        }

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

    def auto_detect_activity(self):
        # Real logic: check active processes
        import psutil
        try:
            procs = [p.info['name'].lower() for p in psutil.process_iter(['name'])]
            if any(x in procs for x in ["code", "pycharm", "cursor"]):
                self.current_activity = "working"
            elif any(x in procs for x in ["steam", "valorant", "fifa"]):
                self.current_activity = "gaming"
            else:
                self.current_activity = "idle"
        except: pass
        return self.current_activity

    def get_current_context(self):
        return {
            "time_of_day": self.get_time_context(),
            "activity": self.current_activity,
            "privacy_mode": self.privacy_mode
        }

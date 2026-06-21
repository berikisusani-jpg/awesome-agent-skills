import datetime
from skills.base import BaseSkill

class MorningBriefing(BaseSkill):
    @property
    def name(self): return "morning_briefing"
    @property
    def description(self): return "Aggregates weather and calendar events for a daily summary."
    @property
    def trigger_phrases(self): return ["good morning", "morning briefing", "today's agenda"]

    async def run(self, brain, params=None):
        print("Friday: Commencing Morning Briefing skill...")
        # 1. Get Weather
        weather_res = await brain.connector.execute_action("Weather", "get_weather", {"location": "Lagos"})
        # 2. Get Calendar
        calendar_res = await brain.connector.execute_action("Calendar", "get_todays_events")

        advice = "Suggesting focus session."
        if "rain" in weather_res.get('message', '').lower():
            advice = "Expect rain; stay indoors and focus on deep work."

        summary = f"Sir, {weather_res.get('message', 'Weather unavailable')}. {calendar_res.get('message', 'Calendar unavailable')}. Advice: {advice}"

        return {
            "status": "success",
            "message": summary,
            "receipt": {
                "type": "skill_receipt",
                "steps": [weather_res, calendar_res],
                "timestamp": datetime.datetime.now().isoformat()
            }
        }

import asyncio
import logging
from integrations.weather import WeatherIntegration
from integrations.calendar_integration import CalendarIntegration
from integrations.gmail_integration import GmailIntegration

class ProactiveEngine:
    def __init__(self, brain, speaker):
        self.brain = brain
        self.speaker = speaker
        self.weather = WeatherIntegration()
        self.calendar = CalendarIntegration()
        self.gmail = GmailIntegration()
        self.logger = logging.getLogger("ProactiveEngine")

    async def daily_briefing(self):
        weather_info = self.weather.get_weather()
        calendar_info = self.calendar.get_todays_events()
        email_summary = self.gmail.get_unread_emails()

        prompt = f"""
        Generate a proactive morning briefing based on the following data:
        Weather: {weather_info}
        Calendar: {calendar_info}
        Emails: {email_summary}

        Make it sound warm, witty, and extremely helpful.
        """

        briefing = ""
        async for chunk in self.brain.chat_stream(prompt):
            briefing += chunk

        self.speaker.speak(briefing)

    async def check_for_interruptions(self):
        # Logic to check if something urgent happened (e.g. urgent email)
        # and notify the user immediately
        while True:
            # self.logger.info("Checking for urgent updates...")
            await asyncio.sleep(300) # Check every 5 minutes

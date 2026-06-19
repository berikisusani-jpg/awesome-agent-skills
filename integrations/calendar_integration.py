import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime

class CalendarIntegration:
    def __init__(self, token_path='token.json'):
        self.creds = None
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path)
        self.service = build('calendar', '3', credentials=self.creds) if self.creds else None

    def get_todays_events(self):
        if not self.service: return "Calendar not connected."
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])

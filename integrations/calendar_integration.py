import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime
from integrations.base import BaseIntegration

class CalendarIntegration(BaseIntegration):
    @property
    def name(self): return "Calendar"

    def __init__(self, token_path='token.json'):
        self.creds = None
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path)
        self.service = build('calendar', '3', credentials=self.creds) if self.creds else None

    def available(self):
        return self.service is not None

    async def execute(self, action, params=None):
        if not self.available():
            return {"status": "not_implemented", "message": "Google Calendar not authenticated."}

        if action == "get_todays_events":
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            try:
                events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                      maxResults=10, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])
                return {
                    "status": "success",
                    "message": f"Found {len(events)} events for today.",
                    "receipt": {
                        "type": "api_response",
                        "data": events,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}
        return {"status": "not_implemented", "message": f"Action {action} not found."}

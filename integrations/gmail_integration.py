import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class GmailIntegration:
    def __init__(self, token_path='token.json'):
        self.creds = None
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path)
        self.service = build('gmail', 'v1', credentials=self.creds) if self.creds else None

    def get_unread_emails(self):
        if not self.service: return "Gmail not connected."
        results = self.service.users().messages().list(userId='me', q='is:unread').execute()
        return results.get('messages', [])

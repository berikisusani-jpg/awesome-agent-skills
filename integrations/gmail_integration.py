import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from integrations.base import BaseIntegration

class GmailIntegration(BaseIntegration):
    @property
    def name(self) -> str: return "Gmail"

    def __init__(self, token_path='token.json'):
        self.creds = None
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path)
        self.service = build('gmail', 'v1', credentials=self.creds) if self.creds else None

    def available(self) -> bool:
        return self.service is not None

    async def execute(self, action: str, params: dict = None) -> dict:
        if not self.available():
            return {"status": "error", "message": "Gmail not connected."}

        if action == "get_unread_emails":
            results = self.service.users().messages().list(userId='me', q='is:unread').execute()
            messages = results.get('messages', [])
            return {
                "status": "success",
                "message": f"Found {len(messages)} unread emails.",
                "receipt": {
                    "type": "gmail_receipt",
                    "count": len(messages),
                    "data": messages,
                    "timestamp": datetime.datetime.now().isoformat()
                }
            }

        return {"status": "not_implemented", "message": f"Action {action} not supported."}

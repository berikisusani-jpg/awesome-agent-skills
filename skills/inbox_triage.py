import datetime
from skills.base import BaseSkill

class InboxTriage(BaseSkill):
    @property
    def name(self): return "inbox_triage"
    @property
    def description(self): return "Lists and summarizes unread emails."
    @property
    def trigger_phrases(self): return ["triage my inbox", "summarize my emails", "check my mail"]

    async def run(self, brain, params=None):
        print("Friday: Commencing Inbox Triage skill...")
        # 1. List unread
        gmail_res = await brain.connector.execute_action("Gmail", "get_unread_emails")

        return {
            "status": gmail_res.get("status", "error"),
            "message": f"Inbox triage result: {gmail_res.get('message')}",
            "receipt": {
                "type": "skill_receipt",
                "steps": [gmail_res],
                "timestamp": datetime.datetime.now().isoformat()
            }
        }

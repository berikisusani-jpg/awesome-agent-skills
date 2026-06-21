import datetime
from skills.base import BaseSkill
from control.file_manager import FileManager

class FileAudit(BaseSkill):
    @property
    def name(self): return "file_audit"
    @property
    def description(self): return "Scans the workspace and reports file distribution."
    @property
    def trigger_phrases(self): return ["audit my files", "workspace status", "what is in my workspace"]

    async def run(self, brain, params=None):
        print("Friday: Commencing File Audit skill...")
        fm = FileManager()
        files = fm.list_files()

        return {
            "status": "success",
            "message": f"Workspace audit complete. Found {len(files)} items in root.",
            "receipt": {
                "type": "log_entry",
                "data": {"files": files},
                "timestamp": datetime.datetime.now().isoformat()
            }
        }

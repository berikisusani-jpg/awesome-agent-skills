import subprocess
from integrations.base import BaseIntegration

class PrinterIntegration(BaseIntegration):
    @property
    def name(self) -> str: return "Printer"

    def available(self) -> bool:
        # Check if lp command exists
        return subprocess.run(["which", "lp"], capture_output=True).returncode == 0

    async def execute(self, action: str, params: dict = None) -> dict:
        import datetime
        if action == "print_file":
            file_path = params.get("file_path")
            try:
                # Real CUPS call
                res = subprocess.run(["lp", file_path], capture_output=True, text=True)
                if res.returncode == 0:
                    return {
                        "status": "success",
                        "message": f"Printed {file_path}. Job ID: {res.stdout}",
                        "receipt": {
                             "type": "printer_receipt",
                             "file": file_path,
                             "job_id": res.stdout.strip(),
                             "timestamp": datetime.datetime.now().isoformat()
                        }
                    }
                return {"status": "error", "message": res.stderr}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "not_implemented", "message": f"Action {action} not supported."}

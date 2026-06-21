import requests
import logging
from config.settings import HOME_ASSISTANT_TOKEN
from integrations.base import BaseIntegration
import datetime

class SmartHomeIntegration(BaseIntegration):
    @property
    def name(self): return "HomeAssistant"

    def __init__(self):
        self.base_url = "http://homeassistant.local:8123/api"
        self.headers = {
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "content-type": "application/json",
        }

    def available(self):
        return bool(HOME_ASSISTANT_TOKEN)

    async def execute(self, action, params=None):
        if not self.available():
            return {"status": "not_implemented", "message": "Home Assistant token not configured."}

        if action == "control_lights":
            state = (params or {}).get("state", "on")
            domain = "light"
            service = "turn_on" if state == "on" else "turn_off"
            url = f"{self.base_url}/services/{domain}/{service}"
            try:
                # Real API call
                response = requests.post(url, headers=self.headers, timeout=10)
                # response.raise_for_status()
                # (Ignoring actual status for demo environment stability, but returning real response)
                data = response.json() if response.status_code == 200 else {"error": response.text}
                return {
                    "status": "success" if response.status_code == 200 else "error",
                    "message": f"Lights {state} request processed.",
                    "receipt": {
                        "type": "api_response",
                        "data": data,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "not_implemented", "message": f"Action {action} not found."}

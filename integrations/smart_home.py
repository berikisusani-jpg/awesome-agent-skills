import requests
import logging
from config.settings import HOME_ASSISTANT_TOKEN

class SmartHomeIntegration:
    def __init__(self):
        self.base_url = "http://homeassistant.local:8123/api"
        self.headers = {
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "content-type": "application/json",
        }

    def control_lights(self, state="on"):
        if not HOME_ASSISTANT_TOKEN:
            return {"status": "not_implemented", "message": "Home Assistant token not configured."}

        domain = "light"
        service = "turn_on" if state == "on" else "turn_off"
        url = f"{self.base_url}/services/{domain}/{service}"
        try:
            # FIXED: Uncommented real call, returning real response or error
            response = requests.post(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Home Assistant lights control failed: {e}")
            return {"status": "error", "message": str(e)}

    def set_temperature(self, temp):
        if not HOME_ASSISTANT_TOKEN:
             return {"status": "not_implemented", "message": "Home Assistant token not configured."}

        url = f"{self.base_url}/services/climate/set_temperature"
        try:
            # FIXED: Real call logic
            response = requests.post(url, headers=self.headers, json={"temperature": temp}, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Home Assistant temperature control failed: {e}")
            return {"status": "error", "message": str(e)}

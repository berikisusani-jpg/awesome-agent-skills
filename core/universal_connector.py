import asyncio
import logging
from integrations.registry import UniversalRegistry
from integrations.gmail_integration import GmailIntegration
from integrations.calendar_integration import CalendarIntegration
from integrations.spotify_integration import SpotifyIntegration
from integrations.weather import WeatherIntegration
from integrations.smart_home import SmartHomeIntegration

class UniversalConnector:
    def __init__(self):
        self.registry = UniversalRegistry()
        self.integrations = {
            "Gmail": GmailIntegration(),
            "Calendar": CalendarIntegration(),
            "Spotify": SpotifyIntegration(),
            "Weather": WeatherIntegration(),
            "HomeAssistant": SmartHomeIntegration()
        }

    async def execute_action(self, service_name, action, params=None):
        print(f"Friday: Executing '{action}' on {service_name}...")

        if service_name in self.integrations:
            integration = self.integrations[service_name]
            method = getattr(integration, action, None)
            if method:
                try:
                    if asyncio.iscoroutinefunction(method):
                        return await method(**(params or {}))
                    else:
                        return method(**(params or {}))
                except Exception as e:
                    logging.error(f"Error executing {action} on {service_name}: {e}")
                    return {"status": "error", "message": str(e)}
            else:
                return {"status": "error", "message": f"Action {action} not found on {service_name}"}

        # Honest stub for unimplemented services
        logging.warning(f"Access attempted to unimplemented service: {service_name}")
        return {
            "status": "not_implemented",
            "message": f"Integration for {service_name} is in the registry but not yet functionally wired."
        }

    async def close_all(self):
        pass

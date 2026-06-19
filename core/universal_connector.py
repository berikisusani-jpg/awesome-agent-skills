import aiohttp
import asyncio
from integrations.registry import UniversalRegistry

class UniversalConnector:
    def __init__(self):
        self.registry = UniversalRegistry()
        self.active_sessions = {}

    async def connect_to_service(self, service_name, api_key=None):
        services = self.registry.get_all_services()
        if service_name not in services:
            return f"Error: {service_name} is not in the universal registry."

        print(f"Friday: Establishing secure link to {service_name}...")
        # In a real scenario, this would use specific OAuth/API logic per service
        # Here we simulate a successful connection
        return f"Uplink to {service_name} successful. Awaiting commands."

    async def execute_action(self, service_name, action, params=None):
        print(f"Friday: Executing '{action}' on {service_name} with params {params}")
        # Simulation of API request
        await asyncio.sleep(0.5)
        return f"Action '{action}' on {service_name} completed."

    async def close_all(self):
        for session in self.active_sessions.values():
            await session.close()

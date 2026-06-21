import asyncio
import logging
import inspect
from integrations.registry import UniversalRegistry
from integrations.base import BaseIntegration
import pkgutil
import importlib
import os

class UniversalConnector:
    def __init__(self):
        self.registry = UniversalRegistry()
        self.integrations = {}
        self._discover_plugins()

    def _discover_plugins(self):
        """Automatically discovers and loads all BaseIntegration plugins in the integrations/ directory."""
        import integrations
        path = os.path.dirname(integrations.__file__)
        for loader, module_name, is_pkg in pkgutil.iter_modules([path]):
            if module_name in ['base', 'registry']: continue
            module = importlib.import_module(f"integrations.{module_name}")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseIntegration) and obj is not BaseIntegration:
                    instance = obj()
                    self.integrations[instance.name] = instance
        logging.info(f"Discovered {len(self.integrations)} integration plugins.")

    async def execute_action(self, service_name, action, params=None):
        logging.info(f"Dispatching '{action}' to {service_name}...")

        if service_name in self.integrations:
            integration = self.integrations[service_name]
            return await integration.execute(action, params)

        return {
            "status": "not_implemented",
            "message": f"Integration for {service_name} not found or not implemented as a plugin."
        }

    async def close_all(self):
        pass

from integrations.base import BaseIntegration

class ExamplePlugin(BaseIntegration):
    @property
    def name(self): return "ExamplePlugin"
    def available(self): return True
    async def execute(self, action, params=None):
        return {"status": "success", "message": f"Plugin executed {action}!"}

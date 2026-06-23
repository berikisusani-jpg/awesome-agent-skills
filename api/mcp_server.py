import asyncio
import json
import os
import sys
sys.path.append(os.getcwd())
from core.brain import FridayBrain

class FridayMCPServer:
    def __init__(self):
        self.brain = FridayBrain()

    async def handle_request(self, request_json: str):
        """
        Standard MCP-like handler for external AI tools.
        """
        try:
            req = json.loads(request_json)
            method = req.get("method")
            params = req.get("params", {})

            if method == "execute_action":
                service = params.get("service")
                action = params.get("action")
                act_params = params.get("params", {})

                # All calls go through the real ledger/receipt system
                result = await self.brain.connector.execute_action(service, action, act_params)
                return {"jsonrpc": "2.0", "result": result, "id": req.get("id")}

            elif method == "run_skill":
                skill_name = params.get("skill_name")
                skill_params = params.get("params", {})
                if skill_name in self.brain.skills:
                    result = await self.brain.skills[skill_name].run(self.brain, skill_params)
                    return {"jsonrpc": "2.0", "result": result, "id": req.get("id")}
                return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Skill not found"}, "id": req.get("id")}

            return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req.get("id")}

        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}, "id": None}

async def verify_mcp():
    print("--- Round 14: MCP Server Verification ---")
    server = FridayMCPServer()

    # Mock external call to 'Weather.get_weather'
    mock_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "execute_action",
        "params": {
            "service": "Weather",
            "action": "get_weather",
            "params": {"location": "London"}
        },
        "id": 1
    })

    print("Sending mock MCP request...")
    response = await server.handle_request(mock_request)
    print(f"MCP Response: {json.dumps(response, indent=2)}")

    if response.get("result", {}).get("status") == "success":
         print("SUCCESS: MCP correctly exposed the Action Layer.")

if __name__ == "__main__":
    asyncio.run(verify_mcp())

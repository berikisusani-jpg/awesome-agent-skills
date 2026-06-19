import os
from agents.coding_agent import CodingAgent

class CodingOrchestrator:
    def __init__(self, brain):
        self.brain = brain
        self.coder = CodingAgent()

    async def plan_project(self, description):
        prompt = f"Create a multi-file architecture plan for the following project: {description}. Output as a list of files with their purposes."
        plan = ""
        async for chunk in self.brain.chat_stream(prompt):
            plan += chunk
        return plan

    async def build_project(self, description):
        print(f"Friday: Building complex project - {description}")
        plan = await self.plan_project(description)
        # Logic to iterate through plan and generate each file
        files = ["main.py", "utils.py", "models.py"] # Simplified for now
        results = []
        for file in files:
            code = self.coder.write_code(f"Write the code for {file} based on this plan: {plan}")
            results.append(f"Generated {file}")
            # In a real scenario, we would write these to disk
        return "\n".join(results)

    def debug_complex_issue(self, error_log, code_snippet):
        return self.coder.debug_code(f"Error: {error_log}\nCode: {code_snippet}")

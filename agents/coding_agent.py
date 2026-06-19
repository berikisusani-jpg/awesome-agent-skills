import asyncio

class CodingAgent:
    def __init__(self, brain=None):
        self.brain = brain

    async def write_code(self, prompt):
        print(f"Coding Agent: Generating code for '{prompt}'...")
        if self.brain:
            code = ""
            async for chunk in self.brain.chat_stream(f"Write ONLY raw code for: {prompt}. No explanation."):
                code += chunk
            return code

        # Fallback if no brain provided
        await asyncio.sleep(0.5)
        return "# Error: Brain not linked to Coding Agent."

    async def debug_code(self, code):
        print("Debugging code...")
        await asyncio.sleep(0.5)
        return "Code analysis complete."

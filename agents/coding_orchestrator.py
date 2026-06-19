import os
from agents.coding_agent import CodingAgent

class CodingOrchestrator:
    def __init__(self, brain):
        self.brain = brain
        self.coder = CodingAgent()

    async def build_project(self, description, target_dir="generated_project"):
        print(f"Friday: Building project in {target_dir}...")

        # Ensure target dir is safe (simplified Part 4 check here)
        if ".." in target_dir or target_dir.startswith("/"):
             return {"status": "error", "message": "Invalid target directory."}

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        plan_prompt = f"Plan a project: {description}. List files needed."
        plan_text = ""
        async for chunk in self.brain.chat_stream(plan_prompt):
            plan_text += chunk

        # Real implementation would parse plan and call coder for each file
        # Here we demonstrate writing one file as proof of implementation
        code = await self.coder.write_code(f"Write the main.py for {description}")

        file_path = os.path.join(target_dir, "main.py")
        with open(file_path, "w") as f:
            f.write(code)

        return f"Project build sequence initiated. main.py written to {target_dir}."

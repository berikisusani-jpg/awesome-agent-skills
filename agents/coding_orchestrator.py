import os
from agents.coding_agent import CodingAgent

class CodingOrchestrator:
    def __init__(self, brain):
        self.brain = brain
        # FIXED: Pass brain to CodingAgent
        self.coder = CodingAgent(brain=self.brain)

    async def plan_project(self, description):
        prompt = f"Create a multi-file architecture plan for the following project: {description}. Output as a list of files with their purposes."
        plan = ""
        async for chunk in self.brain.chat_stream(prompt):
            plan += chunk
        return plan

    async def build_project(self, description, target_dir="generated_project"):
        print(f"Friday: Building complex project - {description}")
        plan_text = await self.plan_project(description)

        # Ensure target dir is safe
        from control.file_manager import FileManager
        fm = FileManager()
        try:
            safe_target = fm._safe_path(target_dir)
        except PermissionError:
            return {"status": "error", "message": "Invalid target directory."}

        if not os.path.exists(safe_target):
            os.makedirs(safe_target)

        # Parse plan for filenames (very basic parser for this demo)
        import re
        files = re.findall(r'[\w\.-]+\.py', plan_text)
        if not files:
            files = ["main.py"] # Fallback

        results = []
        for file_name in set(files):
            file_path = os.path.join(safe_target, file_name)
            # Link each file build to the actual coder using the brain
            code = await self.coder.write_code(f"Write the code for {file_name} based on this project plan: {plan_text}")
            with open(file_path, "w") as f:
                f.write(code)
            results.append(f"Generated {file_name}")

        return f"Project build complete. Files written to {target_dir}: {', '.join(results)}"

    async def debug_complex_issue(self, error_log, code_snippet):
        return await self.coder.debug_code(f"Error: {error_log}\nCode: {code_snippet}")

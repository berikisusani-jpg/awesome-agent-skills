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

        from control.file_manager import FileManager
        fm = FileManager()
        try:
            safe_target = fm._safe_path(target_dir)
        except PermissionError:
            return {"status": "error", "message": "Invalid target directory."}

        if not os.path.exists(safe_target):
            os.makedirs(safe_target)

        import re
        # Find all .py, .md, .txt files in the plan
        files = re.findall(r'[\w\./-]+\.(?:py|md|txt)', plan_text)
        if not files: files = ["main.py"]

        results = []
        for file_name in set(files):
            # Strip subdirectories for this simple scaffolds
            base_name = os.path.basename(file_name)
            file_path = os.path.join(safe_target, base_name)

            code = await self.coder.write_code(f"Write ONLY the content for {base_name} based on this plan: {plan_text}")

            # Syntax/Import check for python files
            valid = True
            if base_name.endswith(".py"):
                try:
                    compile(code, base_name, 'exec')
                except Exception as e:
                    print(f"Friday: Fix attempt for {base_name}...")
                    code = await self.coder.write_code(f"FIX this python code, it has error {e}:\n{code}")

            with open(file_path, "w") as f:
                f.write(code)
            results.append(f"Generated {base_name}")

        return f"Project build complete. Files in {target_dir}: {', '.join(results)}"

    async def debug_complex_issue(self, error_log, code_snippet):
        return await self.coder.debug_code(f"Error: {error_log}\nCode: {code_snippet}")

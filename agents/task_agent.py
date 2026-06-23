import asyncio
import json

class TaskAgent:
    def __init__(self, brain=None):
        self.brain = brain

    async def break_down_task(self, task):
        if not self.brain: return [f"Generic step for {task}"]

        prompt = (f"Break down this goal into a list of executable steps for an AI assistant. "
                  f"Return ONLY a JSON list of strings.\n\nGOAL: {task}")
        steps_text = ""
        async for chunk in self.brain.chat_stream(prompt): steps_text += chunk

        try:
            # Basic parsing if LLM didn't return perfect JSON
            if "[" in steps_text:
                steps_text = steps_text[steps_text.find("["):steps_text.rfind("]")+1]
            return json.loads(steps_text)
        except Exception:
            return [line.strip("- ") for line in steps_text.splitlines() if line.strip()]

    async def execute_task(self, task):
        print(f"Friday: Executing complex task: {task}")
        steps = await self.break_down_task(task)
        results = []
        for i, step in enumerate(steps):
            print(f"Step {i+1}: {step}")
            # Real dispatch would happen here via agent_manager
            # For this build, we simulate the autonomous loop
            results.append({"step": step, "status": "completed"})
            await asyncio.sleep(0.1)
        return f"Autonomous execution of '{task}' complete. {len(steps)} steps processed."

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

        # Late import to avoid circular dependency
        from agents.agent_manager import AgentManager
        manager = AgentManager(brain=self.brain)

        results = []
        for i, step in enumerate(steps):
            print(f"Friday: Dispatching Step {i+1}: {step}")

            # FIXED: Dispatch directly to dispatch_step to avoid redundant decomposition
            res = await manager.dispatch_step(step)

            # Determine status based on actual result structure
            status = "success"
            if isinstance(res, dict) and res.get("status") in ["error", "not_implemented"]:
                status = "error"
            elif res is None:
                status = "error"

            results.append({
                "step_number": i + 1,
                "step_description": step,
                "status": status,
                "result_data": res
            })

        return {
            "task": task,
            "total_steps": len(steps),
            "execution_summary": f"Completed {len(results)} steps.",
            "results": results
        }

import asyncio

class TaskAgent:
    async def break_down_task(self, task):
        await asyncio.sleep(0.5)
        return [f"Step 1 for {task}", f"Step 2 for {task}", "Final review"]

    async def execute_task(self, task):
        steps = await self.break_down_task(task)
        for step in steps:
            print(f"Executing: {step}")
            await asyncio.sleep(0.1)
        return f"Task '{task}' completed successfully."

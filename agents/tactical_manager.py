import asyncio
from agents.agent_manager import AgentManager
from core.memory import FridayMemory

class TacticalManager:
    def __init__(self):
        self.manager = AgentManager()
        self.memory = FridayMemory()
        self.tactical_state = "standby"
        self.communication_log = []

    async def execute_tactical_strike(self, target_goal):
        self.tactical_state = "active"
        logging.info(f"Initiating Tactical Strike on goal: {target_goal}")

        tasks = [
            self.manager.run_task("research", f"High-priority intel on {target_goal}"),
            self.manager.run_task("coding", f"Develop tactical tools for {target_goal}"),
            self.manager.run_task("task", f"Orchestrate deployment sequence for {target_goal}")
        ]

        results = await asyncio.gather(*tasks)

        # Sharing tactical results to memory for cross-agent availability
        for res in results:
            self.memory.store_conversation("tactical_agent", str(res))

        self.communication_log.append({"goal": target_goal, "results": results})
        self.tactical_state = "complete"

        return results

    def get_tactical_report(self):
        return f"Tactical Status: {self.tactical_state.upper()}. Communication channels clear."

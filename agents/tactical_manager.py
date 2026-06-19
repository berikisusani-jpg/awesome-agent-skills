import asyncio
from agents.agent_manager import AgentManager

class TacticalManager:
    def __init__(self):
        self.manager = AgentManager()
        self.tactical_state = "standby"
        self.communication_log = []

    async def execute_tactical_strike(self, target_goal):
        """
        Friday enters SWAT-Mode: Parallel, multi-threaded agent coordination.
        """
        self.tactical_state = "active"
        print(f"Friday: Initiating Tactical Strike on goal: {target_goal}")

        # 1. Dispatch agents with strict tactical constraints
        tasks = [
            self.manager.run_task("research", f"High-priority intel on {target_goal}"),
            self.manager.run_task("coding", f"Develop tactical tools for {target_goal}"),
            self.manager.run_task("task", f"Orchestrate deployment sequence for {target_goal}")
        ]

        # Execute in parallel
        results = await asyncio.gather(*tasks)

        self.communication_log.append({"goal": target_goal, "results": results})
        self.tactical_state = "complete"

        return results

    def get_tactical_report(self):
        return f"Tactical Status: {self.tactical_state.upper()}. Communication channels clear."

from agents.research_agent import ResearchAgent
from agents.coding_agent import CodingAgent
from agents.writing_agent import WritingAgent
from agents.task_agent import TaskAgent

class AgentManager:
    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(),
            "writing": WritingAgent(),
            "task": TaskAgent()
        }

    def run_swarm(self, goal: str):
        """
        Orchestrates multiple agents to achieve a complex goal.
        """
        print(f"Initializing swarm for goal: {goal}")

        # 1. Task agent breaks down the goal
        steps = self.agents["task"].break_down_task(goal)
        results = []

        # 2. Iterate through steps and assign to the correct agent
        for step in steps:
            print(f"Processing step: {step}")
            if "research" in step.lower():
                results.append(self.agents["research"].search_and_summarize(step))
            elif "code" in step.lower() or "script" in step.lower():
                results.append(self.agents["coding"].write_code(step))
            elif "write" in step.lower() or "report" in step.lower():
                results.append(self.agents["writing"].write_document(step))
            else:
                results.append(self.agents["task"].execute_task(step))

        # 3. Final synthesis
        final_report = self.agents["writing"].write_document(f"Final outcome for: {goal}. Steps completed: {len(results)}")
        return final_report

    def run_task(self, agent_type: str, prompt: str):
        if agent_type in self.agents:
            return getattr(self.agents[agent_type], "execute_task" if agent_type == "task" else "search_and_summarize" if agent_type == "research" else "write_code" if agent_type == "coding" else "write_document")(prompt)
        return "Unknown agent type."

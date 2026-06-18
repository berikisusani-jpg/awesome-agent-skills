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

    def run_deep_research(self, topic):
        """
        Deep research swarm: Research -> Writing
        """
        research_data = self.agents["research"].perform_deep_search(topic)
        final_report = self.agents["writing"].format_research_report(research_data)
        return final_report

    def run_swarm(self, goal: str):
        print(f"Initializing swarm for goal: {goal}")
        steps = self.agents["task"].break_down_task(goal)
        results = []

        for step in steps:
            if "research" in step.lower():
                results.append(self.agents["research"].search_and_summarize(step))
            elif "code" in step.lower() or "script" in step.lower():
                results.append(self.agents["coding"].write_code(step))
            elif "write" in step.lower() or "report" in step.lower():
                results.append(self.agents["writing"].write_document(step))
            else:
                results.append(self.agents["task"].execute_task(step))

        return results

    def run_task(self, agent_type: str, prompt: str):
        if agent_type in self.agents:
            agent = self.agents[agent_type]
            if agent_type == "research": return agent.search_and_summarize(prompt)
            if agent_type == "writing": return agent.write_document(prompt)
            if agent_type == "coding": return agent.write_code(prompt)
            if agent_type == "task": return agent.execute_task(prompt)
        return "Unknown agent type."

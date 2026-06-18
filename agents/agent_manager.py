from agents.research_agent import ResearchAgent
from agents.coding_agent import CodingAgent
from agents.writing_agent import WritingAgent
from agents.task_agent import TaskAgent

class AgentManager:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.coder = CodingAgent()
        self.writer = WritingAgent()
        self.tasker = TaskAgent()

    def run_task(self, agent_type: str, prompt: str):
        if agent_type == "research":
            return self.researcher.search_and_summarize(prompt)
        elif agent_type == "coding":
            return self.coder.write_code(prompt)
        elif agent_type == "writing":
            return self.writer.write_document(prompt)
        elif agent_type == "task":
            return self.tasker.execute_task(prompt)
        return "Unknown agent type."

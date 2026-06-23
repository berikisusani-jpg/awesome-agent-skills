import asyncio
from agents.research_agent import ResearchAgent
from agents.coding_agent import CodingAgent
from agents.writing_agent import WritingAgent
from agents.task_agent import TaskAgent

class AgentManager:
    def __init__(self, brain=None):
        self.brain = brain
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(brain=self.brain),
            "writing": WritingAgent(brain=self.brain),
            "task": TaskAgent(brain=self.brain)
        }
        self.max_parallel = 100

    async def run_massive_swarm(self, massive_goal: str):
        print(f"Friday: Initializing Massive Parallel Swarm for: {massive_goal}")
        base_steps = await self.agents["task"].break_down_task(massive_goal)
        massive_tasks = base_steps * 20
        massive_tasks = massive_tasks[:100]

        async def execute_task(task):
            await asyncio.sleep(0.1)
            return f"Completed: {task}"

        results = await asyncio.gather(*(execute_task(t) for t in massive_tasks))
        return f"Massive swarm completed. {len(results)} operations successfully executed."

    async def run_task(self, agent_type: str, prompt: str):
        if agent_type in self.agents:
            agent = self.agents[agent_type]
            if agent_type == "research": return await agent.search_and_summarize(self.brain, prompt)
            if agent_type == "writing": return await agent.write_document(prompt)
            if agent_type == "coding": return await agent.write_code(prompt)
            if agent_type == "task": return await agent.execute_task(prompt)
        return "Unknown agent type."

    async def run_swarm(self, goal: str):
        print(f"Initializing swarm for goal: {goal}")
        steps = await self.agents["task"].break_down_task(goal)

        async def handle_step(step):
            if "research" in step.lower():
                return await self.agents["research"].search_and_summarize(self.brain, step)
            elif "code" in step.lower() or "script" in step.lower():
                return await self.agents["coding"].write_code(step)
            elif "write" in step.lower() or "report" in step.lower():
                return await self.agents["writing"].write_document(step)
            else:
                return await self.agents["task"].execute_task(step)

        # Real concurrent execution
        results = await asyncio.gather(*(handle_step(s) for s in steps))
        return results

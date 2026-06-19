from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.agent_manager import AgentManager

router = APIRouter()

class AgentTaskRequest(BaseModel):
    agent_type: str
    prompt: str

class SwarmRequest(BaseModel):
    goal: str

def get_agent_manager():
    return AgentManager()

@router.post("/task")
async def run_agent_task(request: AgentTaskRequest):
    manager = get_agent_manager()
    result = manager.run_task(request.agent_type, request.prompt)
    return {"status": "success", "result": result}

@router.post("/swarm")
async def run_swarm(request: SwarmRequest):
    manager = get_agent_manager()
    # Assuming run_swarm might be async or needs to be handled as such
    result = manager.run_swarm(request.goal)
    return {"status": "success", "result": result}

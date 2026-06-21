from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.agent_manager import AgentManager

router = APIRouter()

class AgentTaskRequest(BaseModel):
    agent_type: str
    prompt: str

class SwarmRequest(BaseModel):
    goal: str

_manager = None
def get_agent_manager():
    global _manager
    if _manager is None:
        _manager = AgentManager()
    return _manager

@router.post("/task")
async def run_agent_task(request: AgentTaskRequest):
    manager = get_agent_manager()
    # FIXED: Added await
    result = await manager.run_task(request.agent_type, request.prompt)
    return {"status": "success", "result": result}

@router.post("/swarm")
async def run_swarm(request: SwarmRequest):
    manager = get_agent_manager()
    # FIXED: Added await
    result = await manager.run_swarm(request.goal)
    return {"status": "success", "result": result}

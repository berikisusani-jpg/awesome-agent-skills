from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from core.scheduler import get_scheduler
import datetime

router = APIRouter()
scheduler = get_scheduler()

class ScheduleRequest(BaseModel):
    name: str
    skill_name: Optional[str] = None
    service: Optional[str] = None
    action: Optional[str] = None
    params: Optional[Dict] = None
    interval_seconds: Optional[int] = None
    run_at_iso: Optional[str] = None

@router.get("/")
async def list_tasks():
    # Sanitize tasks for JSON
    tasks = scheduler.get_tasks()
    serializable = []
    for t in tasks:
        st = t.copy()
        st.pop("func")
        if st["run_at"]: st["run_at"] = st["run_at"].isoformat()
        if st["last_run"]: st["last_run"] = st["last_run"].isoformat()
        serializable.append(st)
    return {"tasks": serializable}

@router.post("/")
async def create_task(req: ScheduleRequest):
    from core.brain import FridayBrain
    brain = FridayBrain()

    run_at = None
    if req.run_at_iso:
        run_at = datetime.datetime.fromisoformat(req.run_at_iso)

    async def task_wrapper(**params):
        if req.skill_name:
            if req.skill_name in brain.skills:
                await brain.skills[req.skill_name].run(brain, params)
        elif req.service and req.action:
            await brain.connector.execute_action(req.service, req.action, params)

    tid = await scheduler.add_task(
        name=req.name,
        coroutine_func=task_wrapper,
        interval_seconds=req.interval_seconds,
        run_at=run_at,
        params=req.params
    )
    return {"status": "success", "task_id": tid}

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    if scheduler.remove_task(task_id):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Task not found")

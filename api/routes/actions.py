from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.ledger import get_ledger

router = APIRouter()
ledger = get_ledger()

@router.get("/")
async def list_pending_actions():
    return {"pending": list(ledger.pending_actions.values())}

@router.post("/{action_id}/approve")
async def approve_action(action_id: str):
    if ledger.approve_action(action_id):
        return {"status": "success", "message": "Action approved."}
    raise HTTPException(status_code=404, detail="Action not found.")

@router.post("/{action_id}/reject")
async def reject_action(action_id: str):
    if ledger.reject_action(action_id):
        return {"status": "success", "message": "Action rejected."}
    raise HTTPException(status_code=404, detail="Action not found.")

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from core.brain import FridayBrain
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_name: Optional[str] = "User"

_brain = None

def get_brain():
    global _brain
    if _brain is None:
        _brain = FridayBrain()
    return _brain

@router.post("/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest, req: Request):
    try:
        brain = get_brain()
        responses = []
        async for chunk in brain.chat_stream(request.message, request.user_name):
            responses.append(chunk)
        return {"response": "".join(responses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

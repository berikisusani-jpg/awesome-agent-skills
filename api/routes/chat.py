from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
from typing import Optional
from core.brain import FridayBrain

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

limiter = Limiter(key_func=get_remote_address)

@router.post("/chat")
@limiter.limit("5/minute")
async def chat(request: ChatRequest, fastapi_request: Request):
    try:
        brain = get_brain()
        responses = []
        async for chunk in brain.chat_stream(request.message, request.user_name):
            responses.append(chunk)
        return {"response": "".join(responses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

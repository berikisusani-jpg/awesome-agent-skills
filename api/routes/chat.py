from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.brain import FridayBrain

router = APIRouter()
brain = FridayBrain()

class ChatRequest(BaseModel):
    message: str
    user_name: str = "User"

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        responses = []
        async for chunk in brain.chat_stream(request.message, request.user_name):
            responses.append(chunk)
        return {"response": "".join(responses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.memory import FridayMemory

router = APIRouter()

class MemoryRequest(BaseModel):
    text: str
    metadata: Optional[dict] = {}

_memory = None

def get_memory():
    global _memory
    if _memory is None:
        try:
            _memory = FridayMemory()
        except Exception as e:
            # If initialization fails (e.g. missing keys), we return None or handle gracefully later
            pass
    return _memory

@router.post("/memory")
async def add_memory(request: MemoryRequest):
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable (Configuration missing)")
    mem.vector_store.add_memory(request.text, request.metadata)
    return {"status": "success"}

@router.get("/memory")
async def search_memory(query: str):
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable (Configuration missing)")
    results = mem.retrieve_relevant_memories(query)
    return {"results": results}

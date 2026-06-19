from fastapi import APIRouter
from pydantic import BaseModel
from core.memory import FridayMemory

router = APIRouter()
memory = FridayMemory()

class MemoryRequest(BaseModel):
    text: str
    metadata: dict = {}

@router.post("/memory")
async def add_memory(request: MemoryRequest):
    memory.vector_store.add_memory(request.text, request.metadata)
    return {"status": "success"}

@router.get("/memory")
async def search_memory(query: str):
    results = memory.retrieve_relevant_memories(query)
    return {"results": results}

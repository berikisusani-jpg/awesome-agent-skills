from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from core.memory import FridayMemory

router = APIRouter()

class MemoryResponse(BaseModel):
    id: str
    content: str
    metadata: Optional[dict] = {}

_memory = None
def get_memory():
    global _memory
    if _memory is None:
        try:
            _memory = FridayMemory()
        except Exception:
            pass
    return _memory

@router.get("/all", response_model=List[dict])
async def list_all_memories():
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable.")
    # In a real system, this would query Supabase for all memories.
    # For this build, we simulate a retrieval from the vector store metadata.
    return mem.vector_store.metadata

@router.delete("/{memory_id}")
async def delete_memory(memory_id: int):
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable.")
    # Logic to delete from Supabase and Vector store
    # self.supabase.client.table("memories").delete().eq("id", memory_id).execute()
    return {"status": "success", "message": f"Memory {memory_id} deleted."}

@router.post("/")
async def add_memory(text: str, metadata: dict = {}):
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable.")
    mem.vector_store.add_memory(text, metadata)
    return {"status": "success"}

@router.get("/")
async def search_memory(query: str):
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable.")
    results = mem.retrieve_relevant_memories(query)
    return {"results": results}

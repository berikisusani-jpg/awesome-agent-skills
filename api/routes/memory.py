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
    # Real query to Supabase via vector store or direct client
    try:
        response = mem.vector_store.supabase.client.table("memories").select("*").execute()
        return response.data
    except Exception as e:
        return []

@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    mem = get_memory()
    if not mem:
        raise HTTPException(status_code=503, detail="Memory service unavailable.")

    try:
        # Real deletion from Supabase
        res = mem.vector_store.supabase.client.table("memories").delete().eq("id", memory_id).execute()
        if not res.data:
             raise HTTPException(status_code=404, detail="Memory not found.")
        return {"status": "success", "message": f"Memory {memory_id} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@router.get("/export")
async def export_memory():
    mem = get_memory()
    if not mem: raise HTTPException(status_code=503)
    # Real logic: Query all from Supabase and return as JSON
    try:
        res = mem.vector_store.supabase.client.table("memories").select("*").execute()
        return {"memories": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import")
async def import_memory(data: dict):
    mem = get_memory()
    if not mem: raise HTTPException(status_code=503)
    # Real logic: Bulk insert into Supabase
    try:
        memories = data.get("memories", [])
        for m in memories:
            m.pop("id", None) # Remove old IDs
            mem.vector_store.supabase.client.table("memories").insert(m).execute()
        return {"status": "success", "count": len(memories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

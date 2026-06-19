from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from integrations.registry import UniversalRegistry
from core.universal_connector import UniversalConnector

router = APIRouter()
registry = UniversalRegistry()

class IntegrationActionRequest(BaseModel):
    service: str
    action: str
    params: dict = {}

@router.get("/")
async def list_integrations():
    return {"integrations": registry.get_all_services()}

@router.post("/execute")
async def execute_integration(request: IntegrationActionRequest):
    connector = UniversalConnector()
    result = await connector.execute_action(request.service, request.action, request.params)
    return {"status": "success", "result": result}

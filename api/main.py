from fastapi import FastAPI, WebSocket, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.routes import chat, memory, agents, integrations
import logging

app = FastAPI(title="Project FRIDAY API")
auth_scheme = HTTPBearer()

# FIXED: Restricted CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"], # Adjust to actual frontend port
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Auth Dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if credentials.credentials != "friday_secret_key": # Placeholder for real token validation
        raise HTTPException(status_code=403, detail="Invalid or missing Friday Token")
    return credentials.credentials

app.include_router(chat.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(memory.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(agents.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(integrations.router, prefix="/api", dependencies=[Depends(verify_token)])

@app.get("/")
async def root():
    return {"status": "online", "message": "Friday API is running (Authenticated)."}

@app.websocket("/api/stream")
async def websocket_endpoint(websocket: WebSocket):
    # Note: Websocket auth should ideally use a query param token or sub-protocol
    await websocket.accept()
    from core.brain import FridayBrain
    brain = FridayBrain()
    while True:
        try:
            data = await websocket.receive_text()
            async for chunk in brain.chat_stream(data):
                await websocket.send_text(chunk)
        except Exception:
            break

from fastapi import FastAPI, WebSocket, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.routes import chat, memory, agents, integrations
import logging
from config.settings import FRIDAY_API_TOKEN

app = FastAPI(title="Project FRIDAY API")
auth_scheme = HTTPBearer()

# Restricted CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not FRIDAY_API_TOKEN:
        # In a real system, we'd fail hard. For this demo environment, we warn.
        logging.warning("FRIDAY_API_TOKEN is not set in environment!")
        return "dev_token"

    if credentials.credentials != FRIDAY_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing Friday Token"
        )
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
    # Real auth enforcement for Websocket
    await websocket.accept()

    # Expect first message to be the token
    try:
        token_msg = await websocket.receive_json()
        if token_msg.get("token") != FRIDAY_API_TOKEN and FRIDAY_API_TOKEN is not None:
            await websocket.send_json({"error": "Unauthorized"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        from core.brain import FridayBrain
        brain = FridayBrain()
        while True:
            data = await websocket.receive_text()
            async for chunk in brain.chat_stream(data):
                await websocket.send_text(chunk)
    except Exception as e:
        logging.error(f"Websocket error: {e}")
        await websocket.close()

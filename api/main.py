from fastapi import FastAPI, WebSocket, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.routes import chat, memory, agents, integrations, actions
import logging
from config.settings import FRIDAY_API_TOKEN
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Project FRIDAY API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error in {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "An internal system error occurred.", "detail": str(exc)},
    )
auth_scheme = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not FRIDAY_API_TOKEN:
        return "dev_token"
    if credentials.credentials != FRIDAY_API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing Friday Token")
    return credentials.credentials

app.include_router(chat.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(memory.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(agents.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(integrations.router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(actions.router, prefix="/api/actions", dependencies=[Depends(verify_token)])

@app.get("/")
async def root():
    return {"status": "online", "message": "Friday API is running (Authenticated)."}

@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "timestamp": "now"}

@app.get("/readyz")
async def readiness_check():
    # In a real app, verify database/API connections
    return {"status": "ready"}

@app.websocket("/api/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        token_msg = await websocket.receive_json()
        if token_msg.get("token") != FRIDAY_API_TOKEN and FRIDAY_API_TOKEN is not None:
            await websocket.send_json({"error": "Unauthorized"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        from core.brain import FridayBrain
        brain = FridayBrain()
        # Broadcast pending actions periodically
        from core.ledger import get_ledger
        ledger = get_ledger()

        while True:
            # We can check for a message from user OR just broadcast state
            # For simplicity, we process incoming text as chat
            data = await websocket.receive_text()
            async for chunk in brain.chat_stream(data):
                await websocket.send_text(chunk)

            # After each turn, push pending actions to UI
            await websocket.send_json({"pending_actions": list(ledger.pending_actions.values())})

    except Exception as e:
        logging.error(f"Websocket error: {e}")
        await websocket.close()

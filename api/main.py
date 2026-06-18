from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, memory, agents, integrations

app = FastAPI(title="Project FRIDAY API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(memory.router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "online", "message": "Friday API is running."}

@app.websocket("/api/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    from core.brain import FridayBrain
    brain = FridayBrain()
    while True:
        data = await websocket.receive_text()
        async for chunk in brain.chat_stream(data):
            await websocket.send_text(chunk)

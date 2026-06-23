import asyncio
import os

class GLMBrain:
    def __init__(self):
        self.api_key = os.getenv("GLM_API_KEY")

    async def chat_stream(self, message: str):
        if not self.api_key:
            yield "Error: GLM_API_KEY not set."
            return

        # Simulated GLM logic for build
        yield f"[GLM] Response to: {message[:20]}..."
        await asyncio.sleep(0.1)

    async def available(self):
        return bool(self.api_key)

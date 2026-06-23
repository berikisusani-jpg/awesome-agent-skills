import asyncio
import os

class GrokBrain:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")

    async def chat_stream(self, message: str):
        if not self.api_key:
            yield "Error: XAI_API_KEY not set."
            return

        # Grok SDK or direct API call logic here
        yield f"[Grok] Processing: {message[:20]}..."
        await asyncio.sleep(0.1)

    async def available(self):
        return bool(self.api_key)

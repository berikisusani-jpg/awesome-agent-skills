import httpx
import asyncio
from typing import AsyncGenerator
import logging

class LocalBrain:
    def __init__(self, model_name="llama3"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = model_name

    async def available(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://localhost:11434/api/tags", timeout=2)
                return resp.status_code == 200
        except Exception:
            return False

    async def chat_stream(self, message: str) -> AsyncGenerator[str, None]:
        if not await self.available():
            yield "Error: Ollama is not running or model not found. Local fallback unavailable."
            return

        payload = {"model": self.model, "prompt": message, "stream": True}
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream("POST", self.base_url, json=payload) as response:
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            yield data.get("response", "")
        except Exception as e:
            yield f"Error calling local model: {e}"

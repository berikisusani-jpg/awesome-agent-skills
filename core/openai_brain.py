from openai import AsyncOpenAI
import os
from config.settings import OPENAI_API_KEY

class OpenAIBrain:
    def __init__(self, model="gpt-4o"):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    async def chat_stream(self, message: str):
        if not OPENAI_API_KEY:
            yield "Error: OPENAI_API_KEY not set."
            return

        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error in OpenAIBrain: {str(e)}"

    async def available(self):
        return bool(OPENAI_API_KEY)

import google.generativeai as genai
import os
import asyncio
from typing import AsyncGenerator
from config.settings import OPENAI_API_KEY # Assuming we'll add GEMINI_API_KEY to settings

class GeminiBrain:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.chat = self.model.start_chat(history=[])

    async def chat_stream(self, message: str) -> AsyncGenerator[str, None]:
        response = self.chat.send_message(message, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def get_history(self):
        return self.chat.history

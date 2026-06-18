import anthropic
import asyncio
import logging
from typing import List, Dict, Any, AsyncGenerator
from config.settings import ANTHROPIC_API_KEY
from config.friday_identity import get_system_prompt

class FridayBrain:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        self.model = "claude-3-opus-20240229"
        self.logger = logging.getLogger("FridayBrain")
        self.conversation_history = []
        self.tools = [
            {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city name"}
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "search_web",
                "description": "Search the web for information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"}
                    },
                    "required": ["query"]
                }
            }
        ]

    async def chat_stream(self, message: str, user_name: str = "User") -> AsyncGenerator[str, None]:
        system_prompt = get_system_prompt(user_name)
        self.conversation_history.append({"role": "user", "content": message})

        try:
            async with self.client.messages.stream(
                model=self.model,
                max_tokens=2048,
                system=system_prompt,
                tools=self.tools,
                messages=self.conversation_history
            ) as stream:
                full_response = ""
                async for event in stream:
                    if event.type == "content_block_delta" and event.delta.type == "text_delta":
                        text = event.delta.text
                        full_response += text
                        yield text

                self.conversation_history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            self.logger.error(f"Error in FridayBrain: {e}")
            yield f"I'm sorry, I've hit a bit of a snag. Error: {str(e)}"

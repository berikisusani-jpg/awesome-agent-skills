import anthropic
import asyncio
import logging
from typing import List, Dict, Any, AsyncGenerator
from config.settings import ANTHROPIC_API_KEY, GEMINI_API_KEY
from config.friday_identity import get_system_prompt
from core.gemini_brain import GeminiBrain

class FridayBrain:
    def __init__(self):
        self.claude_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        self.gemini_brain = GeminiBrain(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
        self.claude_model = "claude-3-opus-20240229"
        self.logger = logging.getLogger("FridayBrain")
        self.conversation_history = []

    async def chat_stream(self, message: str, user_name: str = "User", force_gemini=False) -> AsyncGenerator[str, None]:
        # Intelligent routing
        if force_gemini or (len(message) > 5000 and self.gemini_brain):
            self.logger.info("Routing to Gemini for long context.")
            async for chunk in self.gemini_brain.chat_stream(message):
                yield chunk
            return

        system_prompt = get_system_prompt(user_name)
        self.conversation_history.append({"role": "user", "content": message})

        try:
            async with self.claude_client.messages.stream(
                model=self.claude_model,
                max_tokens=2048,
                system=system_prompt,
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
            if self.gemini_brain:
                self.logger.info("Falling back to Gemini.")
                async for chunk in self.gemini_brain.chat_stream(message):
                    yield chunk
            else:
                yield f"System error. Both brains offline. {str(e)}"

    def clear_context(self):
        self.conversation_history = []

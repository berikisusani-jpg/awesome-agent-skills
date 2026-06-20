import anthropic
import asyncio
import logging
import os
import json
from typing import List, Dict, Any, AsyncGenerator
from config.settings import ANTHROPIC_API_KEY, GEMINI_API_KEY
from config.friday_identity import get_system_prompt
from core.gemini_brain import GeminiBrain
from core.local_brain import LocalBrain
from integrations.registry import UniversalRegistry
from core.universal_connector import UniversalConnector

class FridayBrain:
    def __init__(self, provider=None):
        self.provider = provider or os.getenv("BRAIN_PROVIDER", "claude")
        self.claude_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        self.gemini_brain = GeminiBrain(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
        self.local_brain = LocalBrain()
        self.claude_model = "claude-3-5-sonnet-20240620"
        self.registry = UniversalRegistry()
        self.connector = UniversalConnector()
        self.logger = logging.getLogger("FridayBrain")
        self.conversation_history = []
        self.history_limit = 20
        self.tools = self._build_universal_tools()

    def _build_universal_tools(self):
        return [{
            "name": "access_universal_service",
            "description": "Access any integrated service to perform an action.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "The service name"},
                    "action": {"type": "string", "description": "The action to perform"},
                    "params": {"type": "object", "description": "Action parameters"}
                },
                "required": ["service", "action"]
            }
        }]

    def _manage_history(self):
        if len(self.conversation_history) > self.history_limit:
            self.conversation_history = self.conversation_history[-self.history_limit:]

    async def chat_stream(self, message: str, user_name: str = "User", force_provider=None) -> AsyncGenerator[str, None]:
        prov = force_provider or self.provider

        if prov == "ollama":
            async for chunk in self.local_brain.chat_stream(message):
                yield chunk
            return

        if (prov == "gemini" or len(message) > 5000) and self.gemini_brain:
            async for chunk in self.gemini_brain.chat_stream(message):
                yield chunk
            return

        if not ANTHROPIC_API_KEY:
            # Fallback to local if claude key missing
            if await self.local_brain.available():
                async for chunk in self.local_brain.chat_stream(message):
                    yield chunk
            else:
                yield "Error: No brain providers (Claude/Ollama) are available."
            return

        system_prompt = get_system_prompt(user_name)
        self.conversation_history.append({"role": "user", "content": message})
        self._manage_history()

        while True:
            full_response = ""
            tool_calls = []
            try:
                async with self.claude_client.messages.stream(
                    model=self.claude_model,
                    max_tokens=2048,
                    system=system_prompt,
                    tools=self.tools,
                    messages=self.conversation_history
                ) as stream:
                    async for event in stream:
                        if event.type == "content_block_delta" and event.delta.type == "text_delta":
                            text = event.delta.text
                            full_response += text
                            yield text

                    final_msg = await stream.get_final_message()
                    for content in final_msg.content:
                        if content.type == "tool_use":
                            tool_calls.append(content)

                if not tool_calls:
                    self.conversation_history.append({"role": "assistant", "content": full_response})
                    break

                self.conversation_history.append({"role": "assistant", "content": final_msg.content})
                for tool in tool_calls:
                    yield f"\n[System: Accessing {tool.input['service']}...]\n"
                    result = await self.connector.execute_action(tool.input["service"], tool.input["action"], tool.input.get("params", {}))
                    self.conversation_history.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool.id, "content": str(result)}]})
            except Exception as e:
                self.logger.error(f"Error in FridayBrain: {e}")
                # Last resort local fallback
                if await self.local_brain.available():
                    async for chunk in self.local_brain.chat_stream(message): yield chunk
                else:
                    yield f"System error: {str(e)}"
                break

    def clear_context(self):
        self.conversation_history = []

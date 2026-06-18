import asyncio
import logging
from core.brain import FridayBrain
from core.personality import FridayPersonality
from voice.wake_word import WakeWordDetector
from voice.listener import FridayListener
from voice.transcriber import FridayTranscriber
from voice.speaker import FridaySpeaker
from config.settings import LOG_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class FridayOrchestrator:
    def __init__(self):
        self.brain = FridayBrain()
        self.personality = FridayPersonality()
        self.speaker = FridaySpeaker()
        self.listener = FridayListener()
        self.transcriber = FridayTranscriber()
        # self.wake_word = WakeWordDetector() # Disabled for headless simulation

    async def run_once(self, text_input=None):
        if not text_input:
            print("System listening for command...")
            # Simulation of recording and transcribing
            # audio_path = self.listener.record_audio()
            # text_input = self.transcriber.transcribe(audio_path)
            text_input = "Hello Friday, what is the weather today?" # Simulated input

        print(f"User: {text_input}")

        full_response = ""
        async for chunk in self.brain.chat_stream(text_input):
            full_response += chunk

        self.speaker.speak(full_response)

    async def start(self):
        print("Friday is online and ready.")
        self.speaker.speak(self.personality.get_greeting())
        # Main loop would normally run here
        await self.run_once()

if __name__ == "__main__":
    orchestrator = FridayOrchestrator()
    asyncio.run(orchestrator.start())

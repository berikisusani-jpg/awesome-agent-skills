import asyncio
import logging
from core.brain import FridayBrain
from core.personality import FridayPersonality
from core.onboarding import AutoOnboarding
from voice.speaker import FridaySpeaker
from voice.listener import FridayListener
from config.settings import LOG_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class FridayOrchestrator:
    def __init__(self):
        self.brain = FridayBrain()
        self.personality = FridayPersonality()
        self.onboarding = AutoOnboarding()
        self.speaker = FridaySpeaker()
        self.listener = FridayListener()

    async def start(self):
        print("Friday is online and ready.")
        # Perform auto-onboarding
        welcome = self.onboarding.get_welcome_message()
        self.speaker.speak(welcome)

        # Simulated run loop
        # await self.run_once()

if __name__ == "__main__":
    orchestrator = FridayOrchestrator()
    asyncio.run(orchestrator.start())

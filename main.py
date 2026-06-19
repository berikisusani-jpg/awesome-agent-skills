import asyncio
import logging
from core.brain import FridayBrain
from core.personality import FridayPersonality
from core.ux_engine import CinematicUXEngine
from core.onboarding import AutoOnboarding
from voice.speaker import FridaySpeaker
from config.settings import LOG_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class FridayOrchestrator:
    def __init__(self):
        self.brain = FridayBrain()
        self.personality = FridayPersonality()
        self.speaker = FridaySpeaker()
        self.ux_engine = CinematicUXEngine(self.speaker)
        self.onboarding = AutoOnboarding()

    async def start(self):
        print("Friday: Nexus Cinematic Core Online.")
        # Perform auto-onboarding
        welcome = self.onboarding.get_welcome_message()

        # Trigger cinematic entry
        await self.ux_engine.trigger_transition("Startup")

        self.speaker.speak(welcome)
        print("Friday is ready for the future.")

if __name__ == "__main__":
    orchestrator = FridayOrchestrator()
    asyncio.run(orchestrator.start())

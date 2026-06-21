import asyncio
import logging
from config.logging_config import setup_logging
from core.brain import FridayBrain
from core.personality import FridayPersonality
from core.ux_engine import CinematicUXEngine
from core.onboarding import AutoOnboarding
from core.monologue import InnerMonologue
from core.evolution import EvolutionEngine
from core.sentinel import EthicalSentinel
from voice.speaker import FridaySpeaker
from voice.listener import FridayListener
from config.settings import LOG_FILE

class FridayOrchestrator:
    def __init__(self):
        self.brain = FridayBrain()
        self.personality = FridayPersonality()
        self.speaker = FridaySpeaker()
        self.ux_engine = CinematicUXEngine(self.speaker)
        self.onboarding = AutoOnboarding()
        self.evolution = EvolutionEngine(self.brain)
        self.sentinel = EthicalSentinel()

        from core.memory import FridayMemory
        self.memory = FridayMemory()
        self.monologue = InnerMonologue(self.memory)

    async def start(self):
        print("\n[FRIDAY ONLINE]")

        from core.scheduler import get_scheduler
        await get_scheduler().start()

        await self.ux_engine.trigger_transition("Startup")

        welcome = self.onboarding.get_welcome_message()
        reflection = self.monologue.reflect_on_interactions()

        self.speaker.speak(welcome)
        self.speaker.speak(reflection)

        print(f"System: {self.sentinel.get_sentinel_report()}")
        print("\n[FRIDAY IS WATCHING]")

if __name__ == "__main__":
    setup_logging()
    orchestrator = FridayOrchestrator()
    asyncio.run(orchestrator.start())

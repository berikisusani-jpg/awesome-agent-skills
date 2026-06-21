import asyncio
import logging
from core.brain import FridayBrain
from core.personality import FridayPersonality
from core.ux_engine import CinematicUXEngine
from core.onboarding import AutoOnboarding
from core.monologue import InnerMonologue
from core.evolution import EvolutionEngine
from core.recursive import RecursiveModificationProtocol
from core.sentinel import EthicalSentinel
from core.synthesis import LifeSynthesisEngine
from voice.speaker import FridaySpeaker
from voice.listener import FridayListener
from config.settings import LOG_FILE

class FridayApexOrchestrator:
    def __init__(self):
        self.brain = FridayBrain()
        self.personality = FridayPersonality()
        self.speaker = FridaySpeaker()
        self.ux_engine = CinematicUXEngine(self.speaker)
        self.onboarding = AutoOnboarding()
        self.evolution = EvolutionEngine(self.brain)
        self.recursive = RecursiveModificationProtocol(self.brain)
        self.sentinel = EthicalSentinel()
        self.synthesis = LifeSynthesisEngine(self.brain)

        from core.memory import FridayMemory
        self.memory = FridayMemory()
        self.monologue = InnerMonologue(self.memory)

    async def start(self):
        print("\n[SINGULARITY APEX ONLINE]")
        await self.ux_engine.trigger_transition("Singularity Ascent")

        welcome = self.onboarding.get_welcome_message()
        advice = await self.synthesis.generate_holistic_advice()
        reflection = self.monologue.reflect_on_interactions()

        self.speaker.speak(welcome)
        self.speaker.speak(reflection)
        self.speaker.speak(advice)

        print(f"System: {self.sentinel.get_sentinel_report()}")
        print("\n[FRIDAY IS WATCHING]")

if __name__ == "__main__":
    orchestrator = FridayApexOrchestrator()
    asyncio.run(orchestrator.start())

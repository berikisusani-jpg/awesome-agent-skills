import asyncio
import logging
import os
from core.brain import FridayBrain
from core.personality import FridayPersonality
from core.ux_engine import CinematicUXEngine
from core.onboarding import AutoOnboarding
from core.synthesis import LifeSynthesisEngine
from core.monologue import InnerMonologue
from core.sentinel import EthicalSentinel
from core.evolution import EvolutionEngine
from core.recursive import RecursiveModificationProtocol
from voice.speaker import FridaySpeaker
from voice.listener import FridayListener
from config.settings import LOG_FILE, FRIDAY_API_TOKEN

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class FridaySingularityOrchestrator:
    def __init__(self):
        self.brain = FridayBrain()
        self.personality = FridayPersonality()
        self.speaker = FridaySpeaker()
        self.ux_engine = CinematicUXEngine(self.speaker)
        self.onboarding = AutoOnboarding()

        # Singularity Modules
        self.synthesis = LifeSynthesisEngine(self.brain)
        self.sentinel = EthicalSentinel()
        self.evolution = EvolutionEngine(self.brain)
        self.recursive = RecursiveModificationProtocol(self.brain)

        from core.memory import FridayMemory
        self.memory = FridayMemory()
        self.monologue = InnerMonologue(self.memory)

    async def start(self):
        print("\n[SINGULARITY PROTOCOL INITIALIZED]")
        print("Friday: Nexus Cinematic Core Online.")

        # 1. Cinematic Startup
        await self.ux_engine.trigger_transition("Singularity Ascent")

        # 2. Environment Scan & Sentinel Check
        welcome = self.onboarding.get_welcome_message()
        sentinel_status = self.sentinel.get_sentinel_report()
        print(f"System: {sentinel_status}")

        # 3. Proactive Life Synthesis
        print("Friday: Synthesizing life-data for optimal trajectory...")
        advice = await self.synthesis.generate_holistic_advice()

        # 4. Self-Reflection (Inner Monologue)
        reflection = self.monologue.reflect_on_interactions()

        # 5. Delivery
        self.speaker.speak(welcome)
        self.speaker.speak(f"Sir, {reflection}")
        self.speaker.speak(f"Current Synthesis: {advice}")

        print("\n[FRIDAY IS AT APEX CAPACITY]")

if __name__ == "__main__":
    if not FRIDAY_API_TOKEN and os.getenv("ENV") != "dev":
        print("CRITICAL: FRIDAY_API_TOKEN not set. Security protocol requires a token.")

    orchestrator = FridaySingularityOrchestrator()
    asyncio.run(orchestrator.start())

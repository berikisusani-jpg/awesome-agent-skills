from integrations.weather import WeatherIntegration
from integrations.global_pulse import GlobalPulse

class LifeSynthesisEngine:
    def __init__(self, brain):
        self.brain = brain
        self.weather = WeatherIntegration()
        self.pulse = GlobalPulse()

    async def generate_holistic_advice(self):
        """
        Synthesizes multiple data streams into actionable personal advice.
        """
        w = await self.weather.execute("get_weather", {"location": "Lagos"})
        p = await self.pulse.get_world_status()

        prompt = f"""
        Synthesize a brief holistic advice for the user based on these inputs:
        - Weather: {w.get('message', 'Unknown')}
        - Global Pulse: {p.get('friday_insight', 'None')}
        - Tech News: {', '.join(p.get('tech_breakthroughs', []))}

        Be concise, witty, and helpful.
        """

        advice = ""
        async for chunk in self.brain.chat_stream(prompt):
            advice += chunk

        return advice

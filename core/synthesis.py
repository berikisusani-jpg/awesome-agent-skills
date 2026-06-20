from integrations.weather import WeatherIntegration
class LifeSynthesisEngine:
    def __init__(self, brain):
        self.brain = brain
        self.weather = WeatherIntegration()
    async def generate_holistic_advice(self):
        w = await self.weather.execute("get_weather", {"location": "Lagos"})
        return f"Weather: {w.get('message')}. Suggesting focus session."

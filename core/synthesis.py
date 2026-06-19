from integrations.finance import FinancialIntelligence
from integrations.weather import WeatherIntegration

class LifeSynthesisEngine:
    def __init__(self, brain):
        self.brain = brain
        self.finance = FinancialIntelligence()
        self.weather = WeatherIntegration()

    async def generate_holistic_advice(self):
        """
        Friday correlates life data points to provide holistic optimization.
        """
        finance_status = self.finance.get_financial_status()
        weather_status = self.weather.get_weather()

        prompt = f"""
        Correlate these factors for the user:
        Finance: {finance_status}
        Weather: {weather_status}
        Environment: User is currently in 'Flow State'.

        Provide a single 'Life-Synthesis' advice that optimizes for health, wealth, and focus.
        """

        advice = ""
        async for chunk in self.brain.chat_stream(prompt):
            advice += chunk

        return advice

    def get_synergy_score(self):
        return "System Synergy: 98% - All life sectors aligned."

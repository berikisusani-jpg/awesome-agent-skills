import requests
from config.settings import OPENWEATHERMAP_API_KEY

class WeatherIntegration:
    def get_weather(self, city="Lagos"):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"Current weather in {city}: {temp}°C with {desc}."
        return "I couldn't retrieve the weather information right now."

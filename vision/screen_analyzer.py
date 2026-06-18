from openai import OpenAI
from config.settings import OPENAI_API_KEY
import base64

class ScreenAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def analyze_screen(self, image_path):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is on the screen right now? Describe it as Friday, an AI assistant."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

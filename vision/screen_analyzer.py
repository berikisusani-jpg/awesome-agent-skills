from openai import OpenAI
from config.settings import OPENAI_API_KEY
import base64
import logging

class ScreenAnalyzer:
    def __init__(self):
        if not OPENAI_API_KEY:
            logging.warning("OPENAI_API_KEY not set. Screen analysis will fail.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def analyze_screen(self, image_path):
        if not OPENAI_API_KEY:
            return "Error: OpenAI API key not configured for vision analysis."

        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            response = self.client.chat.completions.create(
                model="gpt-4o", # Updated from gpt-4-vision-preview
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
        except Exception as e:
            logging.error(f"Screen analysis failed: {e}")
            return f"Error analyzing screen: {str(e)}"

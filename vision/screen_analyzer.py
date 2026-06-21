from openai import OpenAI
from config.settings import OPENAI_API_KEY
import base64
import logging
import json

class ScreenAnalyzer:
    def __init__(self):
        if not OPENAI_API_KEY:
            logging.warning("OPENAI_API_KEY not set. Screen analysis will fail.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def analyze_screen(self, image_path):
        if not OPENAI_API_KEY:
            return "Error: OpenAI API key not configured."
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": "Describe this screen as Friday AI."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def find_element(self, description, image_path):
        """
        FIXED: Vision-grounded element localization.
        Asks GPT-4o for coordinates of a described element.
        """
        if not OPENAI_API_KEY:
            return None
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            prompt = f"Find the center coordinates (x, y) for the element: '{description}'. Return ONLY JSON: {{\"x\": int, \"y\": int}}. If not found, return {{\"x\": -1, \"y\": -1}}."

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}],
                max_tokens=100,
                response_format={ "type": "json_object" }
            )
            coords = json.loads(response.choices[0].message.content)
            if coords.get("x") == -1: return None
            return coords
        except Exception as e:
            logging.error(f"Element localization failed: {e}")
            return None

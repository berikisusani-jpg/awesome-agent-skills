import pyttsx3
import logging
from elevenlabs.client import ElevenLabs
from config.settings import ELEVENLABS_API_KEY

class FridaySpeaker:
    def __init__(self, use_elevenlabs=True):
        self.use_elevenlabs = use_elevenlabs
        self.client = None
        if use_elevenlabs and ELEVENLABS_API_KEY:
            try:
                self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            except Exception as e:
                logging.error(f"Failed to initialize ElevenLabs client: {e}")
                self.use_elevenlabs = False
        else:
            self.use_elevenlabs = False

        self.engine = pyttsx3.init()

    def speak(self, text):
        print(f"Friday: {text}")
        if self.use_elevenlabs and self.client:
            try:
                audio = self.client.generate(
                    text=text,
                    voice="Nicole",
                    model="eleven_monolingual_v1"
                )
                from elevenlabs import play
                play(audio)
            except Exception as e:
                logging.error(f"ElevenLabs generation failed: {e}. Falling back to local TTS.")
                self.engine.say(text)
                self.engine.runAndWait()
        else:
            self.engine.say(text)
            self.engine.runAndWait()

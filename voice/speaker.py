import pyttsx3
from elevenlabs import generate, play, set_api_key
from config.settings import ELEVENLABS_API_KEY

class FridaySpeaker:
    def __init__(self, use_elevenlabs=False):
        self.use_elevenlabs = use_elevenlabs
        if use_elevenlabs:
            set_api_key(ELEVENLABS_API_KEY)
        self.engine = pyttsx3.init()

    def speak(self, text):
        print(f"Friday: {text}")
        if self.use_elevenlabs:
            try:
                audio = generate(text=text, voice="Nicole")
                play(audio)
            except Exception as e:
                print(f"ElevenLabs failed: {e}. Falling back to local TTS.")
                self.engine.say(text)
                self.engine.runAndWait()
        else:
            self.engine.say(text)
            self.engine.runAndWait()

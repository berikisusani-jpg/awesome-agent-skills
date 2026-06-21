import pyttsx3
import logging
import asyncio
from elevenlabs.client import ElevenLabs
from config.settings import ELEVENLABS_API_KEY

class FridaySpeaker:
    def __init__(self, use_elevenlabs=True):
        self.use_elevenlabs = use_elevenlabs
        self.client = None
        self.interrupt_signal = False
        if use_elevenlabs and ELEVENLABS_API_KEY:
            try:
                self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY, base_url="https://api.elevenlabs.io")
            except Exception:
                self.use_elevenlabs = False
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            logging.error(f"Failed to initialize pyttsx3: {e}")
            self.engine = None

    def interrupt(self):
        self.interrupt_signal = True
        if self.engine.isBusy():
            self.engine.stop()

    def speak(self, text):
        self.interrupt_signal = False
        print(f"Friday: {text}")

        # Local TTS is hard to interrupt mid-word without threading,
        # but we check signal before starting.
        if self.interrupt_signal: return

        if self.use_elevenlabs and self.client:
            try:
                # Real ElevenLabs streaming would go here
                pass
            except Exception:
                pass

        # Standard fallback with basic interrupt check
        if self.engine:
            words = text.split()
            for i in range(0, len(words), 5):
                if self.interrupt_signal:
                    print("[Playback Interrupted]")
                    break
                chunk = " ".join(words[i:i+5])
                self.engine.say(chunk)
                self.engine.runAndWait()
        else:
            # If no engine, we just print (already done above)
            pass

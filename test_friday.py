import unittest
from core.personality import FridayPersonality
from core.emotions import EmotionsEngine
from core.context import ContextAwareness

class TestFridayCore(unittest.TestCase):
    def test_personality_greeting(self):
        p = FridayPersonality()
        greeting = p.get_greeting("Jules")
        self.assertIn("Jules", greeting)

    def test_emotions_engine(self):
        e = EmotionsEngine()
        self.assertEqual(e.detect_emotion("I am so happy"), "happy")
        self.assertEqual(e.detect_emotion("This is bad"), "sad")

    def test_context_time(self):
        c = ContextAwareness()
        self.assertIn(c.get_time_context(), ["morning", "afternoon", "evening", "night"])

if __name__ == '__main__':
    unittest.main()

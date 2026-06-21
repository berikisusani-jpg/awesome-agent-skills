import unittest
import asyncio
import os
import pytest
from core.personality import FridayPersonality
from core.emotions import EmotionsEngine
from core.context import ContextAwareness
from integrations.crypto_tracker import CryptoTracker
from control.file_manager import FileManager

class TestFridayUltimate(unittest.IsolatedAsyncioTestCase):
    def test_personality_greeting(self):
        p = FridayPersonality()
        greeting = p.get_greeting("Jules")
        self.assertIn("Jules", greeting)

    def test_emotions_engine_negation(self):
        e = EmotionsEngine()
        self.assertEqual(e.detect_emotion("I am happy"), "happy")
        self.assertEqual(e.detect_emotion("I am NOT happy"), "sad")
        self.assertEqual(e.detect_emotion("I never said I was happy"), "sad")

    def test_crypto_price_interpolation(self):
        from unittest.mock import patch
        c = CryptoTracker()
        # Mocking requests for stability in CI
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {"bitcoin": {"usd": 65000}}
            res = c.get_price("bitcoin")
            self.assertIn("The current price of bitcoin is", res)
            self.assertIn("$65000", res)

    async def test_file_manager_safety(self):
        fm = FileManager()
        # Should fail as ledger will return False for wait_for_approval in default test env (timeout)
        res = await fm.create_file("test.txt", "content")
        self.assertIn("Error", res)

        # Should fail outside root
        with self.assertRaises(PermissionError):
            fm._safe_path("/etc/passwd")

    def test_context_time(self):
        c = ContextAwareness()
        self.assertIn(c.get_time_context(), ["morning", "afternoon", "evening", "night"])

    def test_sentinel_blocking(self):
        from core.ledger import ActionLedger
        import os
        os.environ["AUTONOMY_PROFILE"] = "POWER" # Power usually auto-approves
        ledger = ActionLedger()
        # Even in POWER mode, a "delete" action flagged by Sentinel should have risk_level="critical"
        # and thus be "pending" rather than "approved"
        aid = ledger.queue_action("Test", "delete_everything", {}, risk_level="low")
        self.assertEqual(ledger.pending_actions[aid]["status"], "pending")
        self.assertEqual(ledger.pending_actions[aid]["risk_level"], "critical")

if __name__ == '__main__':
    unittest.main()

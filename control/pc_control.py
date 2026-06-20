import pyautogui
import logging
import time
import datetime
import os
from config.settings import WORKSPACE_ROOT
from core.ledger import get_ledger

class PCControl:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.audit_log = "pc_control_audit.log"
        self.ledger = get_ledger()

    def _log_action(self, action, params):
        with open(self.audit_log, "a") as f:
            f.write(f"{time.ctime()} | Action: {action} | Params: {params}\n")

    def _get_screenshot_receipt(self):
        shot_path = os.path.join(WORKSPACE_ROOT, f"receipt_{int(time.time())}.png")
        pyautogui.screenshot(shot_path)
        return {
            "type": "screenshot",
            "data": shot_path,
            "timestamp": datetime.datetime.now().isoformat()
        }

    async def _gate(self, action, params):
        action_id = self.ledger.queue_action("PCControl", action, params)
        if await self.ledger.wait_for_approval(action_id):
            return True
        return False

    async def move_and_click(self, x, y):
        if not await self._gate("move_and_click", {"x": x, "y": y}):
            return {"status": "error", "message": "Action rejected by user."}

        self._log_action("move_and_click", {"x": x, "y": y})
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        return {
            "status": "success",
            "message": f"Clicked at ({x}, {y})",
            "receipt": self._get_screenshot_receipt()
        }

    async def type_text(self, text):
        if not await self._gate("type_text", {"text": text}):
            return {"status": "error", "message": "Action rejected by user."}

        self._log_action("type_text", {"text": text})
        pyautogui.write(text, interval=0.1)
        return {
            "status": "success",
            "message": f"Typed text: {text}",
            "receipt": self._get_screenshot_receipt()
        }

    async def press_shortcut(self, *keys):
        if not await self._gate("press_shortcut", {"keys": keys}):
            return {"status": "error", "message": "Action rejected by user."}

        self._log_action("press_shortcut", {"keys": keys})
        pyautogui.hotkey(*keys)
        return {
            "status": "success",
            "message": f"Pressed keys: {keys}",
            "receipt": self._get_screenshot_receipt()
        }

import pyautogui
import logging
import time
import datetime
import os
from config.settings import WORKSPACE_ROOT
from core.ledger import get_ledger
from vision.screen_reader import ScreenReader
from vision.screen_analyzer import ScreenAnalyzer

class PCControl:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.audit_log = "pc_control_audit.log"
        self.ledger = get_ledger()
        self.reader = ScreenReader()
        self.analyzer = ScreenAnalyzer()

    def _log_action(self, action, params):
        logging.getLogger("FridayControl").info({
            "component": "PCControl",
            "action": action,
            "params": params
        })

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
        return {"status": "success", "message": f"Clicked at ({x}, {y})", "receipt": self._get_screenshot_receipt()}

    async def click_described(self, description):
        """
        FIXED: Vision-grounded click.
        Locates an element by description and clicks it.
        """
        print(f"Friday: Locating '{description}' on screen...")
        shot_path = self.reader.capture_screen()
        coords = self.analyzer.find_element(description, shot_path)

        if not coords:
            return {"status": "error", "message": f"Could not find element: '{description}'"}

        return await self.move_and_click(coords['x'], coords['y'])

    async def type_text(self, text):
        if not await self._gate("type_text", {"text": text}):
            return {"status": "error", "message": "Action rejected by user."}
        self._log_action("type_text", {"text": text})
        pyautogui.write(text, interval=0.1)
        return {"status": "success", "message": f"Typed text: {text}", "receipt": self._get_screenshot_receipt()}

    async def press_shortcut(self, *keys):
        if not await self._gate("press_shortcut", {"keys": keys}):
            return {"status": "error", "message": "Action rejected by user."}
        self._log_action("press_shortcut", {"keys": keys})
        pyautogui.hotkey(*keys)
        return {"status": "success", "message": f"Pressed keys: {keys}", "receipt": self._get_screenshot_receipt()}

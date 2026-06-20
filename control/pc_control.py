import pyautogui
import logging
import time

class PCControl:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.audit_log = "pc_control_audit.log"

    def _log_action(self, action, params):
        with open(self.audit_log, "a") as f:
            f.write(f"{time.ctime()} | Action: {action} | Params: {params}\n")

    def move_and_click(self, x, y, confirm=False):
        if not confirm: return "Permission denied."
        self._log_action("move_and_click", {"x": x, "y": y})
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        return "Action completed."

    def type_text(self, text, confirm=False):
        if not confirm: return "Permission denied."
        self._log_action("type_text", {"text": text})
        pyautogui.write(text, interval=0.1)
        return "Text typed."

    def press_shortcut(self, *keys, confirm=False):
        # FIXED: Added confirmation gate
        if not confirm: return "Permission denied."
        self._log_action("press_shortcut", {"keys": keys})
        pyautogui.hotkey(*keys)
        return "Keys pressed."

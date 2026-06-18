import pyautogui

class PCControl:
    def __init__(self):
        pyautogui.FAILSAFE = True

    def move_and_click(self, x, y):
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()

    def type_text(self, text):
        pyautogui.write(text, interval=0.1)

    def press_shortcut(self, *keys):
        pyautogui.hotkey(*keys)

    def get_screen_size(self):
        return pyautogui.size()

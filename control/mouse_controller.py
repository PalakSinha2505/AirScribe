import pyautogui

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

        # Safety: prevent PyAutoGUI fail-safes from interrupting
        pyautogui.FAILSAFE = False

    def move(self, x, y, frame_w, frame_h):
        # Normalize safely
        if frame_w == 0 or frame_h == 0:
            return

        screen_x = (x / frame_w) * self.screen_w
        screen_y = (y / frame_h) * self.screen_h

        # Clamp values to screen bounds 
        screen_x = max(0, min(self.screen_w - 1, screen_x))
        screen_y = max(0, min(self.screen_h - 1, screen_y))

        pyautogui.moveTo(screen_x, screen_y, _pause=False)

    def click(self):
        pyautogui.click()
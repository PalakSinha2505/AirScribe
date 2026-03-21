import pyautogui

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

    def move(self, x, y, frame_w, frame_h):
        screen_x = self.screen_w * x / frame_w
        screen_y = self.screen_h * y / frame_h

        pyautogui.moveTo(screen_x, screen_y)

    def click(self):
        pyautogui.click()
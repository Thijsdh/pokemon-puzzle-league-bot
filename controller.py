from typing import Tuple
import pyautogui


class Controller:
    def __init__(self, pos=(0, 0)):
        self.pos = pos

    def move_to(self, target: Tuple[int, int]):
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]

        if dx > 0:
            pyautogui.press('right', presses=dx, interval=.1)

        if dx < 0:
            pyautogui.press('left', presses=-dx, interval=.1)

        if dy > 0:
            pyautogui.press('top', presses=dx, interval=.1)

        if dy < 0:
            pyautogui.press('down', presses=-dx, interval=.1)

        self.pos = target

    def swap(self):
        pyautogui.press('x')

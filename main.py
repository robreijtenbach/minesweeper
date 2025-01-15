import pyautogui
import win32gui
import win32con
from PIL import Image

from game import Game

def enum_windows():
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return windows

for w in enum_windows():
    if "Minesweeper" in w[1]:
        window_id = w[0]
        break
else:
    raise ValueError("Minesweeper not found.")

game = Game(window_id=window_id, version="minesweeperonline")


for i in range(3):
    game.move(i,i)
    game.update()
    game.print_board()


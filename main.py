import pyautogui
import win32gui
import win32con
from PIL import Image

COLOR_RED = (255,0,0,255) #find red letters

def enum_windows():
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return windows

#TODO instead of return x,y of red, use them to find x,y of topleft (maybe all corners)
def find_top_left_corner(image):
    """Finds top left corner of the board.

    Args: image: input screenshot
    
    Returns: coordinates of top left red pixel
    """

    pixels = image.load()

    w,h = image.size
    for y in range(h):
        for x in range(w):
            if pixels[x,y] == COLOR_RED:
                return (x,y)
    else:
        raise ValueError("Target color not found in the image.")

for w in enum_windows():
    if "Minesweeper" in w[1]:
        window_id = w[0]

# window to foreground
#win32gui.ShowWindow(window_id, win32con.SW_RESTORE) # seems to mess things up
win32gui.SetForegroundWindow(window_id)

# take screenshot
l,t,r,b = win32gui.GetWindowRect(window_id)
screenshot = pyautogui.screenshot(region=(l,t,r-l,b-t)).convert("RGBA")

screenshot.save("test.png")



print(screenshot.size)
screenshot.save("test.png")


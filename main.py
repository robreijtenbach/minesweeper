import pyautogui
import win32gui
import win32con
from PIL import Image

# TODO decide whether to crop to red letters and expand or grey sqaure #
BOX_COLOR = (198,198,198,255) #"c6c6c6"
BOX_COLOR = (128,128,128,255) #"c6c6c6"
#BOX_COLOR = (255,0,0,255) #find red letters (test)

def enum_windows():
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return windows

def trim_to_color_border(image, target_color):
    """
    Trims the image to the bounding box defined by the specified color (outline or border).
    
    Args:
        image (PIL.Image.Image): The input image.
        target_color (tuple): The target color as an (R, G, B) or (R, G, B, A) tuple.
        
    Returns:
        PIL.Image.Image: The cropped image.
    """
    # Convert the image to RGBA if necessary
    image = image.convert("RGBA")
    pixels = image.load()

    # Get image dimensions
    width, height = image.size

    # Initialize bounding box variables
    left, top, right, bottom = width, height, 0, 0

    # Iterate through all pixels to find the bounding box of the border color
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == target_color:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    # Check if the target color was found
    if left <= right and top <= bottom:
        # Crop the image to the bounding box
        return image.crop((left, top, right + 1, bottom + 1))
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
screenshot = pyautogui.screenshot(region=(l,t,r-l,b-t))

print(r-l, b-t)

screenshot = trim_to_color_border(screenshot, BOX_COLOR)

print(screenshot.size)
screenshot.save("test.png")


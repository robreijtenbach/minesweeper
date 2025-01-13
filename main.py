import pyautogui
import win32gui
import win32con
from PIL import Image

COLOR_RED = (255,0,0,255) # Red letters above board
COLOR_DARK_GRAY = (128,128,128,255) # Dark gray top left of board
COLOR_WHITE = (255,255,255,255) # White around board

def enum_windows():
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return windows

def get_board_info(image):
    """Finds info of the board.

    Args: image: input screenshot
    
    Returns: dictionary with board size in cells, board border locations and list of all cells (coords).
    """
    board_corners = {}

    pixels = image.load()
    
    width,height = image.size
    
    letter_coords = None
    for y in range(height):
        for x in range(width):
            if pixels[x,y] == COLOR_RED:
                letter_coords = (x,y)
    if not letter_coords:
        raise ValueError("Red letter color not found in the image.")

    # Find white top border
    x,y = letter_coords
    while y < height:
        y+=1
        # Find white pixel with 2 dark gray above it
        if pixels[x,y] == COLOR_WHITE and pixels[x,y-1] == COLOR_DARK_GRAY and pixels[x,y-2] == COLOR_DARK_GRAY:
            break
    else:
        raise ValueError("White border not found in the image.")

    # Find left corner side of board
    while x > 1:
        x -= 1
        if pixels[x-1,y] == COLOR_DARK_GRAY and pixels[x,y] == COLOR_WHITE:
            break
    else:
        raise ValueError("Dark gray left border not found.")

    # Top left corner found
    board_corners["top_left"] = (x,y)

    # Find top right corner and number of cells
    horizontal_cells = 0
    while x < width:
        x += 1
        if pixels[x,y] != COLOR_WHITE:
            horizontal_cells += 1
            if pixels[x+3,y-1] != COLOR_DARK_GRAY: # diagonal above should be dark gray, end found
                break
            else:
                x += 2
    else:
        raise ValueError("Right side of board not found.")

    # Top right corner found
    board_corners["top_right"] = (x,y)

    # Find bottom right corner and number of vertical cells
    vertical_cells = 1
    while y < height - 1:
        y += 1
        if pixels[x,y] != COLOR_DARK_GRAY:
            vertical_cells += 1

        if pixels[x,y+1] == COLOR_WHITE and pixels[x,y+2] == COLOR_WHITE:
            break
    else:
        raise ValueError("Bottom side of board not found")
    
    # Bottom right corner found
    board_corners["bottom_right"] = (x,y)
        
    # Deduce bottom left corner
    x = board_corners["top_left"][0]
    # Bottom left corner found
    board_corners["bottom_left"] = (x,y)
    
    board_info = {}
    board_info["size"] = (horizontal_cells, vertical_cells)
    board_info["left"] = board_corners["top_left"][0]
    board_info["top"] = board_corners["top_left"][1]
    board_info["right"] = board_corners["bottom_right"][0]
    board_info["bottom"] = board_corners["bottom_right"][1]

    # should be equal but might get rounding error
    x_step = (board_info["right"] - board_info["left"]) / horizontal_cells
    y_step = (board_info["bottom"] - board_info["top"]) / vertical_cells

    cells = []
    y = board_info["top"] + y_step/2
    for i in range(vertical_cells): # TODO check for off by one
        row = []
        x = board_info["left"] + x_step/2
        for j in range(horizontal_cells): # TODO check for off by one
            row.append((x,y))
            x += x_step
        cells.append(row)
        y += y_step
    
    board_info["cells"] = cells

    return board_info

for w in enum_windows():
    if "Minesweeper" in w[1]:
        window_id = w[0]
        break
else:
    raise ValueError("Minesweeper not found.")

# window to foreground
#win32gui.ShowWindow(window_id, win32con.SW_RESTORE) # seems to mess things up
win32gui.SetForegroundWindow(window_id)

# take screenshot
l,t,r,b = win32gui.GetWindowRect(window_id)
screenshot = pyautogui.screenshot(region=(l,t,r-l,b-t)).convert("RGBA")

print(l,t,r,b)

board_info = get_board_info(screenshot)

#x,y = board_info["cells"][0][0]
for x,y in board_info["cells"][0]:
    x+=l
    y+=t
    pyautogui.moveTo(x, y, 1, pyautogui.easeInBounce)
    #pyautogui.moveTo(x,y)
    pyautogui.click()
    #pyautogui.click(clicks=2, interval=0.25)

#for cc in board_info["corners"].values():
#    screenshot.putpixel(cc, COLOR_RED)

print(screenshot.size)
screenshot.save("test.png")


import win32gui
import pyautogui
import numpy as np

class MineSweeperOnlineAPI():
    COLOR_DICT = { ##TODO fill in placeholder colors
        (1,3,3,7) : 0,  # zero neighboring mines
        (1,3,3,7) : 1,  # one neighboring mine
        (1,3,3,7) : 2,  # etc.
        (1,3,3,7) : 3,
        (1,3,3,7) : 4,
        (1,3,3,7) : 5,
        (1,3,3,7) : 6,
        (1,3,3,7) : 7,
        (1,3,3,7) : 8,
        (1,3,3,7) : -1, #unknowm cell 
        (1,3,3,7) : -2  #flag cell
    }
    def get_board_info(window_id):
        """
        Finds info of the board.

        Args: image: input window_id
        
        Returns: dictionary with board size in cells, board border locations and list of all cells (coords).
        """
        # window to foreground
        #win32gui.ShowWindow(window_id, win32con.SW_RESTORE) # seems to mess things up

        # Color definitions        
        COLOR_RED = (255,0,0,255) # Red letters above board
        COLOR_DARK_GRAY = (128,128,128,255) # Dark gray top left of board
        COLOR_WHITE = (255,255,255,255) # White around board

        win32gui.SetForegroundWindow(window_id)

        # take screenshot
        left,top,right,bottom = win32gui.GetWindowRect(window_id)
        screenshot = pyautogui.screenshot(region=(left,top,right-left,bottom-top)).convert("RGBA")

        board_corners = {}

        pixels = screenshot.load()
        
        width,height = screenshot.size
        
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
                row.append((x+left,y+top))
                x += x_step
            cells.append(row)
            y += y_step
        
        board_info["cells"] = cells

        return board_info
    
    def __init__(self, window_id):
        self.window_id = window_id
        board_info = self.get_info(self.window_id)

        self.width, self.height = board_info["size"]
        self.cell_coords = board_info["cells"]
        self.window_dimensions = win32gui.GetWindowRect(window_id)
        self.board = np.full((self.width, self.height), -1)

    def get_update(self):
        left,top,right,bottom = win32gui.GetWindowRect(self.window_id)
        if self.window_dimensions != (left,top,right,bottom):
            raise ValueError("Window, position/size changed.")
        screenshot = pyautogui.screenshot(region=(left,top,right-left,bottom-top)).convert("RGBA")
        
        pixels = screenshot.load()

        for i in range(self.height):
            for j in range(self.width):
                cell = self.COLOR_DICT[pixels[i,j]]
                if self.board[i,j] == -1:
                    self.board[i,j] = cell
                elif self.board[i,j] != cell:
                    raise ValueError("Immutable board cell changed")
        
        return self.board # return updated board

    def do_move(self, x,y):
        left = self.window_dimensions[0]
        top = self.window_dimensions[1]
        x,y = self.cell_coords[x,y]
        
        pyautogui.moveTo(x+left, y+top, 1) # 1 for 1 second delay
        pyautogui.click()
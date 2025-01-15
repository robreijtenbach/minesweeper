import numpy as np

from minesweeper_online_api import MineSweeperOnlineAPI

class Game():   
    def __init__(self, window_id, version="minesweeperonline", solver=None):    
        if version == "minesweeperonline":
            self.api = MineSweeperOnlineAPI(window_id)
        else:
            raise ValueError(f"Version: {version} not implemented.")

        self.active = True
        self.won = False
        self.width = self.api.width 
        self.height = self.api.height
        self.board = np.full((self.width, self.height), -1)
        self.solver = solver

    def update(self):
        """Updates the cells of the board"""
        self.board = self.api.get_update()
        self.solver.update(self.board)

    def move(self):
        """Performs the next move"""
        x, y = self.solver.get_move()
        self.api.do_move(x,y)
        
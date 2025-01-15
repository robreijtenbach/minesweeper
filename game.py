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
        #self.solver.update(self.board) # TODO uncomment when solver implemented

    def move(self, x = None, y = None):
        """Performs the next move"""
        # TODO uncomment when solver implemented
        #if not x and not y:
        #    x, y = self.solver.get_move()
        print(x,y)
        self.api.do_move(x,y)

    def print_board(self):
        print(self.board)
        
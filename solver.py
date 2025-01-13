class Solver():
    """This class is going to perform the whole solving of Minesweeper. 
    Somewhere it should have some knowledge of the board and decide which cell
    to click.
    
    TODO Decide how all of this is going to work
        Have to think of how to approach selecting cells
            Which to look at first?
            How do humans do this?            
    TODO Implement what is decided
    """
    def __init__(self, board):
        self.board = board
        self.width = len(board[0])
        self.height = len(board)

    def update(self, board):
        self.board = board

    def getMove(self):
        """Decides best move, returns cell coordinates"""
        x, y = 0,0

        return x, y


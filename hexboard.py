from enum import Enum

SIZE = 4

class Tile(Enum):
    BLANK = 0
    RED   = 1
    GREEN = 2
    BLUE  = 3


class HexBoard():
    def __init__(self, size=SIZE):
        self.size = size
        self.grid = {(x,y,z) : Tile.BLANK   for x in range(-self.size+1, self.size)
                                            for y in range(-self.size+1, self.size)
                                            for z in range(-self.size+1, self.size) if sum((x,y,z))==0}

if (__name__ == "__main__"):
    board = HexBoard()
    for coord in sorted(board.grid.keys()):
        print(coord)


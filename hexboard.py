from enum import Enum
import itertools

SIZE = 3

class Tile(Enum):
    BLANK = '0'
    RED   = 'R'
    GREEN = 'G'
    BLUE  = 'B'


class HexBoard():
    def __init__(self, size=SIZE, start_config=True):
        self.size = size
        self.grid = {coord : Tile.BLANK for coord in self.iter_coords()}
        if (start_config): self.reset_pieces()

    def reset_pieces(self):
        for i in range(0,self.size+1):
            # (-self.size) + i + j = 0
            j = self.size - i
            self.grid[-self.size, i, j] = Tile.RED
            self.grid[i, -self.size, j] = Tile.GREEN
            self.grid[i, j, -self.size] = Tile.BLUE

    def iter_coords(self):
        for x in range(-self.size, self.size+1):
            low = max(- x - self.size, -self.size)
            hih = min(- x + self.size,  self.size)
            for y in range(low, hih+1):
                yield (y,x,-x-y)

    def __iter__(self):
        for coord in self.iter_coords():
            yield self.grid[coord]

    def iter_rows(self):
        for x in range(-self.size, self.size+1):
            low = max(- x - self.size, -self.size)
            hih = min(- x + self.size,  self.size)
            yield (self.grid[y,x,-x-y] for y in range(low, hih+1))

    def __repr__(self):
        result = ''
        for i, row in enumerate(self.iter_rows()):
            result += '\n' + ' '*abs(i-board.size) + ' '.join(str(tile.value) for tile in row)
        return result

if (__name__ == "__main__"):
    board = HexBoard()

    print(board)

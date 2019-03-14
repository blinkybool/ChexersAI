from enum import Enum
import itertools
from collections import defaultdict

PRINT_COORDS = True

SIZE = 3

class Tile(Enum):
    BLANK, RED, GREEN, BLUE = '0','R','G','B'


class HexBoard():
    def __init__(self, size=SIZE, start_config=True):
        self.size = size
        self.grid = defaultdict(lambda: Tile.BLANK)
        if start_config: self.reset_pieces()

    def iter_coords(self):
        for x in range(-self.size, self.size+1):
            low = max(- x - self.size, -self.size)
            hih = min(- x + self.size,  self.size)
            for y in range(low, hih+1):
                yield (x,y,-x-y)

    def __iter__(self):
        for coord in self.iter_coords():
            yield self.grid[coord]

    def iter_rows(self):
        for x in range(-self.size, self.size+1):
            low = max(- x - self.size, -self.size)
            hih = min(- x + self.size,  self.size)
            yield (self.grid[x,y,-x-y] for y in range(low, hih+1))

    def reset_pieces(self):
        i = -self.size
        for j in range(self.size+1):
            # i + j + k = 0
            k = - (i+j)

            self.grid[i,j,k] = Tile.GREEN
            self.grid[j,i,k] = Tile.RED
            self.grid[j,k,i] = Tile.BLUE

    def __repr__(self):
        result = ''
        # for i, row in enumerate(self.iter_rows()):
        #     result += '\n' + ' '*abs(i-board.size) + ' '.join(str(tile) for tile in row)
        # return result

        return '\n'.join(' '*abs(i-board.size) + ' '.join(str(tile) for tile in row) for i, row in enumerate(self.iter_rows()))
        

if (__name__ == "__main__"):
    board = HexBoard()
    print(board)

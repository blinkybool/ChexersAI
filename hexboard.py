from enum import Enum
import itertools

PRINT_COORDS = True

SIZE = 3

class Tile(Enum):
    BLANK, RED, GREEN, BLUE = range(4)


class HexBoard():
    def __init__(self, size=SIZE):
        self.size = size
        self.grid = {coord : Tile.BLANK for coord in self.iter_coords()}

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

    def __repr__(self):
        result = ''
        for i, row in enumerate(self.iter_rows()):
            result += '\n' + ' '*abs(i-board.size) + ' '.join(str(tile) for tile in row)
        return result

if (__name__ == "__main__"):
    board = HexBoard()
    print(board)

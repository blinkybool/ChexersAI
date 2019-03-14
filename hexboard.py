from enum import Enum
import itertools
from collections import defaultdict

SIZE = 3

BLANK = '0'
RED   = 'R'
GREEN = 'G'
BLUE  = 'B'

class HexBoard():



    def __init__(self, size=SIZE, start_config=True):
        self.size = size
        self.grid = defaultdict(lambda: BLANK)
        if start_config: self.reset_pieces()

    def iter_coords(self):
        for x in range(-self.size, self.size+1):
            # y = -x -z
            # -x-size <= y <= -x + size
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
        for j in range(0,self.size+1):
            # i + j + k = 0
            k = - (i+j)

            self.grid[i,j,k] = GREEN
            self.grid[j,i,k] = RED
            self.grid[j,k,i] = BLUE

    def is_val_move(curr_coord, new_coord):
        if  new_coord in neighbours(curr_coord) and grid[new_coord]:
            pass
            
        


    def move():
        pass


    def valid_coord(self, coord):
        return -self.size <= min(coord) and max(coord) <= self.size and sum(coord)==0

    def neighbours(self, coord):
        x,y,z = coord

        if self.valid_coord((x+1,y-1,z)): yield (x+1,y-1,z)
        if self.valid_coord((x-1,y+1,z)): yield (x-1,y+1,z)
        if self.valid_coord((x+1,y,z-1)): yield (x+1,y,z-1)
        if self.valid_coord((x-1,y,z+1)): yield (x-1,y,z+1)
        if self.valid_coord((x,y+1,z-1)): yield (x,y+1,z-1)
        if self.valid_coord((x,y-1,z+1)): yield (x,y-1,z+1)

    def jump_neighbours(self, coord):
        x,y,z = coord

        if self.valid_coord((x+2,y-2,z)): yield (x+2,y-2,z)
        if self.valid_coord((x-2,y+2,z)): yield (x-2,y+2,z)
        if self.valid_coord((x+2,y,z-2)): yield (x+2,y,z-2)
        if self.valid_coord((x-2,y,z+2)): yield (x-2,y,z+2)
        if self.valid_coord((x,y+2,z-2)): yield (x,y+2,z-2)
        if self.valid_coord((x,y-2,z+2)): yield (x,y-2,z+2)

        
        
        


    def __repr__(self):
        return '\n'.join(' '*abs(i-board.size) + ' '.join(str(tile) for tile in row) for i, row in enumerate(self.iter_rows()))
        

if (__name__ == "__main__"):
    board = HexBoard()
    print(board)
    # blah

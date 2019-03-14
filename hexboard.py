from enum import Enum
import itertools
from collections import defaultdict

SIZE = 3
NUM_AXES = 3
BLANK_TILE_CHAR = '0'

class Tile(Enum):
    BLANK = 0
    RED   = 1
    GREEN = 2
    BLUE  = 3

    def __repr__(self):
        return self.name[0] if self.value else BLANK_TILE_CHAR

    def __str__(self):
        return self.__repr__()


class HexBoard():

    def __init__(self, size=SIZE, start_config=True):
        self.size = size
        self.grid = defaultdict(lambda: Tile.BLANK)
        if start_config: self.reset_pieces()

    def reset_pieces(self):
        i = -self.size
        for j in range(0,self.size+1):
            # i + j + k = 0
            k = - (i+j)

            self.grid[i,j,k] = Tile.GREEN
            self.grid[j,i,k] = Tile.RED
            self.grid[j,k,i] = Tile.BLUE
    
    def iter_coords(self):
        for x in range(-self.size, self.size+1):
            # y = -x -z
            # -x-size <= y <= -x + size
            low = max(- x - self.size, -self.size)
            hih = min(- x + self.size,  self.size)
            for y in range(low, hih+1):
                yield (x,y,-x-y)
    
    def is_valid_coord(self, coord):
        return -self.size  <= min(coord) and \
                max(coord) <= self.size and  \
                sum(coord) == 0
    
    # tile iterators

    def __iter__(self):
        for coord in self.iter_coords():
            yield self.grid[coord]

    def iter_rows(self):
        for x in range(-self.size, self.size+1):
            low = max(- x - self.size, -self.size)
            hih = min(- x + self.size,  self.size)
            yield (self.grid[x,y,-x-y] for y in range(low, hih+1))

    def neighbours(self, coord):
        x,y,z = coord

        if self.is_valid_coord((x+1,y-1,z)): yield (x+1,y-1,z)
        if self.is_valid_coord((x-1,y+1,z)): yield (x-1,y+1,z)
        if self.is_valid_coord((x+1,y,z-1)): yield (x+1,y,z-1)
        if self.is_valid_coord((x-1,y,z+1)): yield (x-1,y,z+1)
        if self.is_valid_coord((x,y+1,z-1)): yield (x,y+1,z-1)
        if self.is_valid_coord((x,y-1,z+1)): yield (x,y-1,z+1)

    def jump_neighbours(self, coord):
        x,y,z = coord

        if self.is_valid_coord((x+2,y-2,z)): yield (x+2,y-2,z)
        if self.is_valid_coord((x-2,y+2,z)): yield (x-2,y+2,z)
        if self.is_valid_coord((x+2,y,z-2)): yield (x+2,y,z-2)
        if self.is_valid_coord((x-2,y,z+2)): yield (x-2,y,z+2)
        if self.is_valid_coord((x,y+2,z-2)): yield (x,y+2,z-2)
        if self.is_valid_coord((x,y-2,z+2)): yield (x,y-2,z+2)
    
    # action qualifiers

    # ASSUMES COORDS ARE VALID
    def are_adj(self, coord1, coord2):
        u,v,w = coord1
        x,y,z = coord2
        
        if u==x:
            return abs(w-z) == 1
        elif v==y:
            return abs(w-z) == 1
        elif w==z:
            return abs(u-x) == 1
        else:
            return False

    # ASSUMES COORDS ARE VALID
    def are_jump_adj(self, coord1, coord2):
        u,v,w = coord1
        x,y,z = coord2
        
        if u==x:
            return abs(w-z) == 2
        elif v==y:
            return abs(w-z) == 2
        elif w==z:
            return abs(u-x) == 2
        else:
            return False
    

    def is_valid_move(self, source, dest, colour=None):
        if not (self.is_valid_coord(source) and self.is_valid_coord(dest)):
            return False

        if colour==None:
            colour = self.grid[source]

        if colour == Tile.BLANK:
            return False
        
        if self.grid[source]!=source or self.grid[dest]!=Tile.BLANK:
            return False

        return self.are_adj(source, dest)

    def is_valid_jump(self, source, dest, colour):
        if not (self.is_valid_coord(source) and self.is_valid_coord(dest)):
            return False
        
        if colour==None:
            colour = self.grid[source]

        if colour == Tile.BLANK:
            return False
        
        if self.grid[source]!=source or not self.are_jump_adj(source, dest):
            return False

        between_coord = tuple(sum(i,j)/self.size for i,j in zip(source, dest))

        return self.grid[between_coord] not in {Tile.BLANK, colour}

    # actions

    def move(self, coord, axes, dir):
        assert(abs(dir)==1)

        x,y,z = coord

        if axes == 'x':
            new_coord = (x, y+dir, z-dir)
        elif axes == 'y':
            new_coord = (x+dir, y, z-dir)
        elif axes == 'z':
            new_coord = (x+dir, y-dir, z)
        else:
            assert(0)

        if self.is_valid_move(coord, new_coord):
            self.grid[coord], self.grid[new_coord] == Tile.BLANK, self.grid[coord]
        else:
            assert(0)

    def jump(self, coord, axes, dir):
        assert(abs(dir)==2)

        x,y,z = coord

        if axes == 'x':
            new_coord = (x, y+dir, z-dir)
        elif axes == 'y':
            new_coord = (x+dir, y, z-dir)
        elif axes == 'z':
            new_coord = (x+dir, y-dir, z)
        else:
            assert(0)

        if self.is_valid_jump(coord, new_coord):
            between_coord = tuple(sum(i,j)/self.size for i,j in zip(coord, new_coord))

            self.grid[new_coord] = self.grid[between_coord] = self.grid[coord]

            self.grid[coord] = Tile.BLANK
        else:
            assert(0)

    # other dunder methods

    def __repr__(self):
        return '\n'.join(' '*abs(i-board.size) + ' '.join(str(tile) for tile in row) for i, row in enumerate(self.iter_rows()))

    def __str__(self):
        return self.__repr__()

if __name__ == "__main__":
    board = HexBoard()
    print(board.grid[-3,1,2])
    board.move((-3,1,2), 'z', -1)
    print(board)

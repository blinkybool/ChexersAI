import json
from enum import Enum, unique
from math import ceil
import numpy as np

RADIUS = 3

@unique
class Colour(Enum):
    BLANK = 0
    BLOCK = 1
    RED = 2
    GREEN = 3
    BLUE = 4

    def is_player_colour(self):
        return self.value > Colour.BLOCK.value

    def __call__(self, colour_str):
        return {"red":Colour.RED,
                "green": Colour.GREEN,
                "blue": Colour.BLUE}[colour_str.lower()]
    
    def __str__(self):
        return [" ", "R", "G", "B", "X"][self.value]


class Tile():
    
    def __init__(self, colour, heuristic=None):
        self.colour = colour
        self.heuristic = heuristic

    def __str__(self):
        return self.colour.__str__()




class BoardState():
    
    def __init__(self, pieces=set()):
        self.pieces = set(pieces)

    def __hash__(self):
        pass
    
    def get_heu(self):
        return sum(map(self.tile_heu, self.pieces))

    def tile_heu(self, coord, player):
            '''
            takes a hexboard and assigns a heuristic value to each tile (dependent on player)
            VERSION 1: number of jumps from end tiles (H = ceiling(D/2))
            '''
            
            return self.goal_jump_dist(coord, player)


    def goal_jump_dist(self, coord, player):
        '''
        finds the minimum number of steps taken to reach a player's goal tile, assuming jumps on every possible turn
        '''
        return ceil(self.goal_dist(coord, player)/2)


    def goal_dist(self, coord, player):
        '''
        finds the distance from a given point to the player's goal tiles
        '''

        return {Colour.RED: RADIUS - coord[0],
                Colour.GREEN: RADIUS - coord[1],
                Colour.BLUE: RADIUS - -sum(coord)}[player]







'''
Board state from the perspective of one player
'''
class HexBoard():

    def __init__(self, start_config_file, radius=RADIUS):
        self.radius = radius
        self.tiles = dict()
        
        # initialise all blank tiles
        for coord in self.iter_coords():
            self[coord] = Tile(Colour.BLANK, self.goal_jump_dist(coord))

        # extract data from json
        with open(start_config_file) as start_config_json:
            start_config = json.load(start_config_json)
            self.player = Colour(start_config["colour"])
            self.pieces = start_config["pieces"]
            self.blocks = start_config["blocks"]
        
        # set all the piece positions
        for coord in self.pieces:
            self[coord].colour = self.player

        # set all the block positions
        for coord in self.blocks:
            self[coord].colour = Colour.BLOCK
        

    def __getitem__(self, key):
        return self.tiles.__getitem__(key)

    def __setitem__(self, key, item):
        return self.tiles.__setitem__(key, item)

    def iter_coords(self):
        ran = range(-self.radius, self.radius + 1)
        return ((q,r) for q in ran for r in ran if -q-r in ran)

    def do_heu(self, coord):
        '''
        takes a hexboard and assigns a heuristic value to each tile (dependent on player)
        VERSION 1: number of jumps from end tiles (H = ceiling(D/2))
        '''
        
        return self.goal_jump_dist(coord)


    def goal_jump_dist(self, coord):
        '''
        finds the minimum number of steps taken to reach a player's goal tile, assuming jumps on every possible turn
        '''
        return ceil(self.goal_dist(coord)/2)


    def goal_dist(self, coord):
        '''
        finds the distance from a given point to the player's goal tiles
        '''

        return {Colour.RED: self.radius - coord[0],
                Colour.GREEN: self.radius - coord[1],
                Colour.BLUE: self.radius - -sum(coord)}[self.player]



    def print_it(self, debug=False):
        """
        Helper function to print a drawing of a hexagonal board's contents.
        
        Arguments:

        * `board_dict` -- dictionary with tuples for keys and anything printable
        for values. The tuple keys are interpreted as hexagonal coordinates (using 
        the axial coordinate system outlined in the project specification) and the 
        values are formatted as strings and placed in the drawing at the corres- 
        ponding location (only the first 5 characters of each string are used, to 
        keep the drawings small). Coordinates with missing values are left blank.

        Keyword arguments:

        * `message` -- an optional message to include on the first line of the 
        drawing (above the board) -- default `""` (resulting in a blank message).
        * `debug` -- for a larger board drawing that includes the coordinates 
        inside each hex, set this to `True` -- default `False`.
        * Or, any other keyword arguments! They will be forwarded to `print()`.
        """

        # Set up the board template:
        if not debug:
            # Use the normal board template (smaller, not showing coordinates)
            template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
        else:
            # Use the debug board template (larger, showing coordinates)
            template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

        # prepare the provided board contents as strings, formatted to size.
        ran = range(-3, +3+1)
        cells = []
        for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
            if qr in self:
                cell = str(self[qr]).center(5)
            else:
                cell = "     " # 5 spaces will fill a cell
            cells.append(cell)

        # fill in the template to create the board drawing, then print!
        board = template.format("", *cells)
        print(board)


def main():
    pass


if __name__ == '__main__':
    main()

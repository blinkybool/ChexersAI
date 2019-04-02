import json
from enum import Enum, unique
from math import ceil

RADIUS = 3


@unique
class Colour(Enum):
    BLANK = 0
    BLOCK = 1
    RED = 2
    GREEN = 3
    BLUE = 4

    @classmethod
    def parse(cls, colour):
        return {"red": cls.RED,
                "green": cls.GREEN,
                "blue": cls.BLUE}[colour.lower()]

    def is_player_colour(self):
        return self.value > Colour.BLOCK.value

    def __str__(self):
        return {0: " ", 1: "X", 2: "R", 3: "G", 4: "B"}[self.value]


class Tile():

    def __init__(self, colour, heuristic=None):
        self.colour = colour
        self.heuristic = heuristic

    def __str__(self):
        return self.colour.__str__()


class PieceState():

    def __init__(self, pieces=tuple()):
        self.pieces = tuple(sorted(pieces))

    # def __hash__(self):
    #     self.pieces.__hash__()

    def __getitem__(self, key):
        return self.pieces.__getitem__(key)

    def __iter__(self):
        return self.pieces.__iter__()

    def get_heu(self, board):
        return sum(map(board.tile_heu, self.pieces))

    def __bool__(self):
        return bool(self.pieces)

    def __repr__(self):
        return self.pieces.__repr__()

    def __eq__(self, other):
        return type(self)==type(other) and self.pieces == other.pieces


'''
Board state from the perspective of one player
'''


class HexBoard():

    def __init__(self, start_config_file='', radius=RADIUS):
        self.radius = radius
        self.tiles = dict()
        self.seen_states = set()
        self.start_state = PieceState()

        # extract data from json
        with open(start_config_file) as start_config_json:
            start_config = json.load(start_config_json)
            self.player = Colour.parse(start_config["colour"])
            self.start_state = PieceState(tuple(map(tuple, start_config["pieces"])))
            self.blocks = tuple(map(tuple, start_config["blocks"]))

        # initialise all blank tiles
        for coord in self.iter_coords():
            self[coord] = Tile(Colour.BLANK, self.goal_jump_dist(coord))

        # set all the block positions
        for coord in self.blocks:
            self[coord].colour = Colour.BLOCK

    def __getitem__(self, key):
        return self.tiles.__getitem__(key)

    def __setitem__(self, key, item):
        return self.tiles.__setitem__(key, item)

    def iter_coords(self):
        ran = range(-self.radius, self.radius + 1)
        return ((q, r) for q in ran for r in ran if -q-r in ran)

    def is_valid_coord(self, coord):
        return -RADIUS <= min(coord) and max(coord) <= RADIUS and abs(sum(coord)) <= RADIUS

    def tile_heu(self, coord):
        '''
        takes a hexboard and assigns a heuristic value to each tile (dependent on player)
        VERSION 1: number of jumps from end tiles (H = ceiling(D/2))
        '''

        return self.goal_jump_dist(coord)

    def goal_jump_dist(self, coord):
        '''
        finds the minimum number of steps taken to reach a player's goal tile, assuming jumps on every possible turn
        '''
        return self.goal_dist(coord)/2

    def goal_dist(self, coord):
        '''
        finds the distance from a given point to the player's goal tiles
        '''

        return {Colour.RED:   RADIUS - coord[0],
                Colour.GREEN: RADIUS - coord[1],
                Colour.BLUE:  RADIUS - -sum(coord)}[self.player]

    def can_exit(self, piececoord):
        x, y = piececoord
        if self.player==Colour.RED:
            return x==RADIUS
        if self.player==Colour.GREEN:
            return y==RADIUS
        if self.player==Colour.BLUE:
            return sum(x, y)==-RADIUS
        else:
            print("aaaaaaaaaaaahhhh")
            exit()
        # return {Colour.RED: bool(x==RADIUS), Colour.GREEN: bool(y == RADIUS), Colour.BLUE: bool(sum(x, y)==-RADIUS)}[self.player]

    def occupied(self, coord, state):
        return coord in state or self[coord].colour == Colour.BLOCK

    def move_choices(self, piececoord, state):
        x,y = piececoord

        coords = (
                ((x-1, y), (x-2, y)),
                ((x-1, y+1), (x-2, y+2)),
                ((x, y-1), (x, y-2)),
                ((x, y+1), (x, y+2)),
                ((x+1, y-1), (x+2, y-2)),
                ((x+1, y), (x+2, y)),
            )

        for movecoord, jumpcoord in coords:
            if self.is_valid_coord(movecoord):
                if self.occupied(movecoord,state):
                    if self.is_valid_coord(jumpcoord) and not self.occupied(jumpcoord,state):
                        yield (jumpcoord,"JUMP")
                else:
                    yield (movecoord, "MOVE")
        

    def new_states(self, state):
        '''
        takes a PieceState, and yields 2-tuples containing one of the new possible PieceStates
        and the would-be output for the move to that state
        '''
        for i, piece in enumerate(state):
            for action in self.move_choices(piece, state):
                new_pieces = list(state.pieces)
                move = f"{action[1]} from {piece} to {action[0]}."
                new_pieces[i] = action[0]
                yield (PieceState(tuple(new_pieces)), move)

            if self.can_exit(piece):
                move = f"EXIT from {new_pieces.pop(i)}."
                yield (PieceState(tuple(new_pieces)), move)

    def format_with_state(self, piecestate=None, debug=False):
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

        if piecestate == None:
            piecestate = self.start_state

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
        for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
            cell = Colour.BLANK
            if qr in self.blocks:
                cell = Colour.BLOCK
            elif qr in piecestate:
                cell = self.player

            cells.append(str(cell).center(5))

        # fill in the template to create the board drawing, then print!
        return template.format("", *cells)

    def print_path(self, piecestates):
        for state in piecestates:
            print(self.format_with_state(piecestate=state))


def main():
    hb = HexBoard(start_config_file="test.json")

    print(hb.format_with_state())


if __name__ == '__main__':
    main()

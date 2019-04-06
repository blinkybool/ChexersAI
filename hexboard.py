from enum import Enum, unique
from sys import stderr

RADIUS = 3

@unique
class Tile(Enum):
    BLANK = 0
    BLOCK = 1
    RED = 2
    GREEN = 3
    BLUE = 4

    @classmethod
    def parse_colour(cls, colour):
        return {"red": cls.RED,
                "green": cls.GREEN,
                "blue": cls.BLUE}[colour.lower()]

    def is_player_colour(self):
        return self.value > Tile.BLOCK.value

    def __str__(self):
        return {0: " ", 1: "X", 2: "R", 3: "G", 4: "B"}[self.value]

'''
Board state from the perspective of one player
'''

class HexBoard():

    def __init__(self, config, radius=RADIUS):
        self.radius = radius
        self.tiles = {}
        self.seenstates = {}
        self.currentstate = tuple()

        self.player = Tile.parse_colour(config["colour"])
        self.currentstate = tuple(tuple(sorted(map(tuple, config["pieces"]))))

        # initialise all blank tiles
        for coord in self.iter_coords():
            self[coord] = Tile.BLANK

        # set all the block positions
        for coord in config["blocks"]:
            self[tuple(coord)] = Tile.BLOCK

    def __getitem__(self, key):
        return self.tiles.__getitem__(key)

    def __setitem__(self, key, item):
        return self.tiles.__setitem__(key, item)

    def iter_coords(self):
        ran = range(-self.radius, self.radius + 1)
        return ((q, r) for q in ran for r in ran if -q-r in ran)

    def is_valid_coord(self, coord):
        return -RADIUS <= min(coord) and max(coord) <= RADIUS and abs(sum(coord)) <= RADIUS

    def state_heu(self, state=None):
        if state == None: state = self.currentstate
        return sum(map(self.tile_heu, state))

    def tile_heu(self, coord):
        '''
        takes a hexboard and assigns a heuristic value to each tile (dependent on player)
        VERSION 1: number of jumps from end tiles (H = ceiling(D/2))
        '''

        return self.goal_jump_dist(coord)+1
        # return 0

    def goal_jump_dist(self, coord):
        '''
        finds the minimum number of steps taken to reach a player's goal tile, assuming jumps on every possible turn
        '''
        return self.goal_dist(coord)/2

    def goal_dist(self, coord):
        '''
        finds the distance from a given point to the player's goal tiles
        '''

        return {Tile.RED:   self.radius - coord[0],
                Tile.GREEN: self.radius - coord[1],
                Tile.BLUE:  self.radius - -sum(coord)}[self.player]

    def can_exit(self, piececoord):
        x, y = piececoord
        if self.player==Tile.RED:
            return x==RADIUS
        if self.player==Tile.GREEN:
            return y==RADIUS
        if self.player==Tile.BLUE:
            return x+y==-RADIUS
        else:
            print("aaaaaaaaaaaahhhh", file=stderr)
            exit()
        # return {Tile.RED: bool(x==RADIUS), Tile.GREEN: bool(y == RADIUS), Tile.BLUE: bool(sum(x, y)==-RADIUS)}[self.player]

    def occupied(self, coord, state):
        return coord in state or self[coord] == Tile.BLOCK

    def movejumpchoices(self, piececoord, state):
        q,r = piececoord

        movecoords = \
            (
                ( q ,r-1),(q+1,r-1)     ,
                      #.-'-.#
            (q-1, r )    ,    (q+1, r ) ,
                      #-._.-#  
                (q-1,r+1),( q ,r+1)     ,
            )

        jumpcoords = \
            (
                ( q ,r-2),(q+2,r-2)     ,
                      #.-'-.#
            (q-2, r )    ,    (q+2, r ) ,
                      #-._.-#  
                (q-2,r+2),( q ,r+2)     ,
            )

        for movecoord, jumpcoord in zip(movecoords, jumpcoords):
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
        for acting_piece in state:
            for new_pos, action in self.movejumpchoices(acting_piece, state):

                # replace acting_piece with its new position
                new_state = tuple(sorted(piece if piece!=acting_piece else new_pos for piece in state))

                # right move string
                move_action = f"{action} from {acting_piece} to {new_pos}."

                yield (new_state, move_action)

            if self.can_exit(acting_piece):
                new_state = tuple(piece for piece in state if piece!=acting_piece)
                exit_action = f"EXIT from {acting_piece}."
                yield (tuple(sorted(new_state)), exit_action)

    def format_with_state(self, state=None, debug=False, message=''):
        """
        Helper function to print a drawing of a hexagonal board's contents.
        """

        if state == None: state = self.currentstate

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
        for coord in [(q, r) for q in ran for r in ran if -q-r in ran]:
            cell = self[coord]
            if coord in state:
                assert self.tiles[coord] != Tile.BLOCK
                cell = self.player

            cells.append(str(cell).center(5))

        # fill in the template to create the board drawing, then print!
        return template.format(message, *cells)

    def print_path(self, states):
        for state in states:
            print(self.format_with_state(state=state))


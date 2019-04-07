from enum import Enum, unique
from sys import stderr
from heapy import Heap

RADIUS = 3

@unique
class Colour(Enum):
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
        return self.value > Colour.BLOCK.value

    def __str__(self):
        return {0: " ", 1: "X", 2: "R", 3: "G", 4: "B"}[self.value]

class Tile():

    def __init__(self, colour=Colour.BLANK, heu=None):
        self.colour = colour
        self.heu = heu

    def __str__(self):
        return self.colour.__str__()

'''
Board state from the perspective of one player
'''

class HexBoard():

    def __init__(self, config, radius=RADIUS):
        self.radius = radius
        self.tiles = {}
        self.seenstates = {}
        self.currentstate = tuple()

        self.player = Colour.parse_colour(config["colour"])
        self.currentstate = tuple(tuple(sorted(map(tuple, config["pieces"]))))


        # initialise all blank tiles
        for coord in self.iter_coords():
            self[coord] = Tile()

        # set all the block positions
        for coord in config["blocks"]:
            self[tuple(coord)].colour = Colour.BLOCK
        
        self.exit_coords = tuple(filter(self.is_exit_tile, self.iter_coords()))
        self.set_tile_heuristics()

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
        return sum(self[coord].heu for coord in state)

    def set_tile_heuristics(self):
        # self.basic_heuristics()
        # self.better_heuristics()
        self.dijkstra_heuristics()

    def basic_heuristics(self):
        '''
        takes a hexboard and assigns a heuristic value to each tile (dependent on player)
        VERSION 1: number of jumps from end tiles (H = ceiling(D/2))
        '''
        for coord in self.iter_coords():
            if self[coord].colour != Colour.BLOCK:
                self[coord].heu = self.goal_jump_dist(coord)+1

    def better_heuristics(self):
        for coord in self.iter_coords():
            if self[coord].colour != Colour.BLOCK:
                self[coord].heu = (self.goal_dist(coord)+1)//2 + 1

    def dijkstra_heuristics(self):
        queue = Heap()
        seen_coords = {}
        for exit_coord in self.exit_coords:
            queue.push((1, exit_coord))
            seen_coords[exit_coord] = 1
        
        while queue:
            min_cost, min_coord = queue.pop()
            self[min_coord].heu = min_cost

            for next_coord, _ in self.movejumpchoices(min_coord, tuple(), allowemptyjumps=True):
                if next_coord in seen_coords:
                    old_cost = seen_coords[next_coord]
                    if min_cost+1 < old_cost:
                        seen_coords[next_coord] = min_cost+1
                        queue.replace((old_cost, next_coord), (min_cost+1, next_coord))
                else:
                    queue.push((min_cost+1, next_coord))
                    seen_coords[next_coord] = min_cost+1

    def goal_jump_dist(self, coord):
        '''
        finds the minimum number of steps taken to reach a player's goal tile, assuming jumps on every possible turn
        '''
        return self.goal_dist(coord)/2

    def goal_dist(self, coord):
        '''
        finds the distance from a given point to the player's goal tiles
        '''

        return {Colour.RED:   self.radius - coord[0],
                Colour.GREEN: self.radius - coord[1],
                Colour.BLUE:  self.radius - -sum(coord)}[self.player]

    def is_goal_state(self, state):
        return len(state)==0

    def is_exit_tile(self, coord):
        if self[coord].colour == Colour.BLOCK:
            return False
        
        x, y = coord

        return {Colour.RED: bool(x==RADIUS),
                Colour.GREEN: bool(y == RADIUS),
                Colour.BLUE: bool(sum(coord)==-RADIUS)}[self.player]

    def occupied(self, coord, state=tuple()):
        return coord in state or self[coord].colour == Colour.BLOCK

    def movejumpchoices(self, piececoord, state, allowemptyjumps=False):
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
                    if allowemptyjumps and self.is_valid_coord(jumpcoord) and not self.occupied(jumpcoord):
                        yield (jumpcoord, "JUMP")

                    yield (movecoord, "MOVE")

    def adj_states(self, state):
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

            if self.is_exit_tile(acting_piece):
                new_state = tuple(piece for piece in state if piece!=acting_piece)
                exit_action = f"EXIT from {acting_piece}."
                yield (tuple(sorted(new_state)), exit_action)

    def format_with_state(self, state=None, debug=False, message='', heuristic_mode=False):
        """
        Helper function to print a drawing of a hexagonal board's contents.
        """

        if state == None: state = self.currentstate

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


        # prepare the provided board contents as strings, formatted to size.
        ran = range(-RADIUS, +RADIUS+1)
        cells = []
        for coord in [(q, r) for q in ran for r in ran if -q-r in ran]:

            if heuristic_mode:
                tile = self[coord]
                cell = tile if tile.colour == Colour.BLOCK else tile.heu
            else:
                cell = self[coord]
                if coord in state:
                    assert self.tiles[coord].colour != Colour.BLOCK
                    cell = self.player

            cells.append(str(cell).center(5))

        return template.format(message, *cells)

    def print_path(self, dest_node):
        for node in dest_node.path_from_source():
            print(self.format_with_state(state=node.state, message=f"c={node.cost} + h={node.heu} == {node.cost+node.heu}"))

    def print_board_heuristics(self):
        print(self.format_with_state(message="heuristics: ", heuristic_mode=True))



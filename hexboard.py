# from enum import Enum, unique
from state import State
from game_details import *
import itertools
from copy import deepcopy
from collections import defaultdict


class HexBoard():
    '''
    Representation of the board
    '''

    def __init__(self):
        self.state = State()
        self.seen_state_counts = defaultdict(int)
        self.seen_state_counts[self.state] = 1


    def update(self, player, action):
        self.state.apply_action(player, action)
        self.seen_state_counts[self.state] += 1

    def goal_jump_dist(self, coord, player):
        '''
        finds the minimum number of steps taken to reach a player's goal tile, assuming jumps on every possible turn
        '''
        return (EXIT_DIST[player][coord]+1)//2
    
    def move_jump_choices(self, state, coord, allowemptyjumps=False):
        for move, jump in ALL_NEIGHBOURS[coord]:
            if move in state:
                if jump is not None and jump not in state:
                    yield (jump, "JUMP")
            else:
                if allowemptyjumps and jump is not None and jump not in state:
                    yield (jump, "JUMP")
                yield (move, "MOVE")

    def adj_state_exit_actions(self, player, state=None):
        if state is None:
            state = self.state

        for acting_piece in state[player]:

            if acting_piece in EXIT_COORDS[player]:
                exit_action = ("EXIT", acting_piece)
                new_state = deepcopy(state)
                new_state.apply_action(player, exit_action)
                yield (new_state, exit_action)

    def adj_state_actions(self, player, state=None):
        if state is None:
            state = self.state

        can_move = False
        for acting_piece in state[player]:
            for new_pos, action_type in self.move_jump_choices(state, acting_piece):
                can_move = True
                action = (action_type, (acting_piece, new_pos))
                new_state = deepcopy(state)
                new_state.apply_action(player, action)

                if self.seen_state_counts[new_state] < MAX_STATE_REPEATS:
                    yield (new_state, action)

            if acting_piece in EXIT_COORDS[player]:
                can_move = True
                exit_action = ("EXIT", acting_piece)
                new_state = deepcopy(state)
                new_state.apply_action(player, exit_action)

                if self.seen_state_counts[new_state] < MAX_STATE_REPEATS:
                    yield (new_state, exit_action)
        
        if not can_move:
            yield (state, ("PASS", None))

    def format_board(self, state=None, debug=False, message='', heuristic_mode=False):
        """
        Helper function to print a drawing of a hexagonal board's contents.
        Cheers Matt
        """

        if state == None: state = self.state

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
        cells = []
        for coord in COORDINATES:

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


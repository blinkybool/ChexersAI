# from enum import Enum, unique
from heapy import Heap
from state import State
from game_details import *
import itertools
from copy import deepcopy
from collections import defaultdict


class HexBoard():

    def __init__(self):
        self.state = State()


    def update(self, player, action):
        self.state.apply_action(player, action)

    

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

    def adj_states(self, player, state=None):
        if state is None:
            state = self.state

        can_move = False
        for acting_piece in state[player]:
            for new_pos, action_type in self.move_jump_choices(state, acting_piece):
                can_move = True
                action = (action_type, (acting_piece, new_pos))
                new_state = deepcopy(state)
                new_state.apply_action(player, action)

                yield (new_state, action)

            if acting_piece in EXIT_COORDS[player]:
                can_move = True
                exit_action = ("EXIT", acting_piece)
                new_state = deepcopy(state)
                new_state.apply_action(player, exit_action)
                yield (new_state, exit_action)
        
        if not can_move:
            yield (self, ("PASS", None))

    def format_board(self, state=None, debug=False, message='', heuristic_mode=False):
        """
        Helper function to print a drawing of a hexagonal board's contents.
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

    def print_path(self, dest_node):
        for node in dest_node.path_from_source():
            print(self.format_board(state=node.state, message=f"c={node.cost} + h={node.heu} == {node.cost+node.heu}"))

    def print_board_heuristics(self):
        print(self.format_board(message="heuristics: ", heuristic_mode=True))

    def make_blank_heuristic_maps(self, player=None):
        players = PLAYERS if player is None else (player,)
        return {player: dict.fromkeys(set(COORDINATES).difference(set.union(*map(self.state.__getitem__, OPPONENTS[player])))) for player in PLAYERS}

    def calc_tile_heuristics(self):
        '''
        Determines the heuristic of a tile.
        Simply calls another function as different approaches were taken during development
        Final implementation used dijkstra. Older versions are commented out
        '''
        return self.calc_basic_heuristics()
        # self.better_heuristics()
        # self.dijkstra_heuristics()

    def calc_basic_heuristics(self):
        ''' 
        assigns a heuristic value to each tile
        heuristic assumes an empty board, and calculates the number of jumps required to reach an end tile, plus one to exit
        essentially the cieling of the result of basic_heuristic
        '''
        pass
        # heu_maps = self.make_blank_heuristic_maps()

        # for player in heu_maps:
        #     for coord in heu_maps[player]:
        #         self.heu_maps[player][coord] = self.goal_dist(coord)/2 + 1

    def calc_better_heuristics(self, player):
        ''' 
        assigns a heuristic value to each tile
        heuristic assumes an empty board, and calculates the number of jumps required to reach an end tile, plus one to exit
        essentially the cieling of the result of basic_heuristic
        '''
        pass
        # heu_maps = self.make_blank_heuristic_maps()
        
        # for player in heu_maps:
        #     for coord in heu_maps[player]:
        #         self.heu_maps[player][coord] = (self.goal_dist(coord)+1)//2 + 1

    def set_dijkstra_heuristics(self, player=None):
        '''
        assigns a heuristic value to each tile
        heuristic considers the block tiles on the board
        and calculates the minimum cost to get to each tile from an end tile
        by performing dijkstra (adding one for exit cost).
        Critically, when performing this algorithm, the tile is given the ability to perform jumps over
        empty tiles in order to remain admissible, since in practice, other player tiles may be present
        to facilitate jumps
        '''
        pass
        # heu_maps = self.make_blank_heuristic_maps()
        # queue = Heap()
        # seen_coords = {}
        # for exit_coord in EXIT_COORDS[player]:
        #     # initial coord initialised with 1 to allow for exit cost
        #     queue.push((1, exit_coord))
        #     seen_coords[exit_coord] = 1
        
        # # perform dijkstra
        # while queue:
        #     min_cost, min_coord = queue.pop()
        #     self[min_coord].heu = min_cost

        #     # assume pieces can jump over empty squares
        #     for next_coord, _ in self.move_jump_choices(min_coord, allowemptyjumps=True):
        #         # push accessible coords to queue if not seen before
        #         if next_coord in seen_coords:
        #             old_cost = seen_coords[next_coord]
        #             if min_cost+1 < old_cost:
        #                 seen_coords[next_coord] = min_cost+1
        #                 queue.replace((old_cost, next_coord), (min_cost+1, next_coord))
        #         else:
        #             queue.push((min_cost+1, next_coord))
        #             seen_coords[next_coord] = min_cost+1
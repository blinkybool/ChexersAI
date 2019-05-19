from game_details import *
from weights import *
import csv
import itertools
from copy import deepcopy

VERIFY_EVAL_ADJUST = False
DEBUG = True

class State():
    

    def __init__(self,  players_pieces=None, players_exited=None):
        if players_pieces is None:
            players_pieces = deepcopy(START_COORDS)
        if players_exited is None:
            players_exited = PlayerDict(int)
        
        self.players_pieces = players_pieces
        self.players_exited = players_exited
        self.players_stats = self.calc_players_stats()

    def __getitem__(self, key):
        return self.players_pieces.__getitem__(key)

    def __contains__(self, item):
        return any(item in pieces for pieces in self.players_pieces.values())

    def get_absolute_eval(self):
        if self.is_terminal():
            return {player: BEST_POSSIBLE_EVAL if self.is_winner(player) else WORST_POSSIBLE_EVAL for player in PLAYERS}
        return {player: sum(weight * self.players_stats[player][stat_name] for stat_name, weight in WEIGHTS.items()) for player in PLAYERS}

    def get_relative_eval(self):
        evaluation = self.get_absolute_eval()
        return {player: player_eval - sum(evaluation[opponent] for opponent in OPPONENTS[player])/2 for player, player_eval in evaluation.items()}

    def iter_opponents_pieces(self, player):
        return ((opponent, opponent_pieces) for opponent, opponent_pieces in self.players_pieces.items() if opponent!=player)

    def is_terminal(self):
        return any(map(int(NUM_TO_WIN).__le__, self.players_exited.values()))

    def is_winner(self, player):
        return self.players_exited[player] >= NUM_TO_WIN
    
    def calc_players_stats(self):
        players_stats = {player: {stat: int() for stat in WEIGHTS.keys()} for player in PLAYERS}

        for player, pieces in self.players_pieces.items():
            players_stats[player][NUM_PIECES] = len(self.players_pieces[player])
            players_stats[player][NUM_EXITED] = self.players_exited[player]
            players_stats[player][TOTAL_DIST] = sum(EXIT_DIST[player][piece] for piece in self.players_pieces[player])
            for piece in pieces:
                if piece in EXIT_COORDS[player]:
                    players_stats[player][NUM_CAN_EXIT] += 1
                for move, jump, in ALL_NEIGHBOURS[piece]:
                    if jump is not None and jump not in self:
                        for opponent in OPPONENTS[player]:
                            if move in self.players_pieces[opponent]:
                                players_stats[player][NUM_THREATS] += 1
                                players_stats[opponent][NUM_DANGERED] += 1
        
        return players_stats


                                
    def apply_action(self, acting_player, action):
        action_type, details = action

        if action_type == "EXIT":
            exit_coord = details
            self.players_pieces[acting_player].discard(exit_coord)
            self.players_exited[acting_player] += 1

            self.adjust_eval_piece_remove(acting_player, exit_coord)

        elif action_type == "MOVE":
            from_coord, to_coord = details
            self.players_pieces[acting_player].discard(from_coord)
            self.adjust_eval_piece_remove(acting_player, from_coord)

            self.players_pieces[acting_player].add(to_coord)
            self.adjust_eval_piece_add(acting_player, to_coord)


        elif action_type == "JUMP":
            from_coord, to_coord = details
            between_coord = coord_between(from_coord, to_coord)

            self.players_pieces[acting_player].discard(from_coord)
            self.adjust_eval_piece_remove(acting_player, from_coord)

            for opponent in OPPONENTS[acting_player]:
                if between_coord in self.players_pieces[opponent]:
                    self.players_pieces[opponent].discard(between_coord)
                    self.adjust_eval_piece_remove(opponent, between_coord)

                    self.players_pieces[acting_player].add(between_coord)
                    self.adjust_eval_piece_add(acting_player, between_coord)
                    break

            self.players_pieces[acting_player].add(to_coord)
            self.adjust_eval_piece_add(acting_player, to_coord)
        
        for player in PLAYERS:
            self.players_stats[player][NUM_EXITED] = self.players_exited[player]

            self.players_stats[player][TOTAL_DIST] = sum(EXIT_DIST[player][piece] for piece in self.players_pieces[player])
        
        if VERIFY_EVAL_ADJUST:
            correct_stats = self.calc_players_stats()
            for player in PLAYERS:
                for stat_name, stat_val in self.players_stats[player].items():
                    assert(stat_val == correct_stats[player][stat_name])
    
    def adjust_eval_piece_add(self, player, coord):
        return self.adjust_eval_piece_add_OR_remove(player, coord, addMode=True)

    def adjust_eval_piece_remove(self, player, coord):
        return self.adjust_eval_piece_add_OR_remove(player, coord, addMode=False)

    def adjust_eval_piece_add_OR_remove(self, player, coord, addMode):
        opponents = OPPONENTS[player]

        addORremoveFactor = (1 if addMode else -1)

        self.players_stats[player][NUM_PIECES] += addORremoveFactor

        if coord in EXIT_COORDS[player]:
            self.players_stats[player][NUM_CAN_EXIT] += addORremoveFactor
        
        for move, jump in ALL_NEIGHBOURS[coord]:

            if jump is not None:
                if jump not in self:
                    # Add/Remove threats/dangers regarding coord-piece jumping over neighbouring opponent
                    # 
                    # attacker
                    #  .-'-._.-'-._.-'-._
                    # |coord|move |jump |
                    # '-._.-'-._.-'-._.-'
                    #       victim
                    for opponent in opponents:
                        if move in self.players_pieces[opponent]:
                            self.players_stats[opponent][NUM_DANGERED] += addORremoveFactor
                            self.players_stats[player][NUM_THREATS] += addORremoveFactor
                            break
                else:
                    # Add/Remove threats/dangers regarding jump-piece jumping over move-piece and landing on coord-spot
                    # 
                    #             attacker
                    #  .-'-._.-'-._.-'-._
                    # |coord|move |jump |
                    # '-._.-'-._.-'-._.-'
                    #       victim 
                    for victim, victim_pieces in self.players_pieces.items():
                        if move in victim_pieces:
                            for attacker, attacker_pieces in self.iter_opponents_pieces(victim):
                                if jump in attacker_pieces:
                                    self.players_stats[attacker][NUM_THREATS] -= addORremoveFactor
                                    self.players_stats[victim][NUM_DANGERED] -= addORremoveFactor
                                    break
                            break

        # Add/Remove threats/dangers regarding jump-piece jumping over move-piece and landing on coord-spot
        # 
        #             attacker        attacker
        #  .-'-._.-'-._.-'-._          .-'-._.-'-._.-'-._   
        # |cord1|coord|cord2|   OR    |cord1|coord|cord2|   
        # '-._.-'-._.-'-._.-'         '-._.-'-._.-'-._.-'   
        #       victim                      victim          
        for coord1, coord2 in OPPOSING_NEIGHBOUR_PAIRS[coord]:
            if coord1==None or coord2==None:
                continue
            for opponent in opponents:
                if      (coord1 in self.players_pieces[opponent] \
                    and  coord2 not in self)   \
                    or  (coord2 in self.players_pieces[opponent] \
                    and  coord1 not in self):
                    self.players_stats[opponent][NUM_THREATS] += addORremoveFactor
                    self.players_stats[player][NUM_DANGERED] += addORremoveFactor
                    break
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # Set up the board template:
        if not DEBUG:
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
            for player, pieces in self.players_pieces.items():
                if qr in pieces:
                    cell = str({ # something 5 characters wide for each colour:
                                    RED: " \033[1m(\033[91mR\033[0m\033[1m)\033[0m ",
                                    GREEN: " \033[1m(\033[92mG\033[0m\033[1m)\033[0m ",
                                    BLUE: " \033[1m(\033[94mB\033[0m\033[1m)\033[0m ",
                                    ' ': "     "
                                }[player]).center(5)
                    break
            else:
                cell = "     " # 5 spaces will fill a cell
            cells.append(cell)

        # fill in the template to create the board drawing, then print!
        board = template.format("STATE", *cells)
        return board
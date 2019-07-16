from game_details import *
from weights import *
import csv
import itertools
from copy import deepcopy

VERIFY_EVAL_ADJUST = False
DEBUG = False

class State():
    '''
    Represents the current state of the board
    players_pieces: maps players to sets of their pieces
    players_exited: maps players to their number of exited pieces
    turn: the player whose current turn it is
    '''
    def __hash__(self):
        return self._hash

    def set_hash(self):
        self._hash = hash(tuple((self.players_exited[player], frozenset(self.players_pieces[player])) for player in PLAYERS))

    def __init__(self,  players_pieces=None, players_exited=None, turn=None):

        # Set default values
        if players_pieces is None:
            players_pieces = deepcopy(START_COORDS)
        if players_exited is None:
            players_exited = PlayerDict(int)
        if turn is None:
            turn = NEXT_PLAYER[FIRST_PLAYER]

        self.players_pieces = players_pieces
        self.players_exited = players_exited
        self.players_stats = self.calc_players_stats()
        self.set_hash()
        self.turn = turn

    def __getitem__(self, key):
        return self.players_pieces.__getitem__(key)

    def __contains__(self, item):
        return any(item in pieces for pieces in self.players_pieces.values())

    def __eq__(self, other):
        if type(self) == type(other):
            for player in PLAYERS:
                if self.players_exited[player] != other.players_exited[player]:
                    return False
                if self.players_pieces[player] != other.players_pieces[player]:
                    return False
            return True
        return False

    # get the best strategies for each player to use
    def getStrategies(self):
        playerStratWeights = {}
        for player in PLAYERS:
            if len(self.players_pieces[player]) + self.players_exited[player] < NUM_TO_WIN:
                if len(self.players_pieces[player]) == 1:
                    playerStratWeights[player] = LAST_AND_NEED_MORE
                else:
                    playerStratWeights[player] = NEED_MORE

            elif len(self.players_pieces[player]) + self.players_exited[player] > NUM_TO_WIN:
                if len(self.players_pieces[player]) + self.players_exited[player] >= NUM_TO_WIN + 3:
                    playerStratWeights[player] = HAVE_LOTS_EXTRA

                if len(self.players_pieces[player]) + self.players_exited[player] >= NUM_TO_WIN + 2:
                    playerStratWeights[player] = HAVE_SOME_EXTRA
                else:
                    playerStratWeights[player] = HAVE_1_EXTRA
            
            else:
                playerStratWeights[player] = STANDARD
        return playerStratWeights


    # calculate weighted sum of state features
    # this is essentially the evaluation function
    def get_raw_eval(self, playerStrats = None):
        raw_dict = PlayerDict(float)
        modeWeights={}
        if playerStrats is None:
            playerStrats = self.getStrategies()


        for player in PLAYERS:
            playerStratWeights = STRATEGIES[playerStrats[player]]
            for stat_name in WEIGHTS:
                modeWeights[stat_name] = WEIGHTS[stat_name] * playerStratWeights[stat_name]
            raw_dict[player] = modeWeights[NUM_PIECES] * len(self.players_pieces[player])
            raw_dict[player] += modeWeights[NUM_EXITED] * self.players_exited[player]
            for stat_name, stat in self.players_stats[player].items():

                # Reweight being in danger according to whose turn it is
                if stat_name == NUM_DANGERED:
                    if self.turn == player:
                        raw_dict[player] += (modeWeights[stat_name]*stat)/2
                    else:
                        raw_dict[player] += (modeWeights[stat_name]*stat)*2
                elif stat_name == NUM_THREATS:
                    if self.turn == player:
                        raw_dict[player] += (modeWeights[stat_name]*stat)*2
                    else:
                        raw_dict[player] += (modeWeights[stat_name]*stat)/2

                # convert distance into average distance
                elif stat_name == TOTAL_DIST and len(self.players_pieces[player]):
                    raw_dict[player] += (modeWeights[stat_name]*stat)/len(self.players_pieces[player])
                else:
                    raw_dict[player] += modeWeights[stat_name]*stat
            
        return raw_dict

    # Prioritise details of the terminal states, then normalize the raw evaluations of each player to each other
    def get_relative_eval(self):
        evaluation = self.get_raw_eval()
        #return {player: (self.utility(player), player_eval) for player, player_eval in evaluation.items()}
        relative_eval = {}
        for player, player_eval in evaluation.items():
            opponent_raw = 0
            opponent_raw += 0.45 * evaluation[min(OPPONENTS[player], key=evaluation.__getitem__)] + 0.55 * evaluation[max(OPPONENTS[player], key=evaluation.__getitem__)]
            relative_eval[player] = (self.utility(player), player_eval - opponent_raw)
        return relative_eval


    # Slices players pieces dictionary to be just the opponents
    def iter_opponents_pieces(self, player):
        return ((opponent, opponent_pieces) for opponent, opponent_pieces in self.players_pieces.items() if opponent!=player)

    def is_terminal(self):
        return any(map(int(NUM_TO_WIN).__le__, self.players_exited.values()))

    def is_winner(self, player):
        return self.players_exited[player] >= NUM_TO_WIN

    def utility(self, player):
        if self.is_terminal():
            return 1 if self.is_winner(player) else -1
        return 0

    
    def calc_players_stats(self):
        players_stats = {player: {stat_name: int() for stat_name in (TOTAL_DIST,
                                                                        NUM_CAN_EXIT,
                                                                        NUM_THREATS,
                                                                        NUM_DANGERED,
                                                                        NUM_PROTECTS)} for player in PLAYERS}

        for player, pieces in self.players_pieces.items():
            players_stats[player][TOTAL_DIST] = sum(EXIT_DIST[player][piece] for piece in self.players_pieces[player])
            for piece in pieces:
                if piece in EXIT_COORDS[player]:
                    players_stats[player][NUM_CAN_EXIT] += 1
                for move, jump in ALL_NEIGHBOURS[piece]:
                    if jump is not None and jump not in self:
                        for opponent, opponents_pieces in self.iter_opponents_pieces(player):
                            if move in opponents_pieces:
                                players_stats[player][NUM_THREATS] += 1
                                players_stats[opponent][NUM_DANGERED] += 1
                                break
                    if move in self.players_pieces[player]:
                        players_stats[player][NUM_PROTECTS] += 1
        
        return players_stats

    def apply_action(self, acting_player, action):
        action_type, details = action

        if action_type == "EXIT":
            exit_coord = details
            self.players_pieces[acting_player].remove(exit_coord)
            self.players_exited[acting_player] += 1

            self.adjust_eval_remove_piece(acting_player, exit_coord)

        elif action_type == "MOVE":
            from_coord, to_coord = details
            self.players_pieces[acting_player].remove(from_coord)
            self.adjust_eval_remove_piece(acting_player, from_coord)

            self.players_pieces[acting_player].add(to_coord)
            self.adjust_stats_add_piece(acting_player, to_coord)


        elif action_type == "JUMP":
            from_coord, to_coord = details
            between_coord = coord_between(from_coord, to_coord)

            self.players_pieces[acting_player].remove(from_coord)
            self.adjust_eval_remove_piece(acting_player, from_coord)

            for opponent in OPPONENTS[acting_player]:
                if between_coord in self.players_pieces[opponent]:
                    self.players_pieces[opponent].remove(between_coord)
                    self.adjust_eval_remove_piece(opponent, between_coord)

                    self.players_pieces[acting_player].add(between_coord)
                    self.adjust_stats_add_piece(acting_player, between_coord)
                    break

            self.players_pieces[acting_player].add(to_coord)
            self.adjust_stats_add_piece(acting_player, to_coord)
        
        self.turn = NEXT_PLAYER[acting_player]
        self.set_hash()
        
        if VERIFY_EVAL_ADJUST:
            correct_stats = self.calc_players_stats()
            for player in PLAYERS:
                for stat_name, stat_val in self.players_stats[player].items():
                    assert(stat_val == correct_stats[player][stat_name])
    
    def adjust_stats_add_piece(self, player, coord):
        return self.adjust_eval_add_OR_remove_piece(player, coord, addMode=True)

    def adjust_eval_remove_piece(self, player, coord):
        return self.adjust_eval_add_OR_remove_piece(player, coord, addMode=False)

    def adjust_eval_add_OR_remove_piece(self, player, coord, addMode):
        opponents = OPPONENTS[player]

        addORremoveFactor = (1 if addMode else -1)

        self.players_stats[player][TOTAL_DIST] += addORremoveFactor * EXIT_DIST[player][coord]

        if coord in EXIT_COORDS[player]:
            self.players_stats[player][NUM_CAN_EXIT] += addORremoveFactor
        
        for move, jump in ALL_NEIGHBOURS[coord]:

            if move in self.players_pieces[player]:
                self.players_stats[player][NUM_PROTECTS] += 2 * addORremoveFactor

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
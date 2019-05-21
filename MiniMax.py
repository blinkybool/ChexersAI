from hexboard import HexBoard
from game_details import *
from operator import itemgetter
from state import State

CUTOFF = 2


def maxPlayer(board, state, depth, player):
    '''
    Returns the maximal evaluation state for the expected reachable states up to a cutoff
    '''

    if depth >= CUTOFF or state.is_terminal():
        return state


    return max(map(itemgetter(0), board.adj_state_actions(player, state=state)),
                    key=lambda next_state: maxPlayer(board,
                                                        next_state,
                                                        depth+1,
                                                        NEXT_PLAYER[player]).get_relative_eval()[player])


def miniMax(board, player):
    '''
    Returns the action which maximises the expected state evaluation after CUTOFF many moves
    '''
    return max(board.adj_state_actions(player, board.state),
                        key=lambda nextstate_action: 
                            maxPlayer(board,
                                        state=nextstate_action[0],
                                        depth=1,
                                        player=NEXT_PLAYER[player]).get_relative_eval()[player])[1]


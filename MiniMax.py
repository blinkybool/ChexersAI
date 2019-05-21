from hexboard import HexBoard
from node import Node
from random import randint
from game_details import *
from operator import itemgetter
from state import State

memoized_states = {}

CUTOFF = 1
MIN_DEPTH_AWAY = 2

def maxPlayer(board, state, depth, player, root_strategies):

    if (state, root_strategies) in memoized_states:
        eventual_state, depth_away = memoized_states[state, root_strategies]

        if depth + depth_away >= CUTOFF:
            return eventual_state


    if depth >= CUTOFF or state.is_terminal():
        return state

    eventual_state = max(map(itemgetter(0), board.adj_state_actions(player, state=state)),
                            key=lambda next_state: maxPlayer(board,next_state,depth+1,NEXT_PLAYER[player],root_strategies).get_relative_eval()[player])
    
    depth_away = CUTOFF - depth
    if depth_away >= MIN_DEPTH_AWAY:
        memoized_states[state, root_strategies] = (eventual_state, depth_away)

def miniMax(board, player):
    strategies = board.state.getStrategies()

    ordered_strategies = tuple(strategies[player] for player in PLAYERS)

    best_state,\
    best_action = max(board.adj_state_actions(player, board.state),
                        key=lambda nextstate_action: 
                            maxPlayer(board,
                                        state=nextstate_action[0],
                                        depth=0,
                                        player=NEXT_PLAYER[player],
                                        root_strategies=ordered_strategies).get_relative_eval()[player])
    return (best_state, best_action)



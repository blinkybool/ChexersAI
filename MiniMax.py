from hexboard import HexBoard
from node import Node
from random import randint
from game_details import *
from operator import itemgetter
from state import State

CUTOFF = 2

'''
def maxValue(state, alpha, beta, depth):
    if depth > CUTOFF:
            return evaluate(state)
    for nextState in map(lambda x: x[0], HexBoard.adj_states(state)):
        alpha = max(alpha, MinValue(nextState, alpha, beta, depth+1))
        if alpha >= beta:
            return beta
    return alpha

def minValue(state, alpha, beta, depth):
    if depth > CUTOFF:
            return evaluate(state)
    for nextState in map(lambda x: x[0], HexBoard.adj_states(state)):
        beta = min(alpha, MaxValue(nextState, alpha, beta, depth))
        if beta <= alpha:
            return alpha
    return beta
    '''

def maxPlayer(board, state, depth, player):
    if depth >= CUTOFF:
        return state
    return max(map(itemgetter(0), board.adj_states(player, state=state)),
                key=lambda next_state:
                    maxPlayer(board, next_state, depth+1, NEXT_PLAYER[player])
                        .get_relative_eval()[player])

def miniMax(board, player):
    best_state,\
    best_action = max(board.adj_states(player, board.state),
                        key=lambda nextstate_action: 
                            maxPlayer(board, nextstate_action[0], 1, NEXT_PLAYER[player])[player])
    return (best_state, best_action)


# def evaluate(state):
#     '''
#     takes a state, and returns a tuple, with each entry representing how good the state is for each player.
#     rawEval returns a number determining how good a state is for a given player in isolation,
#     but does not consider how good that player's position is relative to the other players.
#     '''
#     rawVal = [0]*PLAYERNUM
#     evaluation = [0]*PLAYERNUM
#     for player in range(PLAYERNUM):
#         rawVal[player] = rawEval(state, player)
#     for player in range(PLAYERNUM):
#         evaluation[player] = rawVal[player] - min(rawVal[(player + 1)%PLAYERNUM], rawVal[(player + 2)%PLAYERNUM])/3 - 2*max(rawVal[(player + 1)%PLAYERNUM], rawVal[(player + 2)%PLAYERNUM])/3
#     return (randint(0,10)-5, randint(0,10)-5, randint(0,10)-5)



# def rawEval(state, player):
#     '''
#     Determines how good a state is for a player, irrespective of how good the position is for the other players
#     '''

#     -K1*total_distance + K2*total_pieces


# '''
# keeping track of state (solved by using wrapper function)
# def maxPlayer(state, depth, player):
#     maxVal = None
#     if depth > CUTOFF:
#         return evaluate(state)
#     for nextState in map(lambda x: x[0], HexBoard.adj_states(state)):
#         nextVal = maxPlayer(nextState, depth+1, (player+1)%3)
#         if maxVal is None:
#             maxState = nextState
#             maxVal = nextVal
#         elif nextVal[player] > maxVal[player]:
#             maxState = nextState
#             maxVal = nextVal
#     return (maxVal, maxState)
# '''


# def maxRed(state, depth):
#     maxVal = None
#     if depth > CUTOFF:
#         return evaluate(state)
#     for nextState in map(lambda x: x[0], HexBoard.adj_states(state)):
#         if maxVal is None:
#             maxVal = maxGreen(nextState, depth+1)
#         else:
#             maxVal = max(maxVal, maxGreen(nextState, depth+1), key=(lambda x: x[RED]))
#     return maxVal




# def maxGreen(state, depth):
#     maxVal = None
#     if depth > CUTOFF:
#         return evaluate(state)
#     for nextState in map(lambda x: x[0], HexBoard.adj_states(state)):
#         if maxVal is None:
#             maxVal = maxBlue(nextState, depth+1)
#         else:
#             maxVal = max(maxVal, maxBlue(nextState, depth+1), key=(lambda x: x[GREEN]))
#     return maxVal

# def maxBlue(state, depth):
#     maxVal = None
#     if depth > CUTOFF or isGoal(state):
#         return evaluate(state)
#     for nextState in map(lambda x: x[0], HexBoard.adj_states(state)):
#         if maxVal is None:
#             maxVal = maxRed(nextState, depth+1)
#         else:
#             maxVal = max(maxVal, maxRed(nextState, depth+1), key=(lambda x: x[BLUE]))
#     return maxVal
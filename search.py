"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
Billy Price
Luca Kennedy
"""


"""
And now, a message from our intelligent agent:
"""

"""
Hello {markerName}, my name is Kanye's fingers, and I'm here to use my fingers to take the pieces to where they want to be
"""

import sys
import json
from math import ceil
from hexboard import Tile, Colour, PieceState, HexBoard
from heapq import heappush, heappop
from node import Node
from parseboard import parseboard
from heapy import Heap

def parsejson(filename):
    # extract data from json
    with open(filename) as config_json:
        config = json.load(config_json)

    return config

def kanyeplspushthepieces(board):
    queue = Heap()
    bestnode = None
    # board.seen_states.add(board.start_state.pieces)
    queue.push(Node(state=board.start_state, parent=None, prevmove="", cost=0, heu=board.start_state.get_heu(board)))
    while queue:
        nextnode = queue.pop()
        if (bestnode is not None) and (nextnode >= bestnode):     # pretty sure this is the break condition (even though the first one we find should be best)
            break 
        if nextnode.isgoal():
            bestnode = nextnode
            continue
        for node in nextnode.expand(board):
            if node.state.pieces in board.seen_states:
                old_node = board.seen_states[node.state.pieces]
                if node < old_node:
                    queue.replace(old_node, node)
                    board.seen_states[node.state.pieces] = node
            else:
                board.seen_states[node.state.pieces] = node
                queue.push(node)

    return bestnode

def main():

    if len(sys.argv)==1:
        board_config = parseboard()
    elif len(sys.argv)==2:
        board_config = parsejson(sys.argv[1])
    else:
        print("Too many arguments", file=sys.stderr)
        exit()

    board = HexBoard(board_config)
    
    endnode = kanyeplspushthepieces(board)

    # endnode.print_path()
    endnode.print_path_boards(board)
               


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()

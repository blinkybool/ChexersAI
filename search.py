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

import os, sys, json
from math import ceil
from hexboard import Tile, HexBoard
from heapq import heappush, heappop
from node import Node
from parseboard import parseboard
from heapy import Heap

REPLACEMENTS = 0
TESTMODE = True


def parsejson(filename):
    # extract data from json
    with open(filename) as config_json:
        config = json.load(config_json)

    return config

def kanyeplspushthepieces(board):
    global REPLACEMENTS
    queue = Heap()
    bestnode = None
    startnode = Node(state=board.currentstate, cost=0, heu=board.state_heu(), parent=None, prevmove="",)
    board.seenstates[board.currentstate] = startnode
    queue.push(startnode)
    while queue:
        nextnode = queue.pop()
        if (bestnode is not None) and (nextnode >= bestnode):     # pretty sure this is the break condition (even though the first one we find should be best)
            break 
        if nextnode.isgoal():
            bestnode = nextnode
            continue
        for node in nextnode.expand(board):
            if node.state in board.seenstates:
                old_node = board.seenstates[node.state]
                if node < old_node:
                    REPLACEMENTS +=1
                    queue.replace(old_node, node)
                    board.seenstates[node.state] = node
            else:
                board.seenstates[node.state] = node
                queue.push(node)

    return bestnode

def handle_input():
    # find board config file
    if len(sys.argv)==1:
        return parseboard()
    elif len(sys.argv)==2:
        try:
            input_file = sys.argv[1]
            file_ext = os.path.splitext(input_file)[1]
            return {'.json': parsejson,
                    '.txt' : parseboard}[file_ext](input_file)
        except:
            print("bad input", file=sys.stderr)
            exit()
    else:
        print("bad input", file=sys.stderr)
        exit()



def main():

    board_config = handle_input()

    board = HexBoard(board_config)
    
    endnode = kanyeplspushthepieces(board)

    # endnode.print_path()
    # endnode.print_path_boards(board)

    if TESTMODE:
        endnode.print_path_boards(board)
        global REPLACEMENTS
        print(f"STATS: replacements:{REPLACEMENTS}")
    else:
        endnode.print_path()
        print("# yeehaw")


if __name__ == '__main__':
    main()

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
from time import sleep

VANILLA_MODE = False
PRINT_INSTRUCTIONS = True
PRINT_EXECUTION = False
PRINT_BOARD_PATH = True
PRINT_HEURISTICS = True
SLEEP_TIME = 0.01

if VANILLA_MODE:
    PRINT_INSTRUCTIONS = True
    PRINT_BOARD_PATH = False
    PRINT_EXECUTION = False
    PRINT_HEURISTICS = False


def parsejson(filename):
    # extract data from json
    with open(filename) as config_json:
        config = json.load(config_json)

    return config

def kanyeplspushthepieces(board):

    min_queue = Heap()

    startnode = Node(state=board.currentstate,
                     cost=0,
                     heu=board.state_heu(),
                     parent=None,
                     prevmove="",)
    
    board.seenstates[board.currentstate] = startnode
    min_queue.push(startnode)

    if PRINT_EXECUTION:
        nodes_expanded = 0
        max_cost = 0
    
    while min_queue:
        min_node = min_queue.pop()

        if PRINT_EXECUTION:
            nodes_expanded += 1
            max_cost = max(max_cost, min_node.cost)
            stats = f"min_queue size: {len(min_queue)}\n# nodes expanded: {nodes_expanded}\
                        \n# max cost: {max_cost}\n# cur cost:{min_node.cost:2}" + min_node.cost*"#"
            print(board.format_with_state(message=stats,state=min_node.state))
            sleep(SLEEP_TIME)
        
        if board.is_goal_state(min_node.state):
            break
        
        for adj_node in min_node.expand(board):
            if adj_node.state in board.seenstates:
                old_node = board.seenstates[adj_node.state]
                if adj_node < old_node:
                    min_queue.replace(old_node, adj_node)
                    board.seenstates[adj_node.state] = adj_node
            else:
                board.seenstates[adj_node.state] = adj_node
                min_queue.push(adj_node)

    return min_node

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

    dest_node = kanyeplspushthepieces(board)

    if PRINT_BOARD_PATH:
        board.print_path(dest_node)
    
    dest_node.print_instructions()
    print(f"# yeehaw {dest_node.cost} moves")
    
    if PRINT_HEURISTICS:
        board.print_board_heuristics()


if __name__ == '__main__':
    main()

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
PRINT_EXECUTION = True
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

    for piececoord in board.currentstate:
        if board[piececoord].heu == None:
            return None # Not possible for at least one piece to reach goal
    
     
    
    # Construct the first node based on start conditions
    startnode = Node(state=board.currentstate,
                     cost=0,
                     heu=board.state_heu(),
                     parent=None,
                     prevmove="",)
    
    # Create a min-priority, using key = (cost + heuristic) defined in Node Class
    min_queue = Heap()
    min_queue.push(startnode)

    # keep track of all nodes seen, starting with startnode
    # seenstates is a dictionary with...
        # key: board state
        # value: the node with that state
    board.seenstates[board.currentstate] = startnode
    

    if PRINT_EXECUTION:
        nodes_expanded = 0
        max_cost = 0
    
    # process every node in the queue until goal is found or search exhausted
    while min_queue:
        min_node = min_queue.pop()

        if PRINT_EXECUTION:
            # Prints out the state of each node as it is processed, for debugging purposes
            nodes_expanded += 1
            max_cost = max(max_cost, min_node.cost)
            stats = f"min_queue size: {len(min_queue)}\n# nodes expanded: {nodes_expanded}\
                        \n# max cost: {max_cost}\n# cur cost:{min_node.cost:2}" + min_node.cost*"#"
            print(board.format_with_state(message=stats,state=min_node.state))
            sleep(SLEEP_TIME)
        
        if board.is_goal_state(min_node.state):
            # if min_node is a goal state, it must be an optimal solution.
            # The priority queue ensures for every other node, min_node.cost <= node.cost + node.heuristic.
            # The heuristic is admissible, hence every other node must lead to a solution at least as expensive
            # as the current min_node
            return min_node
        
        # expand the min node
        for adj_node in min_node.expand(board):
            # Check if we have seen this state before
            if adj_node.state in board.seenstates:
                old_node = board.seenstates[adj_node.state]
                # Check if new node is cheaper than the previous node with same state.
                # (it IS possible that the second node is cheaper)
                if adj_node < old_node: # < operator compares nodes based on the same key as the queue (cost + heuristic) (See Node Class)
                    # replace old node with new node in queue
                    min_queue.replace(old_node, adj_node)
                    board.seenstates[adj_node.state] = adj_node
            else:
                # if state is unseen, add to queue to be processed
                board.seenstates[adj_node.state] = adj_node
                min_queue.push(adj_node)

    

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
    # initialise piece positions and store block positions
    board_config = handle_input()
    board = HexBoard(board_config)
    # run search algorithm
    dest_node = kanyeplspushthepieces(board)

    if dest_node==None:
        print("# can't do it sorry :(")
        return

    # prints every board state along the path (run with "| more -16" to animate with spacebar)
    if PRINT_BOARD_PATH:
        board.print_path(dest_node)
    
    # prints the required output
    dest_node.print_instructions()

    # Billy insisting on doing a weird output for some reason
    print(f"# yeehaw {dest_node.cost} moves")
    
    # used for debug purposes
    if PRINT_HEURISTICS:
        board.print_board_heuristics()


if __name__ == '__main__':
    main()

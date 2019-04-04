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

class PriorityQueue():
    
    def __init__(self):
        self.queue = []
    
    def push(self, node):
        heappush(self.queue, node)
    
    def pop(self):
        return heappop(self.queue)

    def __bool__(self):
        return bool(self.queue)



class Node():
    def __init__(self, state, parent, prevmove, cost, heu):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heu = heu
        self.prevmove = prevmove

    def isgoal(self):
        return not self.state
    

    # defines how a node should be prioritised for a priority queue.
    # since we are using A*, nodes are ordered based on cost + heuristic
    def __eq__(self, other):
        return (self.cost + self.heu) == (other.cost + other.heu)

    def __ne__(self, other):
        return (self.cost + self.heu) != (other.cost + other.heu)

    def __lt__(self, other):
        return (self.cost + self.heu) < (other.cost + other.heu)

    def __le__(self, other):
        return (self.cost + self.heu) <= (other.cost + other.heu)

    def __gt__(self, other):
        return (self.cost + self.heu) > (other.cost + other.heu)

    def __ge__(self, other):
        return (self.cost + self.heu) >= (other.cost + other.heu)

    def __repr__(self):
        return f"cost:{self.cost} heu:{self.heu} state:{self.state}" 

    def expand(self, hb):
        for newstate, move in hb.new_states(self.state):
            yield Node(newstate, self, move, self.cost+1, newstate.get_heu(hb))

    def get_state_path(self):
        if self.parent is not None:
            return self.parent.get_state_path().append(self.state)
        return [self.state]

    def print_path(self):
        if self.parent is not None:
            self.parent.print_path()
            print(self.prevmove)

    def print_path_boards(self,board):
        if self.parent is not None:
            self.parent.print_path_boards(board)
        print(board.format_with_state(self.state, message=f"c={self.cost} + h={self.heu} == {self.cost+self.heu}"))
    
'''


        curr_node = self
        move_list = []
        while curr_node.parent is not None:
            move_list.append(curr_node.prevmove)
            curr_node = curr_node.parent
        
        while move_list:
            print(move_list.pop())'''




def main():
    board = HexBoard(start_config_file=sys.argv[1])
    queue = PriorityQueue()
    bestnode = None
    board.seen_states.add(board.start_state.pieces)
    queue.push(Node(state=board.start_state, parent=None, prevmove="", cost=0, heu=board.start_state.get_heu(board)))
    while queue:
        nextnode = queue.pop()
        board.seen_states.add(nextnode.state.pieces)
        if bestnode and nextnode >= bestnode:     # pretty sure this is the break condition (even though the first one we find should be best)
            break 
        if nextnode.isgoal():
            bestnode = nextnode
            continue
        for node in nextnode.expand(board):
            if node.state.pieces not in board.seen_states:
                queue.push(node)

    # bestnode.print_path()
    bestnode.print_path_boards(board)
               


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()

from collections import namedtuple  
from itertools import islice

preNode = namedtuple("preNode", ['state', 'cost', 'heu', 'parent', 'prevmove'])

class Node(preNode):
    '''
    Node for searching through different states
    Attributes:
        state: a tuple of coordinates of the player's pieces
        cost: the number of moves taken to enter the state
        heu: a heuristic value giving a lower bound
                on the number of moves needed to reach the goal state
        parent: the node from which this node was expanded
        prevmove: a string describing the move transitioning parent.state to self.state
    '''

    def __hash__(self):
        # use relevant componenents for hashing, ignoring the parent node to avoid
        # to avoid recursive calls to __hash__
        return hash((self.state, self.cost, self.heu))
    
    # defines how a node should be prioritised in a priority queue.
    # since we are using A*, nodes are ordered based on cost + heuristic

    def __lt__(self, other):
        return (self.cost + self.heu) < (other.cost + other.heu)

    def __le__(self, other):
        return (self.cost + self.heu) <= (other.cost + other.heu)

    def __gt__(self, other):
        return (self.cost + self.heu) > (other.cost + other.heu)

    def __ge__(self, other):
        return (self.cost + self.heu) >= (other.cost + other.heu)

    def expand(self, board):
        '''
        generates nodes containing adjacent states which are 1 move away from self.state
        on the board
        '''
        for adj_state, movestring in board.adj_states(self.state):
            yield Node(state=adj_state,
                       cost=self.cost+1,
                       heu=board.state_heu(adj_state),
                       parent=self,
                       prevmove=movestring)

    def path_from_source(self):
        '''returns an iterator over the nodes leading up to the current node'''
        if self.parent != None:
            yield from self.parent.path_from_source()
        yield self

    def print_instructions(self):
        '''
        print all the previous moves strings from each node
        ignoring the very first one
        '''
        for node in islice(self.path_from_source(), 1, None):
            print(node.prevmove)
from itertools import islice

# INSTRUCTION FORMAT STRINGS -----------------------
MOVE_FORMAT = "MOVE from {} to {}."
JUMP_FORMAT = "JUMP from {} to {}."
EXIT_FORMAT = "EXIT from {}."
# --------------------------------------------------

class Node():
    '''
    Node for searching through different states
    Attributes:
        state: a tuple of coordinates of the player's pieces
        cost: the number of moves taken to enter the state
        heu: a heuristic value giving a lower bound
                on the number of moves needed to reach the goal state
        parent: the node from which this node was expanded
        prev_action : a string describing the move transitioning parent.state to self.state
    '''

    def __init__(self, state, cost, heu, parent, prev_action):
        self.state = state
        self.cost = cost
        self.heu = heu
        self.parent = parent
        self.prev_action = prev_action

    def __hash__(self):
        # use relevant componenents for hashing, ignoring the parent node to avoid
        # to avoid recursive calls to __hash__
        return hash((self.state, self.cost, self.heu))
    
    # -------------------------------------------------------------------------
    # Node comparison for sorting
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
    # -------------------------------------------------------------------------

    def expand(self, board):
        '''
        generates nodes containing adjacent states which are 1 move away from self.state
        on the board
        '''
        for adj_state, action in board.adj_state_actions(self.state):
            yield Node(
                    state=       adj_state,
                    cost=        self.cost+1,
                    heu=         board.state_heu(adj_state),
                    parent=      self,
                    prev_action= action)

    def path_from_source(self):
        '''returns an iterator over the nodes leading up to the current node'''
        if self.parent != None:
            yield from self.parent.path_from_source()
        yield self

    def print_instructions(self):
        '''
        print the instructions to transition from the start node to goal node
        '''
        # ignore previous action of start node (it don't exist)
        for node in islice(self.path_from_source(), 1, None):
            action_type, action_coords = node.prev_action
            instruction = { "MOVE": MOVE_FORMAT.format(*action_coords),
                            "JUMP": JUMP_FORMAT.format(*action_coords),
                            "EXIT": EXIT_FORMAT.format(action_coords),
                            "PASS": "PASS"}[action_type]

            print(instruction)
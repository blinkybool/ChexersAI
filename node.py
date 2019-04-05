from collections import namedtuple  

preNode = namedtuple("preNode", ['state', 'cost', 'heu', 'parent', 'prevmove'])

class Node(preNode):

    def __hash__(self):
        return hash((self.state.pieces, self.cost, self.heu))

    def isgoal(self):
        return not bool(self.state)
    
    # defines how a node should be prioritised for a priority queue.
    # since we are using A*, nodes are ordered based on cost + heuristic
    # def __eq__(self, other):
    #     return (self.cost + self.heu) == (other.cost + other.heu)

    # def __ne__(self, other):
    #     return (self.cost + self.heu) != (other.cost + other.heu)

    def __lt__(self, other):
        return (self.cost + self.heu) < (other.cost + other.heu)

    def __le__(self, other):
        return (self.cost + self.heu) <= (other.cost + other.heu)

    def __gt__(self, other):
        return (self.cost + self.heu) > (other.cost + other.heu)

    def __ge__(self, other):
        return (self.cost + self.heu) >= (other.cost + other.heu)

    def expand(self, board):
        for newstate, movestring in board.new_states(self.state):
            yield Node(newstate, self.cost+1, newstate.get_heu(board), self, movestring)

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
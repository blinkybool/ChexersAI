from collections import namedtuple  

preNode = namedtuple("preNode", ['state', 'cost', 'heu', 'parent', 'prevmove'])

class Node(preNode):

    def __hash__(self):
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
        for adj_state, movestring in board.adj_states(self.state):
            yield Node(state=adj_state, cost=self.cost+1, heu=board.state_heu(adj_state), parent=self, prevmove=movestring)

    def get_state_path(self):
        if self.parent != None:
            yield from self.parent.get_state_path()
        yield self.state

    def print_path(self):
        if self.parent is not None:
            self.parent.print_path()
            print(self.prevmove)

    def print_path_boards(self,board):
        if self.parent is not None:
            self.parent.print_path_boards(board)
        print(board.format_with_state(self.state, message=f"c={self.cost} + h={self.heu} == {self.cost+self.heu}"))
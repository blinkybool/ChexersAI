

class Heap():
    
    def __init__(self, heap_list=[]):
        self.heap = heap_list
        self.finder = {heap[i]: i for i in range(heap)}
    
    def __contains__(self, item):
        return self.finder.__contains__(item)

    def __index(self, item):
        return self.finder[item]

    def update_key_bigger(self, item):
        pos = self.__siftdown(0, self.__index(item))
        self.finder[item] = pos
    
    def update_key_smaller(self, item):
        pos = self.__siftup(0, self.__index(item))
        self.finder[item] = pos
    
    def push(self, item):
        self.heap.append(item)
        pos = self.__siftdown(0, len(heap)-1)

    def __siftdown(self, startpos, pos):
        newitem = self.heap[pos]
        # Follow the path to the root, moving parents down until finding a place
        # newitem fits.
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self.heap[parentpos]
            if newitem < parent:
                self.heap[pos] = parent
                pos = parentpos
                continue
            break
        self.heap[pos] = newitem
        return pos

    def __siftup(self, pos):
        endpos = len(heap)
        startpos = pos
        newitem = self.heap[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2*pos + 1    # leftmost child position
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not self.heap[childpos] < self.heap[rightpos]:
                childpos = rightpos
            # Move the smaller child up.
            self.heap[pos] = self.heap[childpos]
            pos = childpos
            childpos = 2*pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self.heap[pos] = newitem
        self.__siftdown(startpos, pos)

        
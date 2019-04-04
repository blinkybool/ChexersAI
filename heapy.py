

class Heap():
    
    def __init__(self):
        self.heap = []
        self.heapmap = {self[i]: i for i in range(len(self))}
    
    def __len__(self):
        return self.heap.__len__()
    
    def __bool__(self):
        return len(self.heap) != 0

    def __contains__(self, item):
        return self.heapmap.__contains__(item)
    
    def index(self, item):
        return self.heapmap[item]

    def __getitem__(self, key):
        return self.heap.__getitem__(key)

    def __setitem__(self, key, item):
        self.heap[key] = item
        self.heapmap[item] = key

    def update_key_bigger(self, item):
        self.__siftdown(0, self.heapmap[item])
    
    def update_key_smaller(self, item):
        self.__siftup  (0, self.heapmap[item])

    def replace(self, item, newitem):
        pos = self.heapmap.pop(item)
        self[pos] = newitem
        if item < newitem:
            self.__siftdown(0,pos)
        elif newitem > item:
            self.__siftup(pos)
    
    def push(self, item):
        if item in self:
            print("ah fuck don't do that")
            exit()
        
        self.heap.append(item)
        lastpos = len(self) - 1
        self.heapmap[item] = lastpos
        self.__siftdown(0, lastpos)

    def pop(self):
        """Pop the smallest item off the heap, maintaining the heap invariant."""
        lastelt = self.heap.pop()    # raises appropriate IndexError if heap is empty
        del self.heapmap[lastelt]
        if self.heap:
            returnitem = self[0]
            del self.heapmap[returnitem]
            self[0] = lastelt
            self.__siftup(0)
            return returnitem
            
        return lastelt

    def __siftdown(self, startpos, pos):
        newitem = self[pos]
        # Follow the path to the root, moving parents down until finding a place
        # newitem fits.
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self[parentpos]
            if newitem < parent:
                self[pos] = parent
                pos = parentpos
                continue
            break
        self[pos] = newitem

    def __siftup(self, pos):
        endpos = len(self)
        startpos = pos
        newitem = self[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2*pos + 1    # leftmost child position
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not self[childpos] < self[rightpos]:
                childpos = rightpos
            # Move the smaller child up.
            self[pos] = self[childpos]
            pos = childpos
            childpos = 2*pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self[pos] = newitem
        self.__siftdown(startpos, pos)

if __name__ == "__main__":
    myheap = Heap()
    myheap.push(8)
    myheap.push(5)
    myheap.push(3)
    myheap.push(10)
    myheap.push(6)
    myheap.push(2)

    print(myheap.heap)
    print(myheap.heapmap)
    print(myheap.pop())

    print(myheap.heap)
    print(sorted(myheap.heapmap.items(), key=lambda x: x[::-1]))
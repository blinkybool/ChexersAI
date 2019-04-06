print((10190234023409234098234098234098432098,).__sizeof__())
print(int(10190234023409234098234098234098432098).__sizeof__())
print((1,2,3,4,5,6,7,8,9,10,11).__sizeof__())

thing = [5,3,4,2,1]
myheapq.heapify(thing)
print(thing)
x = 2.5
print(f"{x} is at {myheapq.heappush(thing, x)}")
print(thing)
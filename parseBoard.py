import json
import search

coordmap =[ [ 0,-3],[ 1,-3],[ 2,-3],[ 3,-3],
        [-1,-2],[ 0,-2],[ 1,-2],[ 2,-2],[ 3,-2],
    [-2,-1],[-1,-1],[ 0,-1],[ 1,-1],[ 2,-1],[ 3,-1],
[-3, 0],[-2, 0],[-1, 0],[ 0, 0],[ 1, 0],[ 2, 0],[ 3, 0],
    [-3, 1],[-2, 1],[-1, 1],[ 0, 1],[ 1, 1],[ 2, 1],
        [-3, 2],[-2, 2],[-1, 2],[ 0, 2],[ 1, 2],
            [-3, 3],[-2, 3],[-1, 3],[ 0, 3] ]

inputStr = '''
    - - - -
   X - - X X 
  X X X X X -   
 - X - - X X X
  - X x - X X   
   x X X - X 
    R - - X
'''[1:-1].replace(" ",'').replace("\n",'')


jthing = {'colour': 'red', 'pieces': [], 'blocks': []}

for i in range(len(inputStr)):
    if inputStr[i] in "RGB":
        jthing["pieces"].append(coordmap[i])
    elif inputStr[i] in "Xx":
        jthing["blocks"].append(coordmap[i])
    elif inputStr[i] != '-':
        print("fuck")




testname = "customtest.json"

with open(testname, 'w') as fp:
    json.dump(jthing, fp)

if __name__ == "__main__":
    search.main()
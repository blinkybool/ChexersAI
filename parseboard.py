import json

'''
Generate test case boards
'''
# Pick player - (use same letter for board design)

PLAYER = 'red'
# PLAYER = 'green'
# PLAYER = 'blue'

# Design the board

board = \
'''
    - - - -
   - - - - - 
  - - - - - -   
 - - - - - - -
  - - - - - -   
   - - - - - 
    R R R R
'''

########################################################

boardcoords = \
(           ( 0,-3),( 1,-3),( 2,-3),( 3,-3),
        (-1,-2),( 0,-2),( 1,-2),( 2,-2),( 3,-2),
    (-2,-1),(-1,-1),( 0,-1),( 1,-1),( 2,-1),( 3,-1),
(-3, 0),(-2, 0),(-1, 0),( 0, 0),( 1, 0),( 2, 0),( 3, 0),
    (-3, 1),(-2, 1),(-1, 1),( 0, 1),( 1, 1),( 2, 1),
        (-3, 2),(-2, 2),(-1, 2),( 0, 2),( 1, 2),
            (-3, 3),(-2, 3),(-1, 3),( 0, 3)            )

PLAYER_TILES = "rgbRGB"
BLOCK_TILES = "xX"
EMPTY_TILE = '-'

def parseboard():
    
    template = {'colour': PLAYER, 'pieces': [], 'blocks': []}

    for tile, coord in zip(board.split(),boardcoords):
        if tile in PLAYER_TILES:
            template["pieces"].append(coord)
        elif tile in BLOCK_TILES:
            template["blocks"].append(coord)
        elif tile != EMPTY_TILE:
            print("bad parse")

    return template


'''Graveyard'''
'''
    - - - -
   X - - X X 
  X X X X X -   
 - X - - X X X
  - X x - X X   
   x X X - X 
    R - - X
'''
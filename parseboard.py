import json, sys, os
'''
Generates board configurations from a board text file
'''

DEFAULT_BOARD_FILENAME = "defaultboard.txt"

# Pick player - (use same letter for board design)
PLAYER = 'red'
# PLAYER = 'green'
# PLAYER = 'blue'

##############################################################################

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

def parseboard(input_board_filename=DEFAULT_BOARD_FILENAME):
    
    template = {'colour': PLAYER, 'pieces': [], 'blocks': []}

    with open(input_board_filename) as board:
        for tile, coord in zip(board.read().split(), boardcoords):
            if tile in PLAYER_TILES:
                template["pieces"].append(coord)
            elif tile in BLOCK_TILES:
                template["blocks"].append(coord)
            elif tile != EMPTY_TILE:
                print("bad parse", file=sys.stderr)

    return template

if __name__ == "__main__":

    if len(sys.argv)==1:
        input_file = DEFAULT_BOARD_FILENAME
    elif len(sys.argv)==2:
        input_file = sys.argv[1]
    else:
        print("# bad input", file=sys.stderr)

    # Dump the board config textfile into a json file
    with open(input_file.split()[0]+".json", 'w') as fp:
        json.dump(parseboard(input_file), fp)
import json, sys
'''
Generate test case boards
'''

BOARD_INPUT_FILENAME = "boardinput.txt"

# Pick player - (use same letter for board design)
PLAYER = 'red'
# PLAYER = 'green'
# PLAYER = 'blue'

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

    with open(BOARD_INPUT_FILENAME) as board:
        for tile, coord in zip(board.read().split(), boardcoords):
            if tile in PLAYER_TILES:
                template["pieces"].append(coord)
            elif tile in BLOCK_TILES:
                template["blocks"].append(coord)
            elif tile != EMPTY_TILE:
                print("bad parse", file=sys.stderr)

    return template

if __name__ == "__main__":
    assert len(sys.argv)==2 and "Need 1 argument (file name for output)"

    # Dump the board config into a json file
    with open(sys.argv[1], 'w') as fp:
        json.dump(parseboard(), fp)
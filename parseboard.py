import json, sys, os
'''
Generates board configurations from a board text file
'''

DEFAULT_BOARD_TEXT_FILE = "defaultboard.txt"

# Pick player - (use same letter for board design)
PLAYER = 'red'
# PLAYER = 'green'
# PLAYER = 'blue'

##############################################################################

boardcoords = (
            ( 0,-3),( 1,-3),( 2,-3),( 3,-3),
        (-1,-2),( 0,-2),( 1,-2),( 2,-2),( 3,-2),
    (-2,-1),(-1,-1),( 0,-1),( 1,-1),( 2,-1),( 3,-1),
(-3, 0),(-2, 0),(-1, 0),( 0, 0),( 1, 0),( 2, 0),( 3, 0),
    (-3, 1),(-2, 1),(-1, 1),( 0, 1),( 1, 1),( 2, 1),
        (-3, 2),(-2, 2),(-1, 2),( 0, 2),( 1, 2),
            (-3, 3),(-2, 3),(-1, 3),( 0, 3))

PLAYER_TILES = "rgbRGB"
BLOCK_TILES = "xX"
EMPTY_TILE = '-'

def parseboardinput():

    if len(sys.argv)==1:
        # Get the default board config returned by parseboard
        board_text_file = DEFAULT_BOARD_TEXT_FILE

    elif len(sys.argv)==2:

        try:
            # determine if the input is a txt file or json file
            board_file = sys.argv[1]
            file_ext = os.path.splitext(board_file)[1]

            if file_ext == ".json":
                with open(board_file) as file_data:
                    return json.load(file_data)
            else:
                board_text_file = board_file
        except:
            print("# bad input", file=sys.stderr)
            exit()
    else:
        print("# too many arguments (expected up to 1)", file=sys.stderr)
        exit()
    
    template = {'colour': PLAYER, 'pieces': [], 'blocks': []}

    with open(board_text_file) as board_text:
        for tile, coord in zip(board_text.read().split(), boardcoords):
            if tile in PLAYER_TILES:
                template["pieces"].append(coord)
            elif tile in BLOCK_TILES:
                template["blocks"].append(coord)
            elif tile != EMPTY_TILE:
                print("bad parse", file=sys.stderr)

    return template
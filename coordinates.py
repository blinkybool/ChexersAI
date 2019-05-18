RADIUS = 3
RED = "red"
GREEN = "green"
BLUE = "blue"
PLAYERS = (RED, GREEN, BLUE)
OPPONENTS = {RED: (GREEN,BLUE), GREEN: (BLUE, RED), BLUE: (RED, GREEN)}
NUM_PLAYERS = len(PLAYERS)

def _coordinates():
    ran = range(-RADIUS,RADIUS+1)
    return tuple((q,r) for q in ran for r in ran if (-q-r) in ran)

def is_valid_coord(coord):
    return -RADIUS <= min(coord) and max(coord) <= RADIUS and abs(sum(coord)) <= RADIUS

def _move_jump_neighbours(coord):
    q,r = coord
    movecoords = \
        (( q ,r-1),(q+1,r-1),
    (q-1, r )    ,    (q+1, r ),
        (q-1,r+1),( q ,r+1))

    # all coords within jumping distance
    jumpcoords = \
        (( q ,r-2),(q+2,r-2),
    (q-2, r )    ,    (q+2, r ),
        (q-2,r+2),( q ,r+2))

    neighbours = zip(movecoords, jumpcoords)
    return tuple((movecoord, jumpcoord) if is_valid_coord(jumpcoord) else (movecoord, None) for movecoord, jumpcoord in neighbours if is_valid_coord(movecoord))

def _opposing_neighbour_pairs(coord):
    q, r = coord
    pairs =(((q,r-1),(q,r+1)),
            ((q-1,r),(q+1,r)),
            ((q-1,r+1),(q+1,r-1)))

    for coord1, coord2 in pairs:
        if is_valid_coord(coord1):
            if is_valid_coord(coord2):
                yield (coord1, coord2)
            else:
                yield (coord1, None)
        elif is_valid_coord(coord2):
            yield (None, coord2)

def coord_dist(coord1, coord2):
    x1,y1 = coord1
    x2,y2 = coord2

    return max(abs(x1-x2), abs(y1-y2), abs((-x1-y1) - (-x2-y2)))

def coord_between(coord1, coord2):
    return ((coord1[0] + coord2[0])//2, (coord1[1] + coord2[1])//2)

COORDINATES = _coordinates()
ALL_NEIGHBOURS = {coord: tuple(_move_jump_neighbours(coord)) for coord in COORDINATES}
OPPOSING_NEIGHBOUR_PAIRS = {coord: tuple(_opposing_neighbour_pairs(coord)) for coord in COORDINATES}

START_COORDS = {RED:    set(coord for coord in COORDINATES if    coord[0] == -RADIUS),
                GREEN:  set(coord for coord in COORDINATES if    coord[1] == -RADIUS),
                BLUE:   set(coord for coord in COORDINATES if -sum(coord) == -RADIUS)}

NUM_STARTING_PIECES = len(START_COORDS[PLAYERS[0]])

EXIT_COORDS = {RED:     frozenset(coord for coord in COORDINATES if coord[0]==RADIUS),
                GREEN:  frozenset(coord for coord in COORDINATES if coord[1]==RADIUS),
                BLUE:   frozenset(coord for coord in COORDINATES if -sum(coord)==RADIUS)}

EXIT_DIST = {player: 
                {coord: min(coord_dist(coord, exit_coord) for exit_coord in EXIT_COORDS[player]) for coord in COORDINATES}
                    for player in PLAYERS}

class PlayerDict(dict):
    _keys = PLAYERS
    def __init__(self, valtype=set):
        if valtype is None:
            valtype = lambda _: None
        self[RED] = valtype()
        self[GREEN] = valtype()
        self[BLUE] = valtype()

    def __setitem__(self, key, value):
        if key not in PlayerDict._keys:
            raise KeyError
        return super().__setitem__(key, value)
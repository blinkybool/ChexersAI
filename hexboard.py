import json
from collections import defaultdict
from enum import Enum

RADIUS = 3


class Tile(Enum):
    BLANK = 0
    RED = 1
    GREEN = 2
    BLUE = 3


class HexBoard():

    def __init__(self, start_config_file="", radius=RADIUS):
        self.radius = radius
        self.tiles = dict()
        self.pieces = set()
        for q in range(-self.radius, self.radius+1):
            # q+r+s = 0
            # r = -q - s
            # -q-size <= r <= -q + size
            low = max(- q - self.radius, -self.radius)
            hih = min(- q + self.radius,  self.radius)
            for r in range(low, hih+1):
                self[q, r] = Tile.BLANK

        if start_config_file:
            with open(start_config_file) as start_config_json:
                start_config = json.load(start_config_json)
                self.pieces = start_config["pieces"]

    def __getitem__(self, key):
        return self.tiles.__getitem__(key)

    def __setitem__(self, key):
        return self.tiles.__setitem__(key)

    def iter_coords(self):
        for q in range(-self.radius, self.radius+1):
            # q+r+s = 0
            # r = -q - s
            # -q-size <= r <= -q + size
            low = max(- q - self.radius, -self.radius)
            hih = min(- q + self.radius,  self.radius)
            for r in range(low, hih+1):
                yield (q, r)


def main():
    HexBoard("test.json")


if __name__ == '__main__':
    main()

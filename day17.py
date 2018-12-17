"""AoC 2018 Day 17: Reservoir Research"""

import re
from itertools import repeat
from operator import itemgetter
from collections import Counter

# Part 1


class Ground():
    def __init__(self, coordinates):
        clay_dict, min_y, max_y = Ground.parse_input(coordinates)
        self.ground = clay_dict
        self.min_y = min_y
        self.max_y = max_y
        self.current = (500, min_y)

    def __repr__(self):
        return f'Ground from y={self.min_y} to y={self.max_y}'

    def __str__(self):
        x_min = min(x for x, y in self.ground)
        x_max = max(x for x, y in self.ground)
        lines = []
        for y in range(self.min_y, self.max_y + 1):
            line = ''
            for x in range(x_min, x_max + 1):
                line += self.ground.get((x, y), '.')
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def parse_input(coordinates):
        clay = []
        reg = re.compile(r'(\d+)')
        for line in coordinates.splitlines():
            coord = [int(i) for i in reg.findall(line)]
            if line[0] == 'x':
                clay.extend(zip(repeat(coord[0]),
                                range(coord[1], coord[2] + 1)))
            else:
                clay.extend(zip(range(coord[1], coord[2] + 1),
                                repeat(coord[0])))
        clay.sort(key=itemgetter(1))
        span_y = clay[0][1], clay[-1][1]
        return [dict.fromkeys(clay, '#'), *span_y]

    def count_water(self):
        count = Counter(self.ground.values())
        return count['|'] + count['~']

    def spill_down(self, coord):
        """
        coord=(x, y). Goes down from coord until it reaches clay (#) or max_y
        """
        x, y = coord
        while True:
            if y == self.max_y:
                return (x, y)
            y += 1
            if self.ground.get((x, y), '') == "#":
                self.ground[(x, y - 1)] = "~"
                break
            self.ground[(x, y)] = '|'
        return (x, y - 1)

    def spread(self, coord):
        """
        coord=(x,y). Spread to the left and right until impossible. Returns the
        values x_min and x_max that were reached.
        """
        x0, y = coord
        self.ground[x0, y] = '~'
        wall_left, wall_right = False, False
        # To the left
        x = x0
        while self.ground.get((x, y + 1), '') in ["#", '~']:
            x -= 1
            if self.ground.get((x, y), '') == "#":
                wall_left = True
                break
            self.ground[x, y] = "~"
        x_min = x + 1
        # To the right
        x = x0
        while self.ground.get((x, y + 1), '') in ["#", '~']:
            x += 1
            if self.ground.get((x, y), '') == "#":
                wall_right = True
                break
            self.ground[x, y] = "~"
        x_max = x - 1
        keep_up = True
        if wall_left and wall_right:
            return (x0, y - 1), keep_up
        if not wall_left and not wall_right:
            return (x_min - 1, y), (x_max + 1, y), not keep_up
        if wall_left and not wall_right:
            return (x_max + 1, y), not keep_up
        if wall_right and not wall_left:
            return (x_min - 1, y), not keep_up

    def fill_up(self, coord):
        """
        Fills the lines up until it can go down somewhere. Returns this coord
        """
        x0, y0 = coord
        keep_up = True
        while keep_up:
            try:
                coord, keep_up = self.spread(coord)
            except ValueError:
                coord_left, coord_right, keep_up = self.spread(coord)
                return [coord_left, coord_right]
        return coord

    def flow_water(self, coord=None):
        """
        The waters drops from start (with y augmenting). It is blocked by the
        clay at coords specified by clay_dict. If it reaches some clay, it
        spreads to the sides. When it reaches some clay again, it goes up. Then
        it spills to the sides.
        """
        if coord is None:
            coord = (500, self.min_y - 1)
        while True:
            coord = self.spill_down(coord)
            if coord[1] == self.max_y:
                break
            coord = self.fill_up(coord)
            # If coord is a tuple, there is only one place to go down again
            if type(coord) == tuple:
                continue
            coord0, coord1 = coord
            # print(str(self.ground))
            self.flow_water(coord0)
            self.flow_water(coord1)
            break


with open("day17_input.txt") as f:
    day = f.read()

test_coords = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

test_ground = Ground(test_coords)
test_ground.flow_water()
print(test_ground)
print(test_ground.count_water())

ground = Ground(day)
ground.flow_water()
print(f'Solution for part 1: {ground.count_water()}')

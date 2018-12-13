"""Aoc 2018 Day 13: Mine Cart Madness"""

from itertools import cycle
from collections import Counter, deque

# Part 1


class Cart():
    """
    Class for carts. Provides access to coordinates, next move and next
    intersection.
    """
    def __init__(self, X, Y, init_status):
        self.X = X
        self.Y = Y
        self.next_cross = cycle(['left', 'straight', 'right'])
        self.status = init_status

    def __repr__(self):
        return f'X: {self.X}, Y: {self.Y}, status: {self.status}'

    def turn(self, direction):
        turn_left  = {'>': '^', '^': '<', '<': 'v', 'v': '>'}  # noqa
        turn_right = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
        if direction == "left":
            self.status = turn_left[self.status]
        if direction == "right":
            self.status = turn_right[self.status]

    def move(self, grid):
        if self.status == ">":
            self.X += 1
        elif self.status == "<":
            self.X -= 1
        elif self.status == "^":
            self.Y -= 1
        elif self.status == "v":
            self.Y += 1
        # After moving, check status
        next_grid = grid[(self.X, self.Y)]
        # 1st case, the cart keeps going
        if next_grid == "-" and self.status in ["<", ">"]:
            pass
        elif next_grid == "|" and self.status in ['v', '^']:
            pass
        # 2nd case, the cart hits a curve
        elif (next_grid, self.status) in [('/', '<'), ('\\', 'v'),
                                          ('/', '>'), ('\\', '^')]:
            self.turn("left")
        elif (next_grid, self.status) in [('/', '^'), ('\\', '<'),
                                          ('/', 'v'), ('\\', '>')]:
            self.turn("right")
        # Finally, the cart reaches an intersection
        elif next_grid == "+":
            next_cross = next(self.next_cross)
            self.turn(next_cross)


class Grid(object):
    def __init__(self, input):
        grid = dict()
        carts = []
        raw_grid = input.splitlines()
        for y, line in enumerate(raw_grid):
            for x, elem in enumerate(line):
                if elem in ['/', '-', '\\', '|', '+']:
                    grid[(x, y)] = elem
                elif elem in ['>', '<']:
                    carts.append(Cart(x, y, elem))
                    grid[(x, y)] = '-'
                elif elem in ['^', 'v']:
                    carts.append(Cart(x, y, elem))
                    grid[(x, y)] = '|'
        self.grid = grid
        self.carts = carts
        self.num_carts = len(carts)

    def __repr__(self):
        return (f'Grid object spanning to x={max(k[0] for k in self.grid)}'
                f' and y={max(k[1] for k in self.grid)} with {len(self.carts)}'
                f' carts')

    def move_all_carts_once(self):
        coords_cart = deque()
        for i, cart in enumerate(self.carts):
            cart.move(self.grid)
            coords_cart.append((cart.X, cart.Y))
        if len(set(coords_cart)) != len(coords_cart):
            # Collision
            raise StopIteration

    def move_until_crash(self):
        while True:
            try:
                self.move_all_carts_once()
            except StopIteration:
                print('Crash!')
                break
        coords_cart = Counter([(cart.X, cart.Y) for cart in self.carts])
        return coords_cart.most_common(1)[0][0]


# GRID = r"""/->-\        
# |   |  /----\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/   
# """

# test_grid = Grid(GRID)

# print(test_grid.move_until_crash())

with open("day13_input.txt") as f:
    day13 = f.read()

grid = Grid(day13)
crash_coord = grid.move_until_crash()

print(f'Solution for part 1: {crash_coord}')

"""Aoc 2018 Day 13: Mine Cart Madness"""

from itertools import cycle

# Part 1


class Cart():
    """
    Class for carts. Provides access to coordinates, next move and next
    intersection.
    """
    def __init__(self, name, X, Y, init_status):
        self.name = name
        self.X = X
        self.Y = Y
        self.next_cross = cycle(['left', 'straight', 'right'])
        self.status = init_status

    def __repr__(self):
        return f'{self.name}, X:{self.X}, Y:{self.Y}, status: {self.status}'

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
        coords_carts = set()
        i = 0
        raw_grid = input.splitlines()
        for y, line in enumerate(raw_grid):
            for x, elem in enumerate(line):
                if elem in ['/', '-', '\\', '|', '+']:
                    grid[(x, y)] = elem
                elif elem in ['>', '<']:
                    carts.append(Cart(i, x, y, elem))
                    i += 1
                    coords_carts.add((x, y))
                    grid[(x, y)] = '-'
                elif elem in ['^', 'v']:
                    carts.append(Cart(i, x, y, elem))
                    i += 1
                    coords_carts.add((x, y))
                    grid[(x, y)] = '|'
        self.grid = grid
        self.carts = carts
        self.coords_cart = coords_carts

    def __repr__(self):
        return (f'Grid object spanning to x={max(k[0] for k in self.grid)}'
                f' and y={max(k[1] for k in self.grid)} with {len(self.carts)}'
                f' carts')

    def move_all_carts_once(self, stop_first_crash=True):
        carts_to_remove = set()
        for cart in sorted(self.carts, key=lambda c: (c.X, c.Y)):
            if cart.name in carts_to_remove:
                continue
            self.coords_cart.remove((cart.X, cart.Y))
            cart.move(self.grid)
            new_coord = cart.X, cart.Y
            if new_coord in self.coords_cart:
                if stop_first_crash:
                    return new_coord
                for cart2 in self.carts:
                    if (cart2.X, cart2.Y) == new_coord:
                        carts_to_remove.add(cart2.name)
                self.coords_cart.remove(new_coord)
            else:
                self.coords_cart.add(new_coord)
        self.carts = [
            cart
            for cart in self.carts
            if cart.name not in carts_to_remove
        ]
        return False

    def move_until_crash(self, stop_first_crash=True):
        crash = False
        while not crash:
            crash = self.move_all_carts_once(stop_first_crash)
        print(f'Crash! At {crash}')
        return crash

    def move_until_last(self):
        while len(self.carts) > 1:
            self.move_all_carts_once(stop_first_crash=False)
        return self.carts[0].X, self.carts[0].Y


with open("day13_input.txt") as f:
    day13 = f.read()

grid = Grid(day13)
crash_coord = grid.move_until_crash()

print(f'Solution for part 1: {crash_coord}')
# 108,60

# Part 2
# We now want to know the coord of the last remaining cart after all the other
# have crashed. I update the Grid class above.

grid = Grid(day13)
print(f'Soluton for part 2: {grid.move_until_last()}')

"""AoC 2018 Day 15: Beverage Bandits"""

from itertools import count
import numpy as np

# Part 1


class Unit():
    elves_count = count()
    goblins_count = count()

    def __init__(self, race, x, y):
        self.race = race  # Elf or Goblin
        self.x = x  # x position on the grid (left to right, 0 is left)
        self.y = y  # y position on the grid (top to bottom, 0 is top)
        self.hp = 200  # Hit points
        self.ap = 3  # Attack power
        if self.race == "Elf":
            self.id = next(Unit.elves_count)
        else:
            self.id = next(Unit.goblins_count)

    def __repr__(self):
        return (f'{self.race} {self.id} with {self.hp} hp and {self.ap} attack'
                f' power at x={self.x}, y={self.y}')


class Grid():
    def __init__(self, input):
        elves = []
        goblins = []
        raw_grid = input.splitlines()
        grid = np.empty(shape=(len(raw_grid[0]), len(raw_grid)), dtype='<U1')
        for y, line in enumerate(raw_grid):
            for x, elem in enumerate(line):
                grid[x, y] = elem
                if elem == "E":
                    elves.append(Unit("Elf", x, y))
                if elem == "G":
                    goblins.append(Unit("Goblin", x, y))
        self.grid = grid
        self.elves = elves
        self.goblins = goblins


#Targets:      In range:     Reachable:    Nearest:      Chosen:
 #######       #######       #######       #######       #######
 #E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
 #...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
 #.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
 #######       #######       #######       #######       #######


grid_test = """#######
#E..G.#
#...#.#
#.G.#G#
#######"""

g = Grid(grid_test)


def gen_target_range(grid, target_race):
    indices = sorted(zip(*np.where(grid == target_race)),
                     key=lambda x: (x[1], x[0]))
    for x, y in indices:
        # In reading order
        for a in [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]:
            if grid[a] == '.':
                yield a


print([a for a in gen_target_range(g.grid, "G")])

g2 = Grid("""#######
#.G...#
#..G..#
#.#.#G#
#..G#E#
#.....#
#######""")


def is_reachable(grid, ind_from, ind_to):
    x_0, y_0 = ind_from
    x_1, y_1 = ind_to
    for x in range(min(x_0, x_1), max(x_0, x_1)):
        if np.all(grid[x, :] != '.'):
            return False
    for y in range(min(y_0, y_1), max(y_0, y_1)):
        if np.all(grid[:, y] != '.'):
            return False
    return True

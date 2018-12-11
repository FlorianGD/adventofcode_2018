"""AoC 2018 Day 11: Chronal Charge"""

import numpy as np
from tqdm import tqdm

# Part 1


def cell_power(x, y, grid_serial):
    rack_id = x + 10
    power = rack_id * y
    power += grid_serial
    power *= rack_id
    # get the third digit if any
    power //= 100
    power %= 10
    power -= 5
    return power


def grid_power(grid_serial, size=300):
    grid = np.zeros(shape=(size + 1, size + 1), dtype=np.int64)
    for x in range(1, size + 1):
        for y in range(1, size + 1):
            grid[x, y] = cell_power(x, y, grid_serial)
    return grid

# Another option would be
# grid = np.fromfunction(cell_power, (301, 301), dtype=np.int64,
#                        grid_serial=grid_serial)
# This differs with the 0th row and column only (but we don't care if these)


def squares_power(grid_serial, size=300):
    cells = grid_power(grid_serial, size)
    squares = np.zeros(shape=(size, size), dtype=np.int64)
    for x in range(1, size - 2):
        for y in range(1, size - 2):
            squares[x, y] = np.sum(cells[x:x+3, y:y+3])
    return squares


def which_max(array):
    return np.unravel_index(np.argmax(array), array.shape)


# assert which_max(squares_power(42)) == (21, 61)
# assert which_max(squares_power(18)) == (33, 45)

print(f'Solution for part 1: {which_max(squares_power(9995))}')

# Part 2
# I try a naive solution, that is working but quite slow (less than day9 part
# 2 though). It takes roughly 3 minutes to compute all masks. There must be
# a better numpy solution.


def squares_power(grid_serial, cells, square_size=3, size=300):
    squares = np.zeros(shape=(size, size), dtype=np.int64)
    for x in range(1, size - square_size + 1):
        for y in range(1, size - square_size + 1):
            squares[x, y] = np.sum(cells[x:x+square_size, y:y+square_size])
    return squares


def max_and_which_max(array):
    return np.max(array), np.unravel_index(np.argmax(array), array.shape)


def max_all_squares(grid_serial, size=300):
    mmax = 0
    imax = 0
    cells = grid_power(grid_serial, size)
    for i in tqdm(range(1, size + 1)):
        m, ind = max_and_which_max(squares_power(grid_serial, cells,
                                                 square_size=i))
        if m > mmax:
            imax = i
            indmax = ind
            mmax = m
    return (*indmax, imax)


print(f'Solution for part 2:{max_all_squares(9995)}')

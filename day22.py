"""AoC 2018 Day 22: Mode Maze"""

from functools import lru_cache
from tqdm import trange
# from numba import jit
# Part 1

DEPTH = 3339
TARGET = 10, 715

# The region at the coordinates of the target has a geologic index of 0.
# The region at 0,0 (the mouth of the cave) has a geologic index of 0.
# If the region's Y coordinate is 0, the geologic index is its X coordinate
# times 16807.
# If the region's X coordinate is 0, the geologic index is its Y coordinate
# times 48271.
# Otherwise, the region's geologic index is the result of multiplying the
# erosion levels of the regions at X-1,Y and X,Y-1.


@lru_cache(maxsize=None)
def geo_index(coord, target=TARGET, depth=DEPTH):
    x, y = coord
    if coord == target:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return (erosion_level((x-1, y), target, depth) *
                erosion_level((x, y-1), target, depth))


@lru_cache(maxsize=None)
def erosion_level(coord, target=TARGET, depth=DEPTH):
    return (geo_index(coord, target, depth) + depth) % 20183


def risk_level(target=TARGET, depth=DEPTH):
    xmax, ymax = target
    risk = 0
    for y in trange(ymax+1):
        for x in range(xmax+1):
            risk += erosion_level((x, y), target, depth) % 3
    return risk


assert risk_level(target=(10, 10), depth=510) == 114

print(f'\nSolution for part 1: {risk_level()}')

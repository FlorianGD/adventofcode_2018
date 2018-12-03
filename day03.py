"""Solutions for day 3 of AoC 2018"""

import re
import numpy as np

# Part 1
# I will use a numpy array to store the cells. O will be empty,
# 1 claimed once, and >=2 will represent overlap.

GRID = np.zeros((1000, 1000), dtype=np.int64)

PATTERN = r'@ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)'
COORDS = re.compile(PATTERN)


def parse_instructions(line, regex=COORDS):
    '''Parse a line of instructions'''
    m = regex.search(line)
    return int(m['left']), int(m['top']), int(m['width']), int(m['height'])


def read_input(file='day03_input.txt'):
    with open(file) as f:
        instr = f.readlines()
    return instr


def update_grid(grid=GRID, lines=read_input()):
    for line in lines:
        left, top, width, height = parse_instructions(line)
        grid[left:left+width, top:top+height] += 1
    return grid


def compute_overlap(grid):
    return np.sum(grid >= 2)


test_input = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
test_grid = np.zeros((8, 8), dtype=np.int64)
updated_test_grid = update_grid(grid=test_grid, lines=test_input)
assert compute_overlap(updated_test_grid) == 4

part_one_solution = compute_overlap(update_grid())
print(f'Solution for part 1: {part_one_solution}')

# Part 2
# Now we need to find the only id with no overlap.
# So, I need to change the regex to get the id also, and to change the update
# process as well.

PATTERN = r'(?P<id>\d+) @ (?P<l>\d+),(?P<t>\d+): (?P<w>\d+)x(?P<h>\d+)'
COORDS_ID = re.compile(PATTERN)


def parse_instructions_id(line, regex=COORDS_ID):
    '''Parse a line of instructions'''
    m = regex.search(line)
    return int(m['id']), int(m['l']), int(m['t']), int(m['w']), int(m['h'])


def find_non_overlap(grid=GRID, lines=read_input()):
    """
    The grid is already updated (it was updated in place with the first part)
    I will scan all the lines again and check if the subgrid has only ones.
    If so I will return the id.
    """
    for line in lines:
        id, left, top, width, height = parse_instructions_id(line)
        if np.all(grid[left:left+width, top:top+height] == 1):
            return id


assert find_non_overlap(grid=test_grid, lines=test_input) == 3

print(f'Solution for part 2: {find_non_overlap(grid=GRID)}')

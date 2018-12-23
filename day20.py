"""AoC 2018 Day 20: A Regular Map"""

import re
from collections import OrderedDict

import numpy as np

# Part 1


def reduce_path(path):
    new_path = ''
    # Find the innermost parenthesis group
    innermost = re.compile(r'(\([NSEW|]*?\))')
    previous_start = 0
    for m in innermost.finditer(path):
        new_path += path[previous_start:m.start()]
        # [1:-1] is to remove the parenthesis
        branches = m.group()[1:-1].split('|')
        if '' in branches:
            longuest_branch = ''
        else:
            longuest_branch = max(branches, key=len)
        new_path += longuest_branch
        previous_start = m.end()
    new_path += path[previous_start:]
    if previous_start == 0:
        return path
    else:
        return reduce_path(new_path)


a = reduce_path('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN')
b = reduce_path('ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))')
c = reduce_path('WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|S'
                'S))))')
assert len(a) == 18
assert len(b) == 23
assert len(c) == 31

with open('day20_input.txt') as f:
    day = f.readline()[1:-2]

reduced = reduce_path(day)
print(f'Solution for part 1: {len(reduced)}')

# Part 2


def find_rooms(path, start_length=0):
    rooms = OrderedDict()
    directions = {'N': np.array([0, 1]),
                  'S': np.array([0, -1]),
                  'E': np.array([1, 0]),
                  'W': np.array([-1, 0])}
    lengths_stack = [0]
    previous_start = [0]
    pos = np.array([0, 0])
    for direction in path:
        if pos in 'NSEW':
            lengths_stack[-1] += 1
            pos = pos + directions[direction]
            if pos not in rooms.keys():
                rooms[pos] = lengths_stack[-1]
        elif pos == '(':
            # branch, store starting point for the branch
            room_before_branch = rooms.items()[-1]
            previous_start.append(room_before_branch[0])
            lengths_stack.append(room_before_branch[1])
        elif pos == '|':
            # Get back to the starting point of the branch
            previous_start.pop()
            lengths_stack
        elif pos == ')':
            pass

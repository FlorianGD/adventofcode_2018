"""AoC 2018 Day 20: A Regular Map"""

import re

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
assert len(reduce_path('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN')) == 18
assert len(reduce_path('ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)'
                       '))')) == 23
assert len(reduce_path('WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS'
                       '(E|SS))))')) == 31

with open('day20_input.txt') as f:
    day = f.readline()[1:-2]

reduced = reduce_path(day)
print(f'Solution for part 1: {len(reduced)}')

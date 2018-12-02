"""Solutions for day 2 of 2018 AoC"""

from collections import Counter

# Part 1

with open('day02_input.txt') as f:
    day02 = f.readlines()


def checksum(input_list):
    twos, threes = 0, 0
    for id in input_list:
        counts = Counter(id).values()
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1
    return twos * threes


# Tests
test_input = [
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab'
]


assert checksum(test_input) == 12
print(f'Solution for part 1: {checksum(day02)}')

"""Solutions for day 2 of 2018 AoC"""

from collections import Counter
from itertools import permutations
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

# Part 2


def dist(str1, str2):
    """
    Returns the distance between two strings in term of number of
    different characters.
    Example:
        dist("abc", "dbc") == 1
        dist("abc", "def") == 3
    """
    return sum(a != b for a, b in zip(str1, str2))


def find_one_diff(input_list):
    """
    Look for 2 items in input where the distance is one
    """
    for a, b in permutations(input_list, 2):
        if dist(a, b) == 1:
            # Need to preserve order
            return ''.join(x for i, x in enumerate(a) if x == b[i])

test_input = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']

assert find_one_diff(test_input) == 'fgij'

print(f'Solution for part 2: {find_one_diff(day02)}')

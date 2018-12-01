'''Solutions for day_01'''

import numpy as np
from itertools import cycle
# Part one

# The inputs are integers, one on each row
day_01 = np.genfromtxt('day01_input.txt', dtype=np.int64)
first_result = np.sum(day_01)

print(f'Result for part one : {first_result}')

# Part 2

# We have to find repeated frequencies
# I will iterate through the cumulative sums
# I use itertools.cycle because it could
# The start is at 0


def find_repeated_freqs(day_01):
    seen_freqs = {0}
    current_freq = 0
    for freq in cycle(day_01):
        current_freq += freq
        if current_freq in seen_freqs:
            return(current_freq)
        else:
            seen_freqs.add(current_freq)

assert find_repeated_freqs([1, -2, 3, 1]) == 2
assert find_repeated_freqs([1, -1]) == 0
assert find_repeated_freqs([3, 3, 4, -2, -4]) == 10
assert find_repeated_freqs([-6, +3, +8, +5, -6]) == 5
assert find_repeated_freqs([+7, +7, -2, -7, -4]) == 14

second_result = find_repeated_freqs(day_01)

print(f'Result for part two : {second_result}')

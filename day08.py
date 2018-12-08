"""AoC 2018 Day 8"""

# Part 1

test_input = [int(i) for i in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()]
# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----


def sum_metadata(header):
    """
    Recursive function, returns the header, n_data and the sum of metadata
    """
    sum_meta = 0
    if not header:
        # Empty list
        return [], sum_meta
    n_data, n_meta, *child = header
    while n_data:
        child, new_meta = sum_metadata(child)
        sum_meta += new_meta
        n_data -= 1
    return child[n_meta:], sum_meta + sum(child[:n_meta])


assert sum_metadata(test_input)[1] == 138

with open("day08_input.txt") as f:
    day08 = [int(i) for i in f.read().split()]

print(f'Solution for part 1: {sum_metadata(day08)[1]}')

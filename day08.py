"""AoC 2018 Day 8"""

# Part 1

test_input = [int(i) for i in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()]
# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----


def sum_metadata(header):
    """
    Recursive function to sum the metadata
    """
    sum_meta = 0
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

# Part 2


def parse_dict(header):
    """
    parse the inpu as a dict, with child entries and a metadata_one
    """
    parsed = dict()
    n_data, n_meta, *child = header
    for i in range(1, n_data + 1):
        child, parsed[i] = parse_dict(child)
    parsed['metadata'] = child[:n_meta]
    return child[n_meta:], parsed


def compute_score(parsed):
    """
    If a node has no child node (len == 1), the score is the sum of the
    metadata, else the metadata are indexes of scores of child nodes. If an
    index does not exists, it is 0.
    """
    score = 0
    if len(parsed) == 1:
        # Only metadata
        score += sum(parsed['metadata'])
    else:
        indices = parsed['metadata']
        for indice in indices:
            try:
                child = parsed[indice]
            except KeyError:
                continue
            score += compute_score(child)
    return score


test_l_meta = parse_dict(test_input)[1]
assert compute_score(test_l_meta) == 66

l_meta = parse_dict(day08)[1]
print(f'Solution for part 2: {compute_score(l_meta)}')

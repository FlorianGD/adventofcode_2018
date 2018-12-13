"""AoC 2018 Day 12: Subterranean Sustainability"""

import re
from collections import deque
from tqdm import tqdm

# Part 1


def parse_input(file):
    next_gen = dict()
    with open(file) as f:
        initial_state = f.readline().strip()[15:]
        f.readline()  # skip blank line
        for line in f.readlines():
            # Take only the lines generating a plant
            if line[-2] == "#":
                next_gen[line[:5]] = line[-2]
    return initial_state, next_gen


def next_gen(init, next_dict):
    """
    Given a string of states and a dict of transitions, return the next state
    """
    # Append 4 empty pots in the beginning and in the end
    expanded = "...." + init + "...."
    next_state = deque()
    for k in range(2, len(expanded) - 3):
        pattern = expanded[k-2:k+3]
        next_state.append(next_dict.get(pattern, "."))
    return "".join(next_state)


def compute_score(state, zero_ind):
    """
    Compute the sum of the position of the flowers (#) in state, given that
    the 0th pot is at index zero_ind
    """
    indices = [match.start() - zero_ind for match in re.finditer("#", state)]
    return sum(indices)


def play(init, next_dict, n_gen=20):
    state = init
    for zero_ind in tqdm(range(0, 2 * n_gen, 2)):
        state = next_gen(state, next_dict)
    return compute_score(state, zero_ind + 2)

# test_init, test_next = parse_input("day12_test_input.txt")
# play(test_init, test_next)

# test_results = """...#..#.#..##......###...###...........
# ...#...#....#.....#..#..#..#...........
# ...##..##...##....#..#..#..##..........
# ..#.#...#..#.#....#..#..#...#..........
# ...#.#..#...#.#...#..#..##..##.........
# ....#...##...#.#..#..#...#...#.........
# ....##.#.#....#...#..##..##..##........
# ...#..###.#...##..#...#...#...#........
# ...#....##.#.#.#..##..##..##..##.......
# ...##..#..#####....#...#...#...#.......
# ..#.#..#...#.##....##..##..##..##......
# ...#...##...#.#...#.#...#...#...#......
# ...##.#.#....#.#...#.#..##..##..##.....
# ..#..###.#....#.#...#....#...#...#.....
# ..#....##.#....#.#..##...##..##..##....
# ..##..#..#.#....#....#..#.#...#...#....
# .#.#..#...#.#...##...#...#.#..##..##...
# ..#...##...#.#.#.#...##...#....#...#...
# ..##.#.#....#####.#.#.#...##...##..##..
# .#..###.#..#.#.#######.#.#.#..#.#...#..
# .#....##....#####...#######....#.#..##.
# """

# for i, state in enumerate(test_results.splitlines()):
#     print(f'iter {i}: score {compute_score(state, 3)}')

if __name__ == '__main__':
    init, next_dict = parse_input("day12_input.txt")
    print(f'Solution for part 1: {play(init, next_dict)}')

# Part 2
# 50000000000 (!) iterations required

# See the notebook day12.ipynb

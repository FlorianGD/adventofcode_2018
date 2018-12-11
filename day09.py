"""AoC 2018 Day 9 : Marble Mania"""

from collections import defaultdict

# Part 1


def play(num_players, num_marbles):
    """
    The players play in turn, posing marbles in a list until all marbles are
    posed. The marbles are posed 2 positions to the right (modulo the number of
    marbles). If a player places a marble multiple of 23, she does not place it
    but adds the value to her score, and remove the marble 7 positions to the
    left and adds it to her score as well. This is the new starting point.
    """
    players = defaultdict(int)
    marbles_circle = [0]
    current_position = 0
    player = 1
    for marble in range(1, num_marbles + 1):
        if marble % 23 == 0:
            players[player] += marble
            new_position = (current_position - 7) % len(marbles_circle)
            players[player] += marbles_circle.pop(new_position)
        else:
            new_position = (current_position + 1) % len(marbles_circle) + 1
            marbles_circle.insert(new_position, marble)
        current_position = new_position
        player = player % num_players + 1
    return players


def top_score(scores):
    return max(v for k, v in scores.items())


assert top_score(play(9, 25)) == 32
assert top_score(play(10, 1618)) == 8317
assert top_score(play(13, 7999)) == 146373
assert top_score(play(17, 1104)) == 2764
assert top_score(play(21, 6111)) == 54718
assert top_score(play(30, 5807)) == 37305

# Puzzle input
# 471 players; last marble is worth 72026 points

print(f'Solution for part 1: {top_score(play(471, 72026))}')

# Part 2

print(f'Solution for part 1: {top_score(play(471, 72026 * 100))}')

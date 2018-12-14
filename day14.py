"""AoC 2018 Day 14: Chocolate Charts"""

from collections import deque
from itertools import islice

# Part 1


def add_recipes(recipes, current1, current2):
    elf1 = recipes[current1]
    elf2 = recipes[current2]
    new_recipes = [int(r) for r in str(elf1 + elf2)]
    recipes.extend(new_recipes)


def move_elf(recipes, current):
    n_moves = recipes[current] + 1
    return (current + n_moves) % len(recipes)


def cook_n_recipes(n, recipes, elf1=0, elf2=1):
    while len(recipes) < n + 10:
        add_recipes(recipes, elf1, elf2)
        elf1 = move_elf(recipes, elf1)
        elf2 = move_elf(recipes, elf2)
    return ''.join(str(i) for i in islice(recipes, n, n+10))


assert cook_n_recipes(9, deque([3, 7])) == '5158916779'
assert cook_n_recipes(5, deque([3, 7])) == '0124515891'
assert cook_n_recipes(18, deque([3, 7])) == '9251071085'
assert cook_n_recipes(2018, deque([3, 7])) == '5941429882'

print(f'Solution for part 1: {cook_n_recipes(919901, deque([3, 7]))}')

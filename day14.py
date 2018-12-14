"""AoC 2018 Day 14: Chocolate Charts"""

# Part 1


def add_recipes(recipes, current1, current2):
    elf1 = recipes[current1]
    elf2 = recipes[current2]
    new_recipes = [int(r) for r in str(elf1 + elf2)]
    recipes.extend(new_recipes)


def move_elves(recipes, current1, current2):
    n_moves1 = recipes[current1] + 1
    n_moves2 = recipes[current2] + 1
    return ((current1 + n_moves1) % len(recipes),
            (current2 + n_moves2) % len(recipes))


def cook_n_recipes(n, recipes, elf1=0, elf2=1):
    while len(recipes) < n + 10:
        add_recipes(recipes, elf1, elf2)
        elf1, elf2 = move_elves(recipes, elf1, elf2)
    return ''.join(str(i) for i in recipes[n:n+10])


assert cook_n_recipes(9, [3, 7]) == '5158916779'
assert cook_n_recipes(5, [3, 7]) == '0124515891'
assert cook_n_recipes(18, [3, 7]) == '9251071085'
assert cook_n_recipes(2018, [3, 7]) == '5941429882'

print(f'Solution for part 1: {cook_n_recipes(919901, [3, 7])}')

# Part 2


def cook_until_pattern(pattern, recipes, elf1=0, elf2=1):
    size = len(pattern)
    pattern = [int(i) for i in pattern]
    previous_len = len(recipes)
    while True:
        recipes.extend([int(r) for r in str(recipes[elf1] + recipes[elf2])])
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
        for last_ind in range(previous_len + 1, len(recipes) + 1):
            if last_ind - size >= 0:
                for i, d in enumerate(pattern):
                    if recipes[last_ind - size + i] != d:
                        break
                else:
                    return last_ind - size
        previous_len = len(recipes)


assert cook_until_pattern('51589', [3, 7]) == 9
assert cook_until_pattern('01245', [3, 7]) == 5
assert cook_until_pattern('92510', [3, 7]) == 18
assert cook_until_pattern('59414', [3, 7]) == 2018


print(f'Solution for part 2: {cook_until_pattern("919901", [3, 7])}')

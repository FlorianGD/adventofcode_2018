"""AoC 2018 day 5 Alchemical Reduction"""

from itertools import zip_longest
# Part 1


def are_opposed(char1: str, char2: str) -> bool:
    """
    Are the 2 characters the same with different case?
    """
    return (char1.lower() == char2.lower()) & (char1 != char2)


def suppress_diff_cases(polymer: str) -> str:
    """
    Scan the input once and outputs a copy where no successive characters are
    the same char with a different case
    """
    reduced_poly = ""
    double_str = zip_longest(polymer, polymer[1:], fillvalue=' ')
    for char1, char2 in double_str:
        if not are_opposed(char1, char2):
            reduced_poly += char1
        else:
            # Skip the 2 characters
            next(double_str)
    return reduced_poly


def process(polymer: str) -> str:
    """
    Process the polymer while there are changes
    """
    processed = suppress_diff_cases(polymer)
    while len(processed) != len(polymer):
        polymer = processed
        processed = suppress_diff_cases(polymer)
    return processed


test_input = 'dabAcCaCBAcCcaDA'
assert process(test_input) == 'dabCBAcaDA'

with open('day05_input.txt', 'r') as f:
    day05 = f.readline().strip()

print(f'Solution for part 1: {len(process(day05))}')

# Part 2
# We need to preprocess the string to remove instances of one letter
# regardless of the case


def preprocess(polymer: str, char: str) ->str:
    """
    Remove all occurrences of the char in the polymer, regardless of case.
    char is lowercase
    """
    new = polymer.replace(char, '')
    new = new.replace(char.upper(), '')
    return new


def shortest_poly(polymer: str) -> int:
    """
    Preprocess the polymer with all letters and return the lenth of the
    shortest afer processing
    """
    shortest = 11946  # Solution from part 1 without preprocessing
    for char in set(polymer.lower()):
        new_poly = preprocess(polymer, char)
        length = len(process(new_poly))
        if length < shortest:
            shortest = length
    return shortest


assert shortest_poly(test_input) == 4
print(f'Solution for part 2: {shortest_poly(day05)}')

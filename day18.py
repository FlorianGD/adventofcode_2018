"""AoC 2018 Day 18: Settlers of The North Pole"""

from collections import Counter

# Part 1


class Land():
    def __init__(self, input):
        land = dict()
        for y, line in enumerate(input.splitlines()):
            for x, elem in enumerate(line):
                land[(x, y)] = elem
        self.current_land = land
        self.next_land = dict.fromkeys(land.keys(), "")

    def __repr__(self):
        count = Counter(self.current_land.values())
        return f'{count}'

    def __str__(self):
        lines = []
        x_max = max(x for x, y in self.current_land.keys())
        y_max = max(y for x, y in self.current_land.keys())
        for x in range(x_max + 1):
            line = ""
            for y in range(y_max + 1):
                line += self.current_land[(x, y)]
            lines.append(line)
        return '\n'.join(lines)

    def neighbors(self, coord):
        neighbors = []
        x0, y0 = coord
        for y in range(y0-1, y0+2):
            for x in range(x0-1, x0+2):
                if x == x0 and y == y0:
                    continue
                neighbors.append(self.current_land.get((x, y), ""))
        return [n for n in neighbors if n != ""]

    def transform(self, coord):
        """
        open ground (.), trees (|), or a lumberyard (#)

        * An open acre will become filled with trees if three or more adjacent
        acres contained trees. Otherwise, nothing happens.
        * An acre filled with trees will become a lumberyard if three or more
        adjacent acres were lumberyards. Otherwise, nothing happens.
        * An acre containing a lumberyard will remain a lumberyard if it was
        adjacent to at least one other lumberyard and at least one acre
        containing trees. Otherwise, it becomes open.
        """
        count_neighbors = Counter(self.neighbors(coord))
        if self.current_land[coord] == '.':
            if count_neighbors['|'] >= 3:
                self.next_land[coord] = "|"
            else:
                self.next_land[coord] = "."
        elif self.current_land[coord] == "|":
            if count_neighbors['#'] >= 3:
                self.next_land[coord] = "#"
            else:
                self.next_land[coord] = "|"
        else:
            if count_neighbors["#"] >= 1 and count_neighbors["|"] >= 1:
                self.next_land[coord] = "#"
            else:
                self.next_land[coord] = "."

    def one_minute(self):
        for coord in self.current_land.keys():
            self.transform(coord)
        self.current_land = self.next_land.copy()

    def n_minutes(self, n=10):
        for i in range(n):
            self.one_minute()
        count = Counter(self.current_land.values())
        return count['#'] * count['|']


with open("day18_input.txt") as f:
    day = f.read()

test = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

test_land = Land(test)
assert test_land.n_minutes() == 1147

if __name__ == '__main__':

    land = Land(day)
    print(f'Solution for part 1: {land.n_minutes()}')

# Part 2
# See notebook

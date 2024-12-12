"""
Oof.  Counting edges is hard.  Worked it out from first principles.
"""

from collections import defaultdict
from pathlib import Path
import sys
from typing import Self


class Region:
    def __init__(self, letter: str, x: int, y: int):
        self.letter = letter
        self.positions = {(x, y)}
        self.area = 1
        self.perimeter = 4
        self.num_sides = 4

    def price(self):
        return self.area * self.perimeter

    def discount_price(self):
        return self.area * self.num_sides

    def borders(self, x, y):
        # We are only ever  adding swaures from below and to the right, so the
        # only possible borders are above and left.
        return [
            (x2, y2)
            for (x2, y2) in [(x - 1, y), (x, y - 1)]
            if (x2, y2) in self.positions
        ]

    def try_add(self, x, y) -> bool:
        borders = self.borders(x, y)
        if borders:
            self.positions.add(
                (x, y),
            )
            self.area += 1
            self.perimeter += 4 - (2 * len(borders))
            upper_left = (x - 1, y - 1) in self.positions
            upper_right = (x + 1, y - 1) in self.positions
            from_above = borders[0] == (x, y - 1)
            if len(borders) == 1:
                self.num_sides += 2 * upper_left
                if from_above and upper_right:
                    # If adding from the left, then upper-right is irrelevant
                    self.num_sides += 2
            elif len(borders) == 2:
                # Connecting from both sides.  Number of sides can go *down*.
                if not upper_right:
                    self.num_sides -= 2
            return True
        return False

    def merge(self, other: Self, x, y):
        # Merging is always via a single bordered cell, left-to right, top-to-bbottom.
        self.positions.update(other.positions)

        self.area += other.area
        self.perimeter += other.perimeter - 2
        self.num_sides += other.num_sides
        # Merging implies that above and left were not touching until now.
        # We either lose zero or 2 sides.  It is zero only if the upper right was already in the shape,
        # *and* we merged from the left (implying the sides we lose are "extended").
        from_left = ((x, y - 1)) in other.positions
        upper_right = (x + 1, y - 1) in self.positions
        if not upper_right or not from_left:
            self.num_sides -= 2

    def __repr__(self):
        # Debugging help
        member_str = ", ".join((f"({x}, {y})" for x, y in self.positions))
        return f"{self.letter} - {member_str}"


def run(input: str) -> tuple[int, int]:
    grid = list(map(list, input.splitlines()))
    regions: defaultdict[str, list[Region]] = defaultdict(list)
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            candidates = regions[letter]
            region = None
            for c in candidates:
                if region:
                    # Already merged with another region!
                    if c.borders(x, y):
                        region.merge(c, x, y)
                        regions[letter].remove(c)
                else:
                    if c.try_add(x, y):
                        # This square is now in the region.
                        region = c

            if not region:
                regions[letter].append(Region(letter, x, y))

    part1 = sum(sum(region.price() for region in l) for l in regions.values())
    part2 = sum(sum(region.discount_price() for region in l) for l in regions.values())
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

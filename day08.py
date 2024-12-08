"""
More grid wrangling, and finding lines of sight.

Had to think about the right maths for calculating antinodes, but otherwise basically nice and smooth.
Think the trap here was to ensure you iterate over pairs of nodes, rather than iterate over the grid.
"""

from pathlib import Path
import math
import sys
from collections import defaultdict


def get_antinodes(coords, max_h, max_w, part2: bool):
    def in_bounds(x, y):
        return x >= 0 and y >= 0 and x < max_w and y < max_h

    # In part2, the nodes themselves are all antinodes as long as there are more than 1.
    ret = set(coords) if part2 and len(coords) > 1 else set()
    for i, (xa, ya) in enumerate(coords):
        for xb, yb in coords[i + 1 :]:
            diffx, diffy = (xa - xb, ya - yb)
            # Technically not needed since in the real input,
            # the x/y offset for each node pair is coprime.
            gcd = math.gcd(diffx, diffy)
            diffx /= gcd
            diffy /= gcd
            i = 1
            while True:
                if i > max_h:
                    raise Exception("Probable bug - infinite loop")

                candidates = set(
                    c
                    for c in (
                        (
                            (xa + i * diffx, ya + i * diffy),
                            (xb - i * diffx, yb - i * diffy),
                        )
                    )
                    if in_bounds(c[0], c[1])
                )
                ret.update(candidates)
                if not part2 or not candidates:
                    break
                i += 1
    return ret


def run(input: str) -> tuple[int, int]:
    node_map = defaultdict(list)
    max_h = max_w = 0
    for y, row in enumerate(input.splitlines()):
        max_h += 1
        for x, c in enumerate(row):
            if y == 0:
                max_w += 1
            if c != ".":
                node_map[c].append((x, y))

    antinodes1 = set(
        n
        for values in node_map.values()
        for n in get_antinodes(values, max_h, max_w, False)
    )
    part1 = len(antinodes1)
    antinodes2 = set(
        n
        for values in node_map.values()
        for n in get_antinodes(values, max_h, max_w, True)
    )
    part2 = len(antinodes2)
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

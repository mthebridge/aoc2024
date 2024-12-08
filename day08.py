"""
More grid wrangling, and finding lines of sight.

Had to think about the right maths for calculating antinodes, but otherwise all nice and smooth.
"""

from pathlib import Path
import sys
from collections import defaultdict


def get_antinodes(coords, max_h, max_w):
    def in_bounds(x, y):
        return x >= 0 and y >= 0 and x < max_w and y < max_h

    ret = []
    for i, (xa, ya) in enumerate(coords):
        for xb, yb in coords[i + 1 :]:
            diffx, diffy = xa - xb, ya - yb
            candidates = ((xa + diffx, ya + diffy), (xb - diffx, yb - diffy))
            ret.extend((c for c in candidates if in_bounds(c[0], c[1])))
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
    print(max_h, max_w)
    part1 = 0
    antinodes = set()
    for key, values in node_map.items():
        these = get_antinodes(values, max_h, max_w)
        print(f"For {key}: nodes at {values}, antinodes at {these}")
        antinodes.update(these)
    part1 = len(antinodes)
    part2 = 0
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

"""
Thought we might need something cleverer but simply loop through the grid and DFS all options to
fins the trails.
Since we are only ever looking for neighbours with "N+1" the decision space never branches too much
so just counting all the trails works fine.

Part 2 actually easier than part 1 - switch from sets to lists.
"""

from pathlib import Path
import sys
from typing import Iterable


def run(input: str) -> tuple[int, int]:
    grid = list(map(lambda row: list(int(c) for c in row), input.splitlines()))
    print(grid)
    WIDTH = len(grid[0])
    HEIGHT = len(grid)
    TRAIL_START = 0
    TRAIL_END = 9

    def neighbours(x, y):
        candidates = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        return [
            (cx, cy) for cx, cy in candidates if 0 <= cx < WIDTH and 0 <= cy < HEIGHT
        ]

    def find_trail_ends(grid, x, y) -> Iterable[tuple[int, int]]:
        current = grid[y][x]
        if current == TRAIL_END:
            yield (x, y)
        else:
            yield from (
                e
                for l in (
                    find_trail_ends(grid, nx, ny)
                    for (nx, ny) in neighbours(x, y)
                    if grid[ny][nx] == current + 1
                )
                for e in l
            )

    part1 = part2 = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == TRAIL_START:
                trails = list(find_trail_ends(grid, x, y))
                part1 += len(set(trails))
                part2 += len(trails)

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

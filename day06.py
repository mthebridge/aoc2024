"""
AOC at its core - grid and pathfinding.

Part 2 is super slow (10s) but the general online consensus is there's no clever trick - you do
to some extent just have to try every option.

Some cacheing would help - if you were to store the full path taken in order, you could start each iteration for
part 2 at the point in the path where the new obstacle was first hit rtaher than constantly recalculating.
Potential fix for future!
"""

from pathlib import Path
import sys
import copy
from typing import Optional


START_MARKER = "^"
WALL = "#"
FLOOR = "."


class InfiniteLoop(Exception):
    pass


def walk_line(
    grid: list[str],
    maxh: int,
    maxw: int,
    path: set[tuple[int, int, str]],
    start: tuple[int, int],
    dir: str,
) -> Optional[tuple[int, int, str]]:
    cur = (start[0], start[1], dir)
    i = 1
    while True:
        if cur in path:
            # Loop!
            raise InfiniteLoop
        path.add(cur)

        if dir == "N":
            next = (cur[0], cur[1] - 1, dir)
        elif dir == "E":
            next = (cur[0] + 1, cur[1], dir)
        elif dir == "S":
            next = (cur[0], cur[1] + 1, dir)
        elif dir == "W":
            next = (cur[0] - 1, cur[1], dir)
        else:
            raise ValueError("bad dir")

        if next[0] < 0 or next[0] >= maxw or next[1] < 0 or next[1] >= maxh:
            return None

        next_val = grid[next[1]][next[0]]
        if next_val == WALL:
            break

        cur = next
        i += 1

    return cur


def next_dir(dir):
    if dir == "N":
        return "E"
    elif dir == "E":
        return "S"
    elif dir == "S":
        return "W"
    elif dir == "W":
        return "N"
    else:
        raise ValueError("Invalid direction")


def do_walk(grid, maxh, maxw, start_x, start_y):
    cur = (start_x, start_y)
    path = set()
    dir = "N"

    while cur is not None:
        cur = walk_line(grid, maxh, maxw, path, cur, dir)
        dir = next_dir(dir)
    return path


def run(input: str) -> tuple[int, int]:
    grid = list(map(list, input.splitlines()))
    maxh = len(grid)
    maxw = len(grid[0])

    for start_y, row in enumerate(grid):
        try:
            start_x = row.index(START_MARKER)
            break
        except ValueError:
            pass

    path = do_walk(grid, maxh, maxw, start_x, start_y)
    visited = set(((x, y) for (x, y, _) in path))
    part1 = len(visited)
    part2 = 0
    for (
        x,
        y,
    ) in visited:
        if grid[y][x] == START_MARKER:
            continue
        grid[y][x] = WALL
        try:
            do_walk(grid, maxh, maxw, start_x, start_y)
        except InfiniteLoop:
            part2 += 1
        grid[y][x] = FLOOR  # Undo change

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

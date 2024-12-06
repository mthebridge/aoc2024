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
    visited: set[tuple[int, int]],
    start: tuple[int, int],
    dir: str,
    path: set[tuple[int, int, str]],
) -> Optional[tuple[int, int]]:
    cur = start
    i = 1
    while True:
        cur_with_dir = (cur[0], cur[1], dir)
        visited.add(cur)
        if cur_with_dir in path:
            # Loop!
            raise InfiniteLoop
        path.add(cur_with_dir)
        if dir == "N":
            next = (cur[0], cur[1] - 1)
        elif dir == "E":
            next = (cur[0] + 1, cur[1])
        elif dir == "S":
            next = (cur[0], cur[1] + 1)
        elif dir == "W":
            next = (cur[0] - 1, cur[1])
        else:
            raise ValueError("bad dir")

        if (
            next[0] < 0
            or next[0] >= len(grid[0])
            or next[1] < 0
            or next[1] >= len(grid)
        ):
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


def do_walk(grid, start_x, start_y):
    cur = (start_x, start_y)
    visited = set()
    path = set()
    dir = "N"
    while cur is not None:
        cur = walk_line(grid, visited, cur, dir, path)
        dir = next_dir(dir)
    return visited


def run(input: str) -> tuple[int, int]:
    grid = list(input.splitlines())

    for start_y, row in enumerate(grid):
        try:
            start_x = row.index(START_MARKER)
            break
        except ValueError:
            pass

    visited = do_walk(grid, start_x, start_y)
    part1 = len(visited)
    part2 = 0
    for x, y in visited:
        if grid[y][x] == FLOOR:
            new_grid = copy.copy(grid)
            row = new_grid[y]
            new_grid[y] = row[:x] + WALL + row[x + 1 :]
            try:
                do_walk(new_grid, start_x, start_y)
            except InfiniteLoop:
                part2 += 1

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

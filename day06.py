from pathlib import Path
import sys


START_MARKER = '^'
WALL = '#'
FLOOR = '.'

def walk_line(grid: list[str], visited: set[tuple[int, int, str]], start: tuple[int, int], dir: str):
    cur = start
    i = 1
    loops = 0
    while True:
        visited.add(cur)
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

        if next[0] < 0 or next[0] >= len(grid[0]) or next[1] < 0 or next[1] >= len(grid) :
            return (None, loops)

        next_val = grid[next[1]][next[0]]
        if next_val == WALL:
            break


        cur = next
        i += 1

    return (cur, loops)

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


def run(input: str) -> tuple[int, int]:
    grid = list(input.splitlines())

    for start_y, row in enumerate(grid):
        try:
            start_x = row.index(START_MARKER)
            break
        except ValueError:
            pass

    visited = set()
    cur = (start_x, start_y)
    dir = "N"
    part2 = 0
    while cur is not None:
        (cur, loops) = walk_line(grid, visited, cur, dir)
        part2 += loops
        dir = next_dir(dir)

    part1 = len(visited)
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

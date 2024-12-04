from pathlib import Path
import sys


def check_word(
    grid: list[str], start: tuple[int, int], direction: tuple[int, int]
) -> bool:
    x, y = start
    dx, dy = direction
    for i, c in enumerate("XMAS"):
        ty, tx = y + dy * i, x + dx * i
        try:
            if ty < 0 or tx < 0 or grid[ty][tx] != c:
                return False
        except IndexError:
            return False

    return True


DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def check_cross(grid: list[str], start: tuple[int, int]) -> bool:
    x, y = start
    if (
        x < 1
        or y < 1
        or x >= len(grid[0]) - 1
        or y >= len(grid) - 1
        or grid[y][x] != "A"
    ):
        return False
    diags = "".join(
        (grid[y - 1][x - 1], grid[y - 1][x + 1], grid[y + 1][x + 1], grid[y + 1][x - 1])
    )
    valids = ("MMSS", "MSSM", "SMMS", "SSMM")
    if diags in valids:
        return True
    return False


def run(input: str) -> tuple[int, int]:
    grid = list(input.splitlines())
    part1 = 0
    part2 = 0
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            for dir in DIRECTIONS:
                part1 += check_word(grid, (x, y), dir)
            part2 += check_cross(grid, (x, y))

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

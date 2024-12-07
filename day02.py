"""
A straightofrward part 1.

Part 2 held me up for a while as I tried to find a clever algorithm that didn't involve n^2
brute force.   I did not succeed, and since linesa re short the "just try removing every entry"
approach works well enough.
"""

from pathlib import Path
import itertools
import sys


def line_entries(line: str) -> list[int]:
    words = line.split()
    return list(map(int, words))


def diffs_safe(lvl_diffs: list[int]) -> bool:
    asc = lvl_diffs[0] > 0

    good = lambda x: (asc and x >= 1 and x <= 3) or (not asc and x <= -1 and x >= -3)
    return all(map(good, lvl_diffs))


def level_safe(input: list[int], dampener: bool) -> bool:
    lvl_diffs = list(map(lambda x: x[1] - x[0], itertools.pairwise(input)))

    if diffs_safe(lvl_diffs):
        return True
    elif dampener:
        for i in range(len(input)):
            new = input.copy()
            _ = new.pop(i)
            if level_safe(new, False):
                return True
    return False


def run(input: str) -> tuple[int, int]:
    lines = list(map(line_entries, input.splitlines()))
    part1 = len(list(filter(lambda x: level_safe(x, False), lines)))
    part2 = len(list(filter(lambda x: level_safe(x, True), lines)))
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

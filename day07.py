from pathlib import Path
from collections import deque
from typing import Tuple
import sys


def parse_line(line: str) -> Tuple[int, list[int]]:
    words = line.split()
    target = int(words[0].rstrip(":"))
    ops: list[int] = list(map(int, words[1:]))
    return target, ops


def check_valid(line: str, allow_concat: bool) -> int:
    target, ops = parse_line(line)
    to_check = deque([ops])
    while True:
        try:
            rem = to_check.popleft()
        except IndexError:
            break
        so_far = rem.pop(0)
        if not rem:
            if so_far == target:
                return target
            else:
                continue
        next = rem.pop(0)
        candidates = [so_far + next, so_far * next]
        if allow_concat:
            candidates.append(int(str(so_far) + str(next)))
        for c in candidates:
            if c <= target:
                to_check.append([c, *rem])

    return 0


def run(input: str) -> tuple[int, int]:
    part1 = sum(map(lambda x: check_valid(x, False), input.splitlines()))
    part2 = sum(map(lambda x: check_valid(x, True), input.splitlines()))
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

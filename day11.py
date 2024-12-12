"""
An AOC classic - the "aha you need dynamic programming for part 2" puzzle.

Super fast once I remembered that functoolslru_cache has a tiny default maximum!

"""

from pathlib import Path
import functools

import sys


@functools.lru_cache(maxsize=100000)
def transform(stone: str, blinks: int) -> int:
    if blinks == 0:
        return 1
    stone = stone.lstrip("0")
    if stone == "":
        return transform("1", blinks - 1)
    digit_len = len(stone)
    if digit_len % 2 == 0:
        mid = digit_len // 2
        return transform(stone[:mid], blinks - 1) + (transform(stone[mid:], blinks - 1))
    else:
        return transform(str(2024 * int(stone)), blinks - 1)


def simulate_blink(stones, blink_count) -> int:
    return sum(transform(s, blink_count) for s in stones)


def run(input: str) -> tuple[int, int]:
    stones = list(input.split())

    part1 = simulate_blink(stones, 25)
    part2 = simulate_blink(stones, 75)

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

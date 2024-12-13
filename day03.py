"""
Part 1 today was made for regex matching.

Gave up on trying to get a valid multiline regex for part 2 so simply scanned through for
the enable/disable instruction types and re-run part 1 code each time we end a section.
"""

from pathlib import Path
import re
import sys


VALID_MULTS = re.compile(r"mul\((\d+),(\d+)\)")
ENABLED = "do()"
DISABLED = "don't()"


def get_all_mults(input: str) -> int:
    pairs = VALID_MULTS.findall(input)
    return sum((int(a) * int(b) for a, b in pairs))


def run(input: str) -> tuple[int, int]:
    part1 = get_all_mults(input)
    part2 = 0
    enabled = True
    last_start = 0
    i = 0
    while i < len(input):
        if enabled:
            next_dis = input[i:].find(DISABLED)
            end_range = i + next_dis if next_dis != -1 else len(input)
            part2 += get_all_mults(input[last_start : end_range + 5])
            i = end_range + len(DISABLED)
            enabled = False
        else:
            next_en = input[i:].find(ENABLED)
            last_start = i + next_en if next_en != -1 else len(input)
            enabled = True
            i = last_start + len(ENABLED)

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

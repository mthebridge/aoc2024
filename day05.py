from pathlib import Path
import sys
from collections import defaultdict


def parse_line(line: str) -> tuple[int, int]:
    words = line.split()
    return int(words[0]), int(words[1])


def check_valid(pages: list[str], rule_map: dict[str, str]) -> bool:
    # Validity is only broken if
    for i, v in enumerate(pages):
        for j in range(i):
            if pages[j] in rule_map[v]:
                return False
    return True


def run(input: str) -> tuple[int, int]:
    [rules, updates] = input.split("\n\n", maxsplit=1)
    rule_map = defaultdict(list)
    for line in rules.splitlines():
        [a, b] = line.split("|", maxsplit=1)
        rule_map[a].append(b)

    part1 = 0
    for u in updates.splitlines():
        pages = u.split(",")
        if check_valid(pages, rule_map):
            part1 += int(pages[len(pages) // 2])

    part2 = 0
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

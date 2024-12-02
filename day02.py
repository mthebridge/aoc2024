from pathlib import Path
import sys


def parse_line(line: str) -> list[int]:
    words = line.split()
    return map(int, words)

def level_safe(input: list[str], dampener: bool) -> bool:
    lvl = list(parse_line(input))
    asc = lvl[1] > lvl[0]
    seen_bad = False
    for i in range(1, len(lvl)):
        diff = lvl[i] - lvl[i-1]
        if (asc and diff < 0) or (not asc and diff > 0) or abs(diff) < 1 or abs(diff) > 3:
            if dampener and not seen_bad:
                seen_bad = True
            else:
                return False

    return True


def run(input: str) -> tuple[int, int]:
    part1 = len(list(filter(lambda x: level_safe(x, False), input.splitlines())))
    part2 = len(list(filter(lambda x: level_safe(x, True), input.splitlines())))
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

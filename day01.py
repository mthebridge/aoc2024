from pathlib import Path
import sys


def parse_line(line: str) -> tuple[int, int]:
    words = line.split()
    return int(words[0]), int(words[1])


def run(input: str) -> tuple[int, int]:
    l1, l2 = zip(*((parse_line(l) for l in input.splitlines())))
    part1 = sum(abs(a - b) for a, b in zip(sorted(l1), sorted(l2)))
    part2 = sum(v * l2.count(v) for v in l1)
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

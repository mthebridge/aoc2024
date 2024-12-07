from pathlib import Path
import sys
from collections import defaultdict


def parse_line(line: str) -> tuple[int, int]:
    words = line.split()
    return int(words[0]), int(words[1])


def check_valid(pages: list[str], rule_map: dict[str, list[str]]) -> bool:
    # Check pairwise.  Since map holds before -> after direction,
    # check for violations by looking for any of the preceding elements.
    for i, v in enumerate(pages):
        if any(pages[j] in rule_map[v] for j in range(i)):
            return False
    return True


def sort_pages(pages: list[str], rule_map: dict[str, list[str]]) -> list[str]:
    # Topological DFS sort.  Lifted straight from Wikipedia.
    # This actually sorts in reverse order, but since we only need
    # the middle item this is fine.
    out = []

    def visit(page: str):
        if page not in pages:
            return

        for next in rule_map[page]:
            visit(next)

        pages.remove(page)
        out.append(page)

    while pages:
        visit(pages[0])

    return out


def run(input: str) -> tuple[int, int]:
    [rules, updates] = input.split("\n\n", maxsplit=1)
    rule_map = defaultdict(list)
    for line in rules.splitlines():
        [a, b] = line.split("|", maxsplit=1)
        rule_map[a].append(b)

    part1 = 0
    part2 = 0
    for u in updates.splitlines():
        pages = u.split(",")
        if check_valid(pages, rule_map):
            part1 += int(pages[len(pages) // 2])
        else:
            sorted_pages = sort_pages(pages, rule_map)
            part2 += int(sorted_pages[len(sorted_pages) // 2])

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

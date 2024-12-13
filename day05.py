"""
Again I wasn't super happy about the n^2 algorithms.

For part 1 I think unavoidable, as you have to check each pair in case there's a rule for them.  I can see an option where
rather than checking each pair in the page you check each rule one by one, but that feels clunkier.

For part 2 I wavered at first at just implementing sort - but some quick refreshers on CS101 reminded me this is
really a graph traversal problem, and so a linear DFS allows us to do a topological sort for each page.
"""

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

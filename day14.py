"""
Part 1 straightdorward enough.

Part 2 feels like an attempt to thwart the LLM users :)
In the end brute forced it - check for a row of more than 10 robots as
likely to be  a tree.  And pretty print it for good measure.
"""

from math import prod
from dataclasses import dataclass
from pathlib import Path
import functools
import re
import os
import sys
import time


type Point = tuple[int, int]


def parse_line(line: str) -> tuple[Point, Point]:
    matches = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
    assert matches is not None
    return (int(matches.group(1)), int(matches.group(2))), (
        int(matches.group(3)),
        int(matches.group(4)),
    )


MAX_HEIGHT = 103
MAX_WIDTH = 101


def calculate_velocity(pos: Point, vel: Point, steps=1) -> Point:
    final_pos = (
        (pos[0] + steps * vel[0]) % MAX_WIDTH,
        (pos[1] + steps * vel[1]) % MAX_HEIGHT,
    )

    return final_pos


def is_adjacent(p1: Point, p2: Point) -> bool:
    return abs(p1[0] - p2[0]) == 1 and abs(p1[1] - p2[1]) == 1


def print_grid(posns: set[Point]):
    print("\n")
    for y in range(MAX_HEIGHT):
        print(" ", end="")
        for x in range(MAX_WIDTH):
            if ((x, y)) in posns:
                print("#", end="")
            else:
                print(".", end="")
        print(" ")


def could_be_tree(posns: list[Point]) -> bool:
    # Find a largest set of connected nodes.
    pset = set(posns)
    for y in range(MAX_HEIGHT):
        row = 0
        last = False
        for x in range(MAX_WIDTH):
            if ((x, y)) in pset:
                if last:
                    row += 1
                elif not last:
                    row = 1
                    last = True
                if row > 10:
                    return True
            else:
                last = False
                row = 0

    return False


def run(file_input: str) -> tuple[int, int]:
    max_steps = 100
    quadrants = [0, 0, 0, 0]
    starts = [parse_line(l) for l in file_input.splitlines()]
    for pos, vel in starts:
        final_pos = calculate_velocity(pos, vel, steps=100)
        if final_pos[0] < MAX_WIDTH // 2 and final_pos[1] < MAX_HEIGHT // 2:
            quadrants[0] += 1
        elif final_pos[0] < MAX_WIDTH // 2 and final_pos[1] > MAX_HEIGHT // 2:
            quadrants[1] += 1
        elif final_pos[0] > MAX_WIDTH // 2 and final_pos[1] < MAX_HEIGHT // 2:
            quadrants[2] += 1
        elif final_pos[0] > MAX_WIDTH // 2 and final_pos[1] > MAX_HEIGHT // 2:
            quadrants[3] += 1
        else:
            assert final_pos[0] == MAX_WIDTH // 2 or final_pos[1] == MAX_HEIGHT // 2

    part1 = prod(quadrants)

    # Part 2 is poorly defined!
    # Start by just exploring...
    part2 = 0
    steps = 1
    posns = [x[0] for x in starts]
    vels = [x[1] for x in starts]
    while steps < 100000:
        posns = [calculate_velocity(pos, vel) for pos, vel in zip(posns, vels)]

        if could_be_tree(posns):
            print_grid(posns)
            part2 = steps
            break

        steps += 1

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

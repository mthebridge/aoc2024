"""
Solve simultaneous linear equations.  Use the muptiplciation method, checking
for integer solutions.

Slight hiccup for part2 from some instances in the real input only - needing to check all divisions for
remainder 0, not just the first.  But that was the only issue.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from math import gcd
from typing import Optional, Self


@dataclass
class Variable:
    x: int
    y: int

    def __repr__(self):
        return f"(X={self.x}, Y+{self.y})"


@dataclass
class Machine:
    prize: Variable
    button_a: Variable
    button_b: Variable

    def solve_part2(self) -> int:
        increment = 10_000_000_000_000
        self.prize.x += increment
        self.prize.y += increment
        return self.solve()

    def solve(self) -> int:
        # Need to solve:  Ax*An  + Bx*Bn = Px,  Ay*An  + By*Bn = Py, for minimal integer An and Bn
        # Multiply up and subtract so the equations cancel when summed.
        # In other words, we want Mx and My such that Mx * Ax == My * Ay.
        gcd_a = gcd(self.button_a.x, self.button_a.y)
        x_mult = self.button_a.y // gcd_a
        y_mult = self.button_a.x // gcd_a

        # Multiplying both equations and subtracting will cancel, leaving us with a solution for B,
        # iff the division has no remainder
        bn, b_rem = divmod(
            self.prize.x * x_mult - self.prize.y * y_mult,
            self.button_b.x * x_mult - self.button_b.y * y_mult,
        )
        if b_rem != 0:
            return 0

        # Now plug into equation for A, again checking the division has no remainder.
        (
            an,
            a_rem,
        ) = divmod(self.prize.x - (self.button_b.x * bn), self.button_a.x)
        if a_rem != 0:
            return 0

        assert an * self.button_a.x + bn * self.button_b.x == self.prize.x
        assert an * self.button_a.y + bn * self.button_b.y == self.prize.y
        return 3 * an + bn


def parse(input: str) -> Machine:
    lines = list(input.splitlines())
    a_matches = re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[0])
    assert a_matches is not None
    b_matches = re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[1])
    assert b_matches is not None
    prize_matches = re.match(r"Prize: X=(\d+), Y=(\d+)", lines[2])
    assert prize_matches is not None
    button_a = Variable(x=int(a_matches.group(1)), y=int(a_matches.group(2)))
    button_b = Variable(x=int(b_matches.group(1)), y=int(b_matches.group(2)))
    prize = Variable(x=int(prize_matches.group(1)), y=int(prize_matches.group(2)))
    return Machine(prize, button_a, button_b)


def run(input: str) -> tuple[int, int]:
    machines = map(parse, input.split("\n\n"))
    part1 = sum(map(Machine.solve, machines))
    machines = map(parse, input.split("\n\n"))
    part2 = sum(map(Machine.solve_part2, machines))
    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

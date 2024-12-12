import day12
import pytest


SMALL_INPUT = """AAAA
BBCD
BBCC
EEEC
"""

ABBA_INPUT = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

LARGE_INPUT = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

OXO_INPUT = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""


EX_INPUT = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""


@pytest.mark.parametrize(
    "input, expected_p1, expected_p2",
    [
        (LARGE_INPUT, 1930, 1206),
        (SMALL_INPUT, 140, 80),
        (OXO_INPUT, 772, 436),
        (EX_INPUT, 692, 236),
        (ABBA_INPUT, 1184, 368),
    ],
)
def test_day12(input, expected_p1, expected_p2):
    p1, p2 = day12.run(input)
    assert p1 == expected_p1
    assert p2 == expected_p2

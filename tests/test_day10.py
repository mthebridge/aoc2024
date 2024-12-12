import day10

INPUT = """0123
1234
8765
9876
"""

INPUT_LARGE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def test_day10():
    p1, p2 = day10.run(INPUT)
    assert p1 == 1
    assert p2 == 16

    p1, p2 = day10.run(INPUT_LARGE)
    assert p1 == 36
    assert p2 == 81

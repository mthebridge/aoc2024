import day02

INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_day2():
    p1, p2 = day02.run(INPUT)
    assert p1 == 2
    assert p2 == 4

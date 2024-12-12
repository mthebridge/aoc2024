import day11

INPUT = """125 17"""


def test_day11():
    p1, p2 = day11.run(INPUT)
    assert p1 == 55312
    assert p2 == 0

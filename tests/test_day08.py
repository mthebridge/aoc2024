import day08

INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def test_day8():
    p1, p2 = day08.run(INPUT)
    assert p1 == 14
    assert p2 == 34

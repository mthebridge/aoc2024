import day09

INPUT2 = "12345"
INPUT = "2333133121414131402"


def test_day9():
    p1, p2 = day09.run(INPUT2)
    assert p1 == 60
    assert p2 == 132

    p1, p2 = day09.run(INPUT)
    assert p1 == 1928
    assert p2 == 2858

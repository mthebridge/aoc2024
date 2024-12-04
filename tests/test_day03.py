import day03

INPUT = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def test_day3():
    p1, p2 = day03.run(INPUT)
    assert p1 == 161
    assert p2 == 48

from src import day01

INPUT = """3   4
4   3
2   5
1   3
3   9
3   3
"""

def test_day1():
    p1, p2 = day01.run(INPUT)
    assert p1 == 11
    assert p2 == 31

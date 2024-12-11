"""
A gentle starter.

Simply implement the given algorithm.  Python's ierable functions make things concise here.
"""

from pathlib import Path
import sys


def get_file_data(input: str, idx: int) -> tuple[int, int]:
    assert idx % 2 == 0
    return idx // 2, int(input[idx])


def calc_csum(file_id: int, file_size: int, disk_pos: int) -> int:
    return sum((file_id * (disk_pos + i) for i in range(file_size)))


def run(input: str) -> tuple[int, int]:
    ii = 0
    jj = len(input) - 1
    if jj % 2 == 1:
        jj -= 1
    part1 = 0
    cur_space = 0
    disk_pos = 0
    end_size = 0

    while ii <= jj:
        if ii % 2 == 0:
            # Existing file.
            start_id, start_size = get_file_data(input, ii)
            if ii == jj:
                # Already moved some of this file!
                start_size = end_size
            part1 += calc_csum(start_id, start_size, disk_pos)
            disk_pos += start_size
            ii += 1
        else:
            if end_size == 0:
                end_id, end_size = get_file_data(input, jj)

            if cur_space == 0:
                cur_space = int(input[ii])

            to_move = min(cur_space, end_size)
            part1 += calc_csum(end_id, to_move, disk_pos)
            disk_pos += to_move
            cur_space -= to_move
            end_size -= to_move

            if cur_space == 0:
                # Next file
                ii += 1
            if end_size == 0:
                # Move back to next file
                jj -= 2

    part2 = 0

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

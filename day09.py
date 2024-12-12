"""
Brute force algorithm that's slow but pretty memory efficient, as
it only stores one mutable copy of the input plus constant factor.

Main fun was keeping track of all the pointers and so on correctly.
Could do something cleverer but part 2 runs in 5 seconds...
"""

import copy
from pathlib import Path
import sys


def get_file_data(input: list[int], idx: int) -> tuple[int, int]:
    assert idx % 2 == 0
    return idx // 2, input[idx]


def calc_csum(file_id: int, file_size: int, disk_pos: int) -> int:
    # The checksum is file_id * (sum of disk positions), which is an arithemtic sequence
    return (
        file_size * ((file_id * disk_pos) + (file_id * (disk_pos + file_size - 1))) // 2
    )


def defrag(original_input: list[int], entire_files: bool) -> int:
    # Make a copy for original values.
    input = copy.copy(original_input)
    start_ptr = 0
    end_ptr = len(input) - 1
    if end_ptr % 2 == 1:
        end_ptr -= 1
    cur_end_ptr = end_ptr
    checksum = 0
    cur_space = 0
    disk_pos = 0
    end_size = 0

    while start_ptr <= end_ptr:
        if start_ptr % 2 == 0:
            # Existing file.  Add checksum and move disk forward.
            start_id, start_size = get_file_data(input, start_ptr)
            if start_size > 0:
                # print(f"Add checksum for file {start_id} at {disk_pos}")
                checksum += calc_csum(start_id, start_size, disk_pos)
            else:
                # We need to check how big the *original* file in this space was so we know
                # how far to advance the disk
                _, start_size = get_file_data(original_input, start_ptr)
            disk_pos += start_size
            start_ptr += 1
        else:
            cur_end_ptr = end_ptr
            if end_size == 0:
                end_id, end_size = get_file_data(input, cur_end_ptr)

            if cur_space == 0:
                cur_space = int(input[start_ptr])

            if entire_files:
                # No space for the whole file.  Keep moving backwards until we find one that does fit.
                # Start from the end until we find a non-zero-sized file that can move
                while (
                    end_size > cur_space or end_size == 0
                ) and cur_end_ptr > start_ptr:
                    # print(cur_space, end_ptr, cur_end_ptr, end_size)
                    cur_end_ptr -= 2
                    end_id, end_size = get_file_data(input, cur_end_ptr)

                # We either have found a space, or this file can't go anywhere.
                if end_size > cur_space or cur_end_ptr <= start_ptr:
                    # Nothing can fit in this space.  Move the disk up, and reset end_size.
                    # print(f"No files fit at {start_ptr}, increment disk by {cur_space}")
                    disk_pos += cur_space
                    cur_space = 0
                    end_size = 0

            if cur_space != 0:
                to_move = min(cur_space, end_size)
                checksum += calc_csum(end_id, to_move, disk_pos)
                disk_pos += to_move
                cur_space -= to_move
                end_size -= to_move
                input[cur_end_ptr] = end_size

            if cur_space == 0:
                # Next file
                start_ptr += 1
            if end_size == 0 and not entire_files:
                # Move back to next file
                end_ptr -= 2

    return checksum


def run(input: str) -> tuple[int, int]:
    data = list(map(int, input.strip()))
    part1 = defrag(data, False)
    part2 = defrag(data, True)

    return part1, part2


if __name__ == "__main__":
    p1, p2 = run(Path(sys.argv[1]).read_text())
    print(f"Part 1: {p1}, Part 2: {p2}")

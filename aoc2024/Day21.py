import time
from functools import cache

import Utils
from aocd import submit

day = 21
year = 2024
p1_expected_tst_result = 126384
p2_expected_tst_result = 154115708116294

Utils.download_input(year, day)

"""
┌───────────┬───────────┬───────────┐
│ 7 (0, -3) │ 8 (1, -3) │ 9 (2, -3) │
├───────────┼───────────┼───────────┤
│ 4 (0, -2) │ 5 (1, -2) │ 6 (2, -2) │
├───────────┼───────────┼───────────┤
│ 1 (0, -1) │ 2 (1, -1) │ 3 (2, -1) │
└───────────┼───────────┼───────────┤
  (0,  0)   │ 0 (1,  0) │ A (2,  0) │
            └───────────┴───────────┘
"""
# Coords are such that (0,0) is the empty space on both
key_pad = {
    '7': (0, -3), '8': (1, -3), '9': (2, -3),
    '4': (0, -2), '5': (1, -2), '6': (2, -2),
    '1': (0, -1), '2': (1, -1), '3': (2, -1),
    '0': (1, 0), 'A': (2, 0)
}

"""
           ┌──────────┬──────────┐
   (0, 0)  │ ^ (1, 0) │ A (2, 0) │
┌──────────┼──────────┼──────────┤
│ < (0, 1) │ v (1, 1) │ > (2, 1) │
└──────────┴──────────┴──────────┘
"""
d_pad = {
    '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
}


def vector_dif(v, w):
    return v[0] - w[0], v[1] - w[1]


# Move from cur_pos to target position. Target position also contains how many times it needs to be pressed.
@cache
def calc_length(target, cur_pos, max_depth):
    target_pos, num_presses = target

    if max_depth == 0:
        return num_presses

    length = 0
    x_dif, y_dif = vector_dif(cur_pos, target_pos)
    x_mov = (d_pad['>'], abs(x_dif)) if x_dif < 0 else (d_pad['<'], x_dif)
    y_mov = (d_pad['v'], abs(y_dif)) if y_dif < 0 else (d_pad['^'], y_dif)
    end_mov = (d_pad['A'], num_presses)

    if x_dif == 0:
        length += (calc_length(y_mov, d_pad['A'], max_depth - 1) +
                   calc_length(end_mov, y_mov[0], max_depth - 1))
    elif y_dif == 0:
        length += (calc_length(x_mov, d_pad['A'], max_depth - 1) +
                   calc_length(end_mov, x_mov[0], max_depth - 1))
    elif cur_pos[1] == 0 and target_pos[0] == 0:
        # Avoiding (0,0) is the highest priority
        length += (calc_length(y_mov, d_pad['A'], max_depth - 1) +
                   calc_length(x_mov, y_mov[0], max_depth - 1) +
                   calc_length(end_mov, x_mov[0], max_depth - 1))
    elif (cur_pos[0] == 0 and target_pos[1] == 0) or x_dif > 0:
        # '<' is the furthest from 'A', and itself takes two '<' pushes to reach
        # Move to it first when possible to avoid splitting the two '<'
        length += (calc_length(x_mov, d_pad['A'], max_depth - 1) +
                   calc_length(y_mov, x_mov[0], max_depth - 1) +
                   calc_length(end_mov, y_mov[0], max_depth - 1))
    else:
        length += (calc_length(y_mov, d_pad['A'], max_depth - 1) +
                   calc_length(x_mov, y_mov[0], max_depth - 1) +
                   calc_length(end_mov, x_mov[0], max_depth - 1))
    return length


def solve(codes, robots=3):
    complexity = 0

    for code in codes:
        length = 0
        for i in range(len(code)):
            length += calc_length((key_pad[code[i]], 1), key_pad[code[i - 1]], robots)
        complexity += int(code[:-1]) * length

    return complexity


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve(tst_input, 26)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve(puzzle_input, 26)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")

import time
from functools import cache

import Utils
from aocd import submit

day = 19
year = 2024
p1_expected_tst_result = 6
p2_expected_tst_result = 16

Utils.download_input(year, day)


def parse(data):
    patterns, designs = data.split("\n\n")
    return [p for p in patterns.split(", ")], [d for d in designs.split("\n")]


def solve(data):
    patterns, designs = parse(data)

    max_pattern_length = max([len(p) for p in patterns])

    @cache
    def count_reductions(design):
        if len(design) == 0:
            count = 1
        else:
            count = 0
            for i in range(min(max_pattern_length, len(design))):
                match_part = design[0:i+1]
                rest = design[i+1:]

                if match_part in patterns:
                    count += count_reductions(rest)

        return count

    cnt = 0
    cnt_all = 0
    for d in designs:
        amt_solutions = count_reductions(d)
        if amt_solutions > 0:
            cnt += 1
            cnt_all += amt_solutions

    return cnt, cnt_all


if __name__ == "__main__":
    tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result[0]}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result[0] == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result[0], part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p1_tst_result[1]}.")
    if p1_tst_result[1] == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p1_result[1], part="b", day=day, year=year)
    else:
        print("Test failed")

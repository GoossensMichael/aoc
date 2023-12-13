import functools

import Utils
import re
import time
from aocd import submit

day = 12
year = 2023
p1_expected_tst_result = 21
p2_expected_tst_result = 525152

Utils.download_input(year, day)
spring_states = [".", "#"]


def count_possible_groups(template):
    if len(template) == 0:
        return 0

    cnt = 0
    if template[0] == ".":
        in_group = False
    else:
        in_group = True
        cnt += 1

    i = 1
    while i < len(template):
        if in_group:
            if template[i] in (".", "?"):
                in_group = False
        else:
            if template[i] in ("#", "?"):
                in_group = True
                cnt += 1
        i += 1

    return cnt


def copy(springs_report, copy_count):
    springs, report = springs_report

    n_springs = springs
    n_springs_report = report
    for _ in range(0, copy_count):
        n_springs += "?" + springs
        n_springs_report += "," + report

    return n_springs, n_springs_report


@functools.cache
def permutate(springs, report):
    if len(report) == 0:
        valid = 1 if "#" not in springs else 0
        return valid

    cnt_p = count_possible_groups(springs)
    s_r = sum(report)
    l_r = len(report)
    if cnt_p < l_r and len(springs) < (s_r + l_r - 1) and count_possible_groups(springs) < len(report):
        return 0

    while len(springs) > 0 and springs[0] == ".":
        springs = springs[1:]

    if len(springs) > 0:
        # Mandatory group of damaged springs - Needs to be parsed for the size of the next report value.
        if springs[0] == "#":
            i = 0
            while i < len(springs) and i < report[0] and springs[i] in ["#", "?"]:
                i += 1

            if i == report[0]:
                springs = springs[i:]
                if 0 == len(springs):
                    # The current report still matches the springs -> exit
                    return permutate(springs, report[1:])
                elif springs[0] in [".", "?"]:
                    dot_permutation = "."
                    if len(springs) > 0:
                        dot_permutation += springs[1:]
                    return permutate(dot_permutation, report[1:])
                else:
                    return 0
            else:
                return 0
        else:
            dot_permutation = "." + springs[1:]
            hash_permutation = "#" + springs[1:]
            return (permutate(dot_permutation, report) +
                    permutate(hash_permutation, report))
    else:
        return 0




def solve(data, copy_count=0):
    s_data = tuple([copy([springs_report for springs_report in d.split()], copy_count) for d in data])
    spring_reports = tuple([(r, tuple([int(g) for g in gs.split(",")])) for r, gs in s_data])

    return sum(permutate(springs, report) for springs, report in spring_reports)


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")
#
print()
start_time = time.time()
print("Part 2")
p2_tst_result = solve(tst_input, 4)
print(f"Test solution: {p2_tst_result}.")
print(f"Elapsed time: {time.time() - start_time} seconds")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    start_time = time.time()
    p2_result = solve(puzzle_input, 4)
    print(f"Elapsed time: {time.time() - start_time} seconds")
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")

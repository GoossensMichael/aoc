from itertools import permutations
from math import floor

import Utils
from aocd import submit
from collections import defaultdict

day = 5
year = 2024
p1_expected_tst_result = 143
p2_expected_tst_result = 123

Utils.download_input(year, day)


def parse(data):
    pipe_section, list_section = data.split("\n\n")

    # Create maps
    forward_map = defaultdict(list)

    for line in pipe_section.strip().split("\n"):
        key, value = map(int, line.split("|"))
        forward_map[key].append(value)

    list_of_lists = []

    for line in list_section.strip().split("\n"):
        list_of_lists.append(list(map(int, line.split(","))))

    return forward_map, list_of_lists


def is_right_order(pages, map):
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            if pages[i] in map[pages[j]]:
                return False

    return True


def solve(data):
    ordering, updates = parse(data)

    sum = 0
    sum2 = 0
    for i in updates:
        if is_right_order(i, ordering):
            sum += i[floor(len(i) / 2)]
        else:
            s = []
            for w in i:
                rules = ordering[w]
                pos = len(s)
                for r in rules:
                    try:
                        pos = min(pos, s.index(r))
                    except ValueError:
                        pos = min(pos, len(s))
                s.insert(pos, w)
            sum2 += s[floor(len(s) / 2)]

    return sum, sum2


def sort(rules):
    s = []

    for k, v in rules.items():
        pos = len(s)
        for n in v:
            try:
                pos = min(pos, s.index(n))
            except ValueError:
                pos = min(pos, len(s))
        s.insert(pos, k)

    return s


if __name__ == "__main__":
    tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

    print("Part 1")
    p1_tst_result, p2_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        p1_result, p2_result = solve(puzzle_input)
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")

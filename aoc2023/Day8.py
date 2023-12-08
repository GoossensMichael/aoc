import Utils
import math
from itertools import cycle
from aocd import submit

day = 8
year = 2023
p1_expected_tst_result = 6
p2_expected_tst_result = 6

Utils.download_input(year, day)


def parse(data):
    (d, p) = data.split("\n\n")

    return cycle(d), {p: (l, r) for p, l, r in [Utils.extract_string("% = (%, %)", p) for p in p.split("\n") if p != ""]}


def ending_with(path_map, c):
    return set([k for k in path_map.keys() if k[2] == c])


def solve(data):
    (directions, path_map) = parse(data)

    p, i = "AAA", 0
    while p != "ZZZ":
        p, i = path_map[p][0] if next(directions) == "L" else path_map[p][1], i + 1

    return i


def solve2(data):
    (directions, path_map) = parse(data)

    starting_points, solutions, i = ending_with(path_map, "A"), [], 0
    amt_starting_points = len(starting_points)
    while len(solutions) != amt_starting_points:
        d, i, new_positions = next(directions), i + 1, []
        for p in starting_points:
            new_position = path_map[p][0] if d == "L" else path_map[p][1]
            solutions.append(i) if new_position[2] == "Z" else new_positions.append(new_position)
        starting_points = new_positions

    return math.lcm(*solutions)


tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

tst_input = Utils.read_input_flat(f"input/day{day}_tst2_input.txt")
print()
print("Part 2")
p2_tst_result = solve2(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve2(puzzle_input)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")

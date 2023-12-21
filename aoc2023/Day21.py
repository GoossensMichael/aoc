import Utils
from aocd import submit
import math

day = 21
year = 2023
p1_expected_tst_result = 16
p2_expected_tst_result = 528192461129799

Utils.download_input(year, day)

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def find_s(garden):
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            if garden[i][j] == "S":
                return i, j
    return None

def all_plots(garden):
    all_plots = set()
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            all_plots.add((i, j))
    return all_plots


def solve(data, steps = 6):
    garden = [[d for d in l] for l in data]
    s = find_s(garden)

    reached_plots = {(s[0], s[1])}
    for _ in range(steps):
        n_reached_plots = set()
        for reached_plot in reached_plots:
            for d in directions:
                p = Utils.add_2d(reached_plot, d)
                if garden[p[0] % len(garden)][p[1] % len(garden[0])] != "#" and p not in n_reached_plots:
                    n_reached_plots.add(p)
        reached_plots = n_reached_plots

    return len(reached_plots)

def solve_quadratic(f0, f1, f2, n):
    # Constructing f(n) = an^2 + bn + c by using f0, f1 and f2 as model results for f(0), f(1) and f(2), which
    # provide three equations to derive the general one from.
    a = (f2 - 2 * f1 + f0) // 2
    b = f1 - f0 - a
    c = f0

    return a * n**2 + b * n + c

def solve_p2(data, steps):
    garden_size = len(data)
    border_distance = garden_size // 2

    f0, f1, f2 = [solve(data, n) for n in (border_distance, border_distance + garden_size, border_distance + 2 * garden_size)]

    amount_of_tiles = (steps - border_distance) // garden_size

    return solve_quadratic(f0, f1, f2, amount_of_tiles)


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input, 64)
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
p2_tst_result = solve_p2(tst_input, 26501365)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve_p2(puzzle_input, 26501365)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")

import math
import Utils
from aocd import submit

day = 6
year = 2023
p1_expected_tst_result = 288
p2_expected_tst_result = 71503

Utils.download_input(year, day)


def parse(data, merge):
    if merge:
        return [(int(data[0][10:].replace(" ", "")), int(data[1][10:].replace(" ", "")))]
    else:
        return [(t, d) for t, d in zip([int(d) for d in data[0].split()[1:]], [int(d) for d in data[1].split()[1:]])]


def disc(t, d):
    return math.sqrt(t ** 2 - (4 * d))


def solve(data, merge = False):
    return math.prod([math.ceil((t + disc(t, d)) / 2) - math.floor((t - disc(t, d)) / 2) - 1 for (t, d) in parse(data, merge)])


def solve_brute_force(data, merge = False):
    games = parse(data, merge)

    cnt = 1
    for t, d in games:
        win = 0
        for speed in range(1, t + 1):
            distance = (t - speed) * speed
            if (distance > d):
                win += 1

        if win > 0:
            cnt *= win

    return cnt

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input)
    print(f"Puzzle solution: {p1_result}.")
    if input("submit part 1? (y or n) - ") == "y":
        submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
p2_tst_result = solve(tst_input, True)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve(puzzle_input, True)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)
